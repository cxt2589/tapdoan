import os
import sys
import json
import time
import datetime
import subprocess
import requests
import threading
import re
import html

# Ensure unbuffered output for PM2 logs
sys.stdout.reconfigure(line_buffering=True)


from trading_agent_core import (
    load_config, save_config, generate_morning_plan, 
    generate_weekly_report, get_market_data, get_today_news
)

CONFIG_FILE = "/opt/trading_agent/config.json"

def send_msg(chat_id, text, reply_markup=None, parse_mode="HTML"):
    cfg = load_config()
    token = cfg.get("bot_token")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        r = requests.post(url, json=payload, timeout=15)
        res = r.json()
        if not res.get("ok") and parse_mode:
            # Fallback to plain text if formatting tags failed
            payload.pop("parse_mode", None)
            r = requests.post(url, json=payload, timeout=15)
            res = r.json()
        return res
    except Exception as e:
        print(f"[!] Error sending msg: {e}")
        return None

def send_chat_action(chat_id, action="typing"):
    cfg = load_config()
    token = cfg.get("bot_token")
    url = f"https://api.telegram.org/bot{token}/sendChatAction"
    try:
        requests.post(url, json={"chat_id": chat_id, "action": action}, timeout=5)
    except Exception:
        pass

class TypingHeartbeat:
    """Sends typing action to Telegram periodically while an operation is processing."""
    def __init__(self, chat_id, interval=3.5):
        self.chat_id = chat_id
        self.interval = interval
        self.stop_event = threading.Event()
        self.thread = None

    def _run(self):
        while not self.stop_event.is_set():
            send_chat_action(self.chat_id, "typing")
            self.stop_event.wait(self.interval)

    def start(self):
        send_chat_action(self.chat_id, "typing")
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)

def markdown_to_telegram_html(text):
    if not text:
        return text
    
    # 1. Protect code blocks by extracting them
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(2))
        return f"@@@CODEBLOCK{len(code_blocks)-1}@@@"
    
    text = re.sub(r'```([a-zA-Z0-9_]*)\n?([\s\S]*?)```', save_code_block, text)
    
    # 2. Protect inline code
    inline_codes = []
    def save_inline_code(match):
        inline_codes.append(match.group(1))
        return f"@@@INLINECODE{len(inline_codes)-1}@@@"
    
    text = re.sub(r'`([^`\n]+)`', save_inline_code, text)

    # 3. HTML escape remaining text
    text = html.escape(text, quote=False)

    # 4. Convert markdown headers: # Header -> <b>Header</b> (must require at least 1 space so hashtags aren't caught)
    text = re.sub(r'^#{1,6}\s+(.+)$', r'<b>\1</b>', text, flags=re.MULTILINE)

    # 5. Convert bold: **text** or __text__ -> <b>text</b>
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__([^_]+)__', r'<b>\1</b>', text)

    # 6. Convert italic: *text* or _text_ -> <i>text</i>
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', text)
    text = re.sub(r'(?<![a-zA-Z0-9_])_([^_]+)_(?![a-zA-Z0-9_])', r'<i>\1</i>', text)

    # 7. Restore inline code
    for i, code in enumerate(inline_codes):
        escaped_code = html.escape(code, quote=False)
        text = text.replace(f"@@@INLINECODE{i}@@@", f"<code>{escaped_code}</code>")

    # 8. Restore code blocks
    for i, code in enumerate(code_blocks):
        escaped_code = html.escape(code, quote=False)
        text = text.replace(f"@@@CODEBLOCK{i}@@@", f"<pre><code>{escaped_code}</code></pre>")

    return text

def send_long_msg(chat_id, text):
    if not text:
        return
    # Convert standard Markdown from AI into valid Telegram HTML
    formatted_html = markdown_to_telegram_html(text)
    max_len = 4000
    if len(formatted_html) <= max_len:
        send_msg(chat_id, formatted_html)
        return
    # Chunk cleanly by paragraphs
    paragraphs = formatted_html.split("\n\n")
    current_chunk = ""
    for p in paragraphs:
        if len(current_chunk) + len(p) + 2 <= max_len:
            current_chunk += (p + "\n\n")
        else:
            if current_chunk:
                send_msg(chat_id, current_chunk.strip())
                time.sleep(0.5)
            current_chunk = p + "\n\n"
    if current_chunk:
        send_msg(chat_id, current_chunk.strip())


