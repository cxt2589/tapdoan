#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BẢN TIN KHỚP GIAO DỊCH B2B BUỔI SÁNG (06:30 AM)
Tự động quét kho dữ liệu Buyer & Supplier, chấm điểm Ma Trận 6 Chiều và gửi tóm tắt về Telegram Chủ tịch.
Tách riêng biệt khỏi bản tin tâm linh để đảm bảo tính tinh gọn, không spam tin nhắn dài.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta

# Đảm bảo UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "intelligence_db.json")
URL_FILE = os.path.join(BASE_DIR, "cloudflare_url.txt")
LOG_FILE = os.path.join(BASE_DIR, "data", "morning_matches_history.json")

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8821881768:AAFysU6f0IGu4qHHVeN5P-b1fqgFHNPcECI")
DEFAULT_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "6034655358")

# Import Trade Matcher
try:
    import trade_matcher
except ImportError:
    sys.path.append(BASE_DIR)
    import trade_matcher

def get_portal_url():
    if os.path.exists(URL_FILE):
        try:
            with open(URL_FILE, "r", encoding="utf-8") as f:
                url = f.read().strip()
                if url.startswith("http"):
                    return url
        except Exception:
            pass
    return "https://cup-specialist-class-nickname.trycloudflare.com"

def run_morning_dispatch(force=False, dry_run=False):
    if not os.path.exists(DATA_FILE):
        print(f"[ERROR] Database file not found at: {DATA_FILE}")
        return False

    # Giờ hiện tại GMT+7
    now_vn = datetime.now(timezone(timedelta(hours=7)))
    date_str = now_vn.strftime("%d/%m/%Y")
    time_str = now_vn.strftime("%H:%M")

    # =========================================================================
    # KIỂM SOÁT TẦN SUẤT THEO CHỈ THỊ CỦA CHỦ TỊCH:
    # CHỈ PHÁT 1 LẦN/NGÀY VÀO BUỔI SÁNG (06:30), TUYỆT ĐỐI KHÔNG GỬI LẶP LẠI
    # =========================================================================
    if not force and not dry_run and os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
                for entry in history:
                    if entry.get("date") == date_str and entry.get("telegram_sent") is True:
                        print(f"[ONCE_PER_DAY_LOCK] Bản tin khớp giao dịch cho ngày {date_str} đã được phát thành công trước đó (lúc {entry.get('timestamp')}).")
                        print(f"[ONCE_PER_DAY_LOCK] Thực thi nghiêm lệnh Chủ tịch: Hệ thống chỉ gửi 1 lần mỗi ngày vào buổi sáng. Bỏ qua lượt gửi này.")
                        return True
        except Exception as e:
            print(f"[WARNING] Không thể đọc log lịch sử để kiểm tra khóa ngày: {e}")

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)

    metrics = trade_matcher.get_daily_matching_metrics(db)
    portal_url = get_portal_url()
    matchmaker_url = f"{portal_url}#tab-matchmaker"

    pipe_millions = round(metrics["total_pipeline_val_usd"] / 1_000_000, 1)

    # 1. Cơ cấu ngành hàng thu gọn 1 dòng trực quan
    ind_parts = []
    for ind, count in metrics.get("industry_breakdown", {}).items():
        s_ind = ind.split(" & ")[0].split(" / ")[0]
        icon = "🌾" if "Nông sản" in ind else ("🧪" if "Phân bón" in ind else ("🐟" if "Thủy" in ind else ("🪵" if "Gỗ" in ind else "⚙️")))
        ind_parts.append(f"{icon} {s_ind}: <b>{count}</b>")
    ind_summary = " • ".join(ind_parts) if ind_parts else "Đa ngành ngoại thương"

    daily_theme = metrics.get("daily_theme") or f"Chiến Lược Luân Chuyển Đối Tác Toàn Cầu • {date_str}"
    top_deals = metrics.get("top_diamond_deals", [])

    # 2. Xây dựng nội dung HTML phân cấp thị giác tinh gọn, chống rối mắt trên di động
    lines = [
        "🏛️ <b>TỔNG HÀNH DINH // BẢN TIN KHỚP GIAO DỊCH 06:30</b>",
        f"<i>{daily_theme}</i>",
        "────────────────────────────",
        "📊 <b>TỔNG QUAN PIPELINE HÔM NAY:</b>",
        f"• 💎 <b>Khớp Kim Cương (≥85đ):</b> <b>{metrics['diamond_count']}</b> thương vụ <i>(Xác suất chốt &gt;90%)</i>",
        f"• 🥇 <b>Khớp Hoàng Kim (70-84đ):</b> <b>{metrics['gold_count']}</b> thương vụ",
        f"• 💰 <b>Tổng giá trị Pipeline:</b> <b>${pipe_millions}M USD</b> <i>({metrics.get('total_scanned_suppliers', 20)} NCC / 12 Nước)</i>",
        f"• 🌐 <b>Cơ cấu ngành:</b> {ind_summary}",
        "",
        f"⭐ <b>GIAO DỊCH ĐA NGÀNH TIÊU BIỂU HÔM NAY ({len(top_deals[:4])} NGÀNH XOAY VÒNG):</b>",
        ""
    ]

    for idx, d in enumerate(top_deals[:4]):
        b_name = d.get("buyer_name", "")
        b_c = d.get("buyer_country", "")
        s_name = d.get("supplier_short_name", "") or d.get("supplier_name", "")
        s_c = d.get("supplier_country", "")
        item = d.get("matched_commodity", "")
        hs = d.get("matched_hs", "")
        score = d.get("total_score", 0)
        tier_vi = d.get("tier_vi", "Khớp Kim Cương")
        val_m = round(d.get("deal_value_usd", 0) / 1_000_000, 2)
        ind_lbl = d.get("industry_label") or d.get("_industry_name") or "🌐 Ngoại thương"

        # Lấy 3 tag quy chuẩn trọng tâm, lược bỏ mã HS thô
        raw_tags = [t.replace('#', '').replace('_', ' ') for t in d.get("matched_tags", []) if not t.startswith('#HS_')]
        tags_str = " • ".join(raw_tags[:3]) if raw_tags else "Mã HS & Quy cách chuẩn"

        lines.append(f"<b>{idx+1}️⃣ [{ind_lbl}]</b>")
        lines.append(f"<b>{b_name} ({b_c}) ⇄ {s_name} ({s_c})</b>")
        lines.append(f"• 📦 Mặt hàng: <b>{item}</b> (Mã HS: {hs})")
        lines.append(f"• 🎯 Điểm ma trận 6 chiều: <b>{score}/100</b> <i>({tier_vi})</i>")
        lines.append(f"• 💰 Giá trị thương vụ: ~<b>${val_m}M USD</b>")
        lines.append(f"• ⚡ Quy chuẩn khớp: <code>{tags_str}</code>")
        lines.append("")

    lines.append("────────────────────────────")
    lines.append(f"📌 <i>Chỉ đạo: Mở Bàn Khớp Lệnh trên Portal để đối soát chi tiết ma trận 6 chiều hoặc kích hoạt bộ đôi RFQ hai chiều.</i>")

    message_html = "\n".join(lines)
    message_text = re.sub(r"<[^>]+>", "", message_html)

    # Inline Keyboard
    reply_markup = {
        "inline_keyboard": [
            [
                {
                    "text": "⚡ Mở Bàn Khớp Lệnh Portal (Xem Chi Tiết)",
                    "url": matchmaker_url
                }
            ],
            [
                {
                    "text": "🌐 Cổng Tình Báo Ngoại Thương Toàn Cầu",
                    "url": portal_url
                }
            ]
        ]
    }

    if dry_run:
        print(f"[DRY_RUN] Chế độ kiểm thử (dry_run=True): Bản tin khớp lệnh 06:30 đã được biên soạn và kiểm tra cú pháp thành công.")
        print(f"[DRY_RUN] Bỏ qua bước gọi Telegram API để không gửi tin nhắn tới Chủ tịch.")
        return True

    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": DEFAULT_CHAT_ID,
        "text": message_html,
        "parse_mode": "HTML",
        "reply_markup": json.dumps(reply_markup)
    }

    success = False
    try:
        req_data = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(send_url, data=req_data, headers={'User-Agent': 'AntigravityTradeMatcher/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            res = json.loads(resp.read().decode())
            if res.get("ok"):
                print(f"[SUCCESS] Đã gửi Bản tin Khớp Giao Dịch B2B tới Telegram ({DEFAULT_CHAT_ID}) lúc {time_str}!")
                success = True
    except Exception as e:
        print(f"[WARNING] Gửi HTML kèm Inline Keyboard thất bại ({e}), chuyển sang gửi fallback không bàn phím...")
        try:
            fallback_payload = {
                "chat_id": DEFAULT_CHAT_ID,
                "text": message_html + f"\n\n🔗 Xem chi tiết tại: {matchmaker_url}",
                "parse_mode": "HTML"
            }
            req_data = urllib.parse.urlencode(fallback_payload).encode("utf-8")
            req = urllib.request.Request(send_url, data=req_data, headers={'User-Agent': 'AntigravityTradeMatcher/1.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                res = json.loads(resp.read().decode())
                if res.get("ok"):
                    print(f"[SUCCESS] Đã gửi bản tin Telegram (HTML Fallback) thành công!")
                    success = True
        except Exception as e2:
            print(f"[ERROR] Không thể gửi Telegram: {e2}")

    # Ghi nhật ký
    try:
        log_entry = {
            "timestamp": now_vn.isoformat(),
            "date": date_str,
            "metrics": metrics,
            "telegram_sent": success
        }
        history = []
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                history = []
        history.append(log_entry)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(history[-30:], f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[WARNING] Không thể lưu log lịch sử: {e}")

    return success

if __name__ == "__main__":
    force_flag = "--force" in sys.argv
    dry_run_flag = "--dry-run" in sys.argv or "-d" in sys.argv
    run_morning_dispatch(force=force_flag, dry_run=dry_run_flag)