def answer_callback(cb_id, text):
    cfg = load_config()
    token = cfg.get("bot_token")
    url = f"https://api.telegram.org/bot{token}/answerCallbackQuery"
    try:
        requests.post(url, json={"callback_query_id": cb_id, "text": text, "show_alert": True}, timeout=10)
    except Exception as e:
        print(f"[!] Error answering callback: {e}")

def edit_msg_reply_markup(chat_id, msg_id, reply_markup=None):
    cfg = load_config()
    token = cfg.get("bot_token")
    url = f"https://api.telegram.org/bot{token}/editMessageReplyMarkup"
    payload = {"chat_id": chat_id, "message_id": msg_id}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"[!] Error editing markup: {e}")

use_continue_session = True

EXECUTIVE_SYSTEM_PREFIX = (
    "LỆNH ĐIỀU HÀNH TẬP ĐOÀN (BẮT BUỘC TUÂN THỦ NGHIÊM NGẶT):\n"
    "Cơ quan thừa hành & phát ngôn: Văn phòng Thư ký Tập đoàn.\n"

    "KỸ NĂNG ÁP DỤNG: Chuẩn hóa văn bản hành chính & thiết kế tin nhắn Telegram cấp cao (executive-admin-telegram-drafter).\n"
    "QUY CHUẨN ĐỊNH DẠNG TIN NHẮN BÁO CÁO:\n"
    "1. CHUẨN HÓA DANH XƯNG: Luôn xưng là 'Văn phòng Thư ký Tập đoàn'. TUYỆT ĐỐI KHÔNG xưng là 'Văn phòng Tổng Hành Dinh'.\n"
    "2. NGHỆ THUẬT THIẾT KẾ TIN NHẮN TELEGRAM (MICRO-VISUAL COMMUNICATION):\n"
    "   - Bố cục thị giác gọn gàng, sắc nét, tối ưu cho màn hình điện thoại di động (đọc hiểu trong 30 giây).\n"
    "   - Sử dụng các neo thị giác (Visual Anchors) khi cần: 🎯 Mục tiêu, ⏱️ Thời hạn, 👤 Người phụ trách, 💰 Số liệu, 📌 Hành động bắt buộc.\n"
    "   - Khi Chủ tịch yêu cầu ban hành lệnh điều hành hoặc thông báo: Thiết kế mẫu tin nhắn điều hành hoàn chỉnh kèm Hashtag điều phối (#ChiDaoChuTich #VanPhongThuKy #TienDoTapDoan).\n"
    "3. TUYỆT ĐỐI KHÔNG TRÍCH NGUỒN, KHÔNG DÙNG LINK FILE (file://...), KHÔNG GHI ĐƯỜNG DẪN /opt/... HAY TÊN FILE .md (như SO_TAY_THU_KY.md, PORTFOLIO.md, README.md): Cấm tuyệt đối chèn link file markdown.\n"
    "4. TUYỆT ĐỐI KHÔNG DIỄN KỊCH: Cấm hoàn toàn văn phong kịch bản, tiểu thuyết, hoặc miêu tả hành động trong ngoặc đơn như *(nhấn chuông)*, *(cúi đầu)*, *(mở cửa)*, v.v.\n"
    "5. XƯNG HÔ CHUẨN MỰC: Mở đầu bằng 'Báo cáo Chủ tịch:' hoặc 'Kính thưa Chủ tịch,'. Kết thúc bằng 'Kính trình Chủ tịch chỉ đạo.' hoặc ngắn gọn.\n"
    "6. TINH GỌN, TRỰC DIỆN (EXECUTIVE COMPACT): Trình bày ngắn gọn, súc tích, tối ưu hoàn hảo cho màn hình điện thoại Telegram. Không lạm dụng trích dẫn lồng nhau, không dùng divider rườm rà.\n"
    "7. KHI TRIỆU TẬP HOẶC ĐIỂM DANH CÁC CÔNG TY CON: Mỗi đơn vị trình bày đúng 1 đến 2 dòng gồm Tên đơn vị, Người phụ trách, và Trọng tâm công việc cốt lõi. Tuyệt đối không chèn link hay tên file sổ tay.\n"
    "8. ĐI THẲNG VÀO NỘI DUNG: Trả lời đúng trọng tâm yêu cầu của Chủ tịch, nêu rõ số liệu, tiến độ, quyết sách hoặc đề xuất cần phê duyệt.\n\n"
    "NỘI DUNG YÊU CẦU CỦA CHỦ TỊCH:\n"
)


def clean_executive_output(text):
    if not text:
        return text
    
    # 1. Remove theatrical action lines or narrative paragraphs
    text = re.sub(r'^\s*[\*\s]*\(?.*?(?:nhấn chuông|cúi đầu|phòng họp mở rộng|bước vào|tề tựu|bút sổ).*?\)?[\*\s\.]*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r'^\s*\*[^\n]+\*\.?\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*\([^\)]*\)\*', '', text)

    # 2. Remove theatrical closing lines
    text = re.sub(r'^\s*Các đơn vị đã mở sổ tay[^\n]*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*Các đơn vị đã sẵn sàng tiếp nhận[^\n]*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\(?\s*Xem chi tiết[^\n]*\)?\s*$', '', text, flags=re.MULTILINE | re.IGNORECASE)

    # 3. Strip all file links and paths (No file:/// links, no /opt/ paths, no .md files)
    text = re.sub(r'\(\s*\[[^\]]+\]\(file:///[^\)\s]+\)\s*\)', '', text)
    text = re.sub(r'\[`?[a-zA-Z0-9_\-\/]+`?\]\(file:///[^\)\s]+\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\(file:///[^\)\s]+\)', r'\1', text)
    text = re.sub(r'\(?\s*file:///[^\)\s]+\s*\)?', '', text)
    text = re.sub(r'\(?\s*/opt/[^\)\s]+\s*\)?', '', text)
    text = re.sub(r'[`\'"]?[\w_\-]+\.(?:md|json|py|txt|sh)[`\'"]?', '', text)

    # 4. Strip leftover phrases like "kèm Thư ký riêng mang"
    text = re.sub(r'kèm\s+(?:Thư ký riêng\s+)?mang\s*', '', text, flags=re.IGNORECASE)

    # 5. Clean up blockquotes and dividers
    text = re.sub(r'^>\s*(\*")?', '', text, flags=re.MULTILINE)
    text = re.sub(r'("\*|\*")\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'(---\s*)+', '', text)

    # 6. Normalize official name to 'Văn phòng Thư ký Tập đoàn'
    text = re.sub(r'Văn phòng Tổng Hành Dinh', 'Văn phòng Thư ký Tập đoàn', text, flags=re.IGNORECASE)
    text = re.sub(r'Thư ký Tổng Hành Dinh', 'Văn phòng Thư ký Tập đoàn', text, flags=re.IGNORECASE)
    text = re.sub(r'Tổng Thư Ký Tổng Hành Dinh', 'Văn phòng Thư ký Tập đoàn', text, flags=re.IGNORECASE)

    # 7. Clean up punctuation and spacing
    text = re.sub(r'\(\s*\)', '', text)
    text = re.sub(r'\s+:', ':', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def run_antigravity_chat(prompt, continue_session=True):
    global use_continue_session
    try:
        full_prompt = EXECUTIVE_SYSTEM_PREFIX + prompt
        cmd = ["/usr/local/bin/agy"]
        if continue_session and use_continue_session:
            cmd.append("-c")
        cmd.extend([
            "-p", full_prompt,
            "--model", "gemini-3.8-flash-high",
            "--dangerously-skip-permissions"
        ])
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=180, cwd="/opt/tapdoan")
        out = res.stdout.strip()
        err = res.stderr.strip()
        if out:
            return clean_executive_output(out)
        elif err:
            return f"⚠️ [Antigravity Output]:\n{err}"
        return "✅ Nhiệm vụ đã hoàn tất."
    except subprocess.TimeoutExpired:
        return "⏱️ [Timeout] Nhiệm vụ mất hơn 3 phút để xử lý. Vui lòng chia nhỏ câu hỏi."
    except Exception as e:
        return f"❌ [Lỗi]: {e}"

def telegram_poller():
    global use_continue_session
    cfg = load_config()
    token = cfg.get("bot_token")
    last_update_id = 0
    print("[*] Starting Telegram Bot Poller in NATURAL CHAT MODE with Gemini 3.8 Flash High & Executive Heartbeat...")

    while True:
        try:
            url = f"https://api.telegram.org/bot{token}/getUpdates?offset={last_update_id + 1}&timeout=30"
            resp = requests.get(url, timeout=35).json()
            if resp.get("ok"):
                for item in resp.get("result", []):
                    last_update_id = item["update_id"]

                    # 1. Handle incoming text messages
                    if "message" in item:
                        msg = item["message"]
                        chat_id = msg["chat"]["id"]
                        text = msg.get("text", "").strip()

                        # Auto-register chat_id
                        c = load_config()
                        c_ids = c.get("chat_ids", [])
                        if chat_id not in c_ids:
                            c_ids.append(chat_id)
                            c["chat_ids"] = c_ids
                            save_config(c)
                            print(f"[+] Registered Chat ID: {chat_id}")

                        # Special Commands
                        if text == "/start":
                            reply = (
                                f"🏛️ <b>Kính chào Chủ tịch Tập đoàn!</b>\n\n"
                                f"Tôi là <b>Văn phòng Thư ký Tập đoàn</b>, vận hành bởi <b>Antigravity AI (Gemini 3.8 Flash High)</b>.\n\n"
                                f"✨ <b>CHẾ ĐỘ ĐIỀU HÀNH CẤP CAO ĐÃ SẴN SÀNG:</b>\n"

                                f"Chủ tịch có thể chỉ đạo, giao việc hoặc hỏi han tự nhiên trực tiếp trên tin nhắn này.\n\n"
                                f"📌 <i>Tra cứu nhanh:</i>\n"
                                f"• <code>/news</code> — Lịch tin kinh tế USD hôm nay (Giờ VN)\n"
                                f"• <code>/plan</code> — Lập kế hoạch giao dịch XAU/USD\n"
                                f"• <code>/status</code> — Trạng thái thị trường & lệnh\n"
                                f"• <code>/reset</code> — Bắt đầu phiên điều hành mới"
                            )
                            send_msg(chat_id, reply)

                        elif text == "/reset" or text == "/new":
                            use_continue_session = False
                            send_msg(chat_id, "🔄 <b>Đã làm mới phiên hội thoại!</b> Phiên điều hành tiếp theo sẽ bắt đầu với ngữ cảnh mới.")

                        elif text == "/plan":
                            send_msg(chat_id, "⏳ <i>Đang phân tích thị trường XAU/USD (OANDA) từ TradingView và lập kế hoạch...</i>")
                            def run_plan_async(cid):
                                hb = TypingHeartbeat(cid)
                                hb.start()
                                try:
                                    generate_morning_plan()
                                finally:
                                    hb.stop()
                            threading.Thread(target=run_plan_async, args=(chat_id,), daemon=True).start()

                        elif text == "/status":
                            data = get_market_data()
                            c = load_config()
                            plan = c.get("active_plan")
                            trade = c.get("active_trade")
                            price_str = f"{data['price']:.2f}" if data else "N/A"
                            lock_str = "ĐANG KHÓA (Gần giờ tin đỏ)" if c.get("news_lockout") else "Bình thường"

                            status_msg = (
                                f"📊 <b>[TRẠNG THÁI HỆ THỐNG TRADING AGENT]</b>\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"💰 <b>XAU/USD Hiện tại:</b> <code>{price_str}</code>\n"
                                f"📋 <b>Kế hoạch hiện hành:</b> {plan.get('action', '')} tại {plan.get('entry', '')} ({plan.get('status', 'Chưa có')})\n"
                                f"🎯 <b>Lệnh đang mở:</b> {trade.get('action', '') + ' tại ' + str(trade.get('entry_price', '')) if trade else 'Chưa có lệnh nào'}\n"
                                f"🛡️ <b>Trạng thái phòng thủ:</b> {lock_str}\n"
                                f"🧠 <b>AI Core:</b> Antigravity CLI (Gemini 3.8 Flash High)\n"
                                f"⚙️ <b>Hạ tầng:</b> VPS-01 (Ubuntu 24.04 LTS | PM2 24/7)\n"
                                f"━━━━━━━━━━━━━━━━━━"
                            )
                            send_msg(chat_id, status_msg)

                        elif text == "/news":
                            today_news = get_today_news(high_only=False)
                            if not today_news:
                                send_msg(chat_id, "📅 <b>[LỊCH TIN KINH TẾ HÔM NAY]</b>\nKhông có sự kiện USD nào đáng chú ý trong ngày hôm nay.")
                            else:
                                lines = ["📅 <b>[LỊCH TIN KINH TẾ USD HÔM NAY (GMT+7)]</b>", "━━━━━━━━━━━━━━━━━━"]
                                for n in today_news:
                                    icon = "🔴" if n.get("impact") == "High" else ("🟠" if n.get("impact") == "Medium" else "🟡")
                                    t = n.get("time_vn", "")
                                    title = n.get("title", "")
                                    fc = n.get("forecast") or "N/A"
                                    pr = n.get("previous") or "N/A"
                                    lines.append(f"{icon} <b>[{t}]</b> {title}\n    • Dự báo: <code>{fc}</code> | Kỳ trước: <code>{pr}</code>")
                                lines.append("━━━━━━━━━━━━━━━━━━")
                                lines.append("🛡️ <i>Trading Agent tự động trinh sát trước 30p, khóa rủi ro trước 15p và bắt sóng sau 5p.</i>")
                                send_long_msg(chat_id, "\n".join(lines))

                        elif text == "/weekly":
                            def run_weekly_async(cid):
                                hb = TypingHeartbeat(cid)
                                hb.start()
                                try:
                                    generate_weekly_report()
                                finally:
                                    hb.stop()
                            threading.Thread(target=run_weekly_async, args=(chat_id,), daemon=True).start()

                        # ANY OTHER MESSAGE -> NATURAL CHAT DIRECTLY WITH ANTIGRAVITY AI!
                        else:
                            clean_prompt = text
                            if clean_prompt.startswith("/task ") or clean_prompt.startswith("/ai "):
                                clean_prompt = clean_prompt.split(" ", 1)[1].strip()

                            def handle_natural_chat(cid, p):
                                hb = TypingHeartbeat(cid)
                                hb.start()
                                try:
                                    result = run_antigravity_chat(p, continue_session=True)
                                    send_long_msg(cid, result)
                                except Exception as e:
                                    send_msg(cid, f"❌ [Lỗi xử lý]: {e}")
                                finally:
                                    hb.stop()
                            
                            threading.Thread(target=handle_natural_chat, args=(chat_id, clean_prompt), daemon=True).start()

                    # 2. Handle Inline Button Clicks
                    elif "callback_query" in item:
                        cb = item["callback_query"]
                        cb_id = cb["id"]
                        data_val = cb.get("data", "")
                        chat_id = cb["message"]["chat"]["id"]
                        msg_id = cb["message"]["message_id"]

                        c = load_config()
                        current_p = c.get("active_plan")

                        if data_val.startswith("approve_"):
                            plan_id = data_val.replace("approve_", "")
                            if current_p and current_p.get("id") == plan_id:
                                current_p["status"] = "APPROVED"
                                current_p["approved_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                current_p["is_auto_approved"] = False
                                c["active_plan"] = current_p
                                save_config(c)
                                
                                answer_callback(cb_id, "✅ Đã phê duyệt kế hoạch thành công!")
                                edit_msg_reply_markup(chat_id, msg_id, reply_markup=None)

                                confirm_msg = (
                                    f"✅ <b>[XÁC NHẬN PHÊ DUYỆT THÀNH CÔNG]</b>\n"
                                    f"━━━━━━━━━━━━━━━━━━\n"
                                    f"Chủ tịch đã <b>PHÊ DUYỆT</b> kế hoạch <code>{plan_id}</code>:\n"
                                    f"• Lệnh: <b>{current_p['action']} XAU/USD</b>\n"
                                    f"• Điểm vào (Entry): <code>{current_p['entry']:.2f}</code>\n"
                                    f"• Cắt lỗ (SL): <code>{current_p['sl']:.2f}</code>\n"
                                    f"• Chốt lời (TP): <code>{current_p['tp']:.2f}</code>\n"
                                    f"━━━━━━━━━━━━━━━━━━\n"
                                    f"🎯 Trading Agent đang canh nến để đón điểm khớp lệnh tối ưu!"
                                )
                                send_msg(chat_id, confirm_msg)
                            else:
                                answer_callback(cb_id, "Kế hoạch đã được xử lý hoặc không còn hiệu lực.")

                        elif data_val.startswith("cancel_"):
                            plan_id = data_val.replace("cancel_", "")
                            if current_p and current_p.get("id") == plan_id:
                                current_p["status"] = "CANCELLED"
                                c["active_plan"] = None
                                save_config(c)
                                answer_callback(cb_id, "❌ Đã hủy kế hoạch!")
                                edit_msg_reply_markup(chat_id, msg_id, reply_markup=None)
                                send_msg(chat_id, f"❌ <b>Chủ tịch đã HỦY</b> kế hoạch <code>{plan_id}</code>. Hệ thống sẽ không vào lệnh.")
                            else:
                                answer_callback(cb_id, "Kế hoạch không còn hiệu lực!")

        except Exception as e:
            print(f"[!] Poller exception: {e}")
            time.sleep(3)

if __name__ == "__main__":
    telegram_poller()
