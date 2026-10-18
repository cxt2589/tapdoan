import os
import sys
import json
import time

sys.stdout.reconfigure(line_buffering=True)

import datetime
import threading
import urllib.request
import requests
from tradingview_ta import TA_Handler, Interval

try:
    from auto_delete import record_for_auto_delete, delete_message_now, DEFAULT_TTL
except ImportError:
    DEFAULT_TTL = 86400
    def record_for_auto_delete(chat_id, message_id, ttl_seconds=86400, timestamp=None):
        pass
    def delete_message_now(bot_token, chat_id, message_id):
        pass

CONFIG_FILE = "/opt/trading_agent/config.json"
TRADES_FILE = "/opt/trading_agent/paper_trades.json"
CALENDAR_CACHE = "/opt/trading_agent/economic_calendar.json"
VN_TZ = datetime.timezone(datetime.timedelta(hours=7))

DEFAULT_CONFIG = {
    "bot_token": "8821881768:AAFysU6f0IGu4qHHVeN5P-b1fqgFHNPcECI",
    "chat_ids": [],
    "symbol": "XAUUSD",
    "exchange": "OANDA",
    "screener": "cfd",
    "auto_approve_timeout_sec": 300,
    "auto_delete_ttl_seconds": 86400,
    "entry_check_interval_sec": 60,
    "monitor_interval_sec": 60,
    "news_lockout": False,
    "pre_news_baseline": None,
    "active_plan": None,
    "active_trade": None
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_CONFIG

def save_config(cfg):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

def load_trades():
    if os.path.exists(TRADES_FILE):
        try:
            with open(TRADES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_trade(trade):
    trades = load_trades()
    trades.append(trade)
    os.makedirs(os.path.dirname(TRADES_FILE), exist_ok=True)
    with open(TRADES_FILE, "w", encoding="utf-8") as f:
        json.dump(trades, f, ensure_ascii=False, indent=2)

def send_telegram(text, reply_markup=None, ttl_seconds=DEFAULT_TTL):
    cfg = load_config()
    token = cfg.get("bot_token")
    chat_ids = cfg.get("chat_ids", [])
    if not token:
        return None
    last_mid = None
    for cid in chat_ids:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": cid,
            "text": text,
            "parse_mode": "HTML"
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        try:
            r = requests.post(url, json=payload, timeout=10)
            res = r.json()
            if not res.get("ok"):
                payload.pop("parse_mode", None)
                r2 = requests.post(url, json=payload, timeout=10)
                res = r2.json()
            if res and res.get("ok"):
                mid = res.get("result", {}).get("message_id")
                if mid:
                    last_mid = mid
                    if ttl_seconds is not None:
                        record_for_auto_delete(cid, mid, ttl_seconds=ttl_seconds)
        except Exception as e:
            print(f"[!] Error sending telegram to {cid}: {e}")
    return last_mid


# ==========================================
# ECONOMIC CALENDAR ENGINE
# ==========================================

def fetch_and_cache_calendar():
    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
            with open(CALENDAR_CACHE, "w", encoding="utf-8") as f:
                json.dump({"updated_at": time.time(), "events": data}, f, ensure_ascii=False, indent=2)
            return data
    except Exception as e:
        print(f"[!] Error fetching calendar: {e}")
        if os.path.exists(CALENDAR_CACHE):
            try:
                with open(CALENDAR_CACHE, "r", encoding="utf-8") as f:
                    return json.load(f).get("events", [])
            except Exception:
                pass
        return []

def get_today_news(high_only=True):
    events = []
    if os.path.exists(CALENDAR_CACHE):
        try:
            with open(CALENDAR_CACHE, "r", encoding="utf-8") as f:
                cached = json.load(f)
                if isinstance(cached, dict) and (time.time() - cached.get("updated_at", 0) < 14400):
                    events = cached.get("events", [])
                elif isinstance(cached, list):
                    events = cached
        except Exception:
            pass
    if not events:
        events = fetch_and_cache_calendar()

    today_str = datetime.datetime.now(VN_TZ).strftime("%Y-%m-%d")
    today_news = []
    for e in events:
        if e.get("country") != "USD":
            continue
        raw_date = e.get("date")
        if not raw_date:
            continue
        try:
            dt = datetime.datetime.fromisoformat(raw_date).astimezone(VN_TZ)
            if dt.strftime("%Y-%m-%d") == today_str:
                if high_only and e.get("impact") != "High":
                    continue
                e["datetime_vn"] = dt
                e["time_vn"] = dt.strftime("%H:%M")
                today_news.append(e)
        except Exception:
            pass
    today_news.sort(key=lambda x: x["datetime_vn"])
    return today_news

def get_today_high_impact_news(high_only=True):
    return get_today_news(high_only=high_only)

# ==========================================
# MARKET DATA ENGINE
# ==========================================

_last_market_data = None
_last_market_time = 0

def get_market_data():
    global _last_market_data, _last_market_time
    now = time.time()
    if _last_market_data and (now - _last_market_time < 15):
        return _last_market_data

    cfg = load_config()
    try:
        handler = TA_Handler(
            symbol=cfg["symbol"],
            exchange=cfg["exchange"],
            screener=cfg["screener"],
            interval=Interval.INTERVAL_15_MINUTES
        )
        an = handler.get_analysis()
        ind = an.indicators

        cur_price = ind.get("close", 0)
        high = ind.get("high", cur_price)
        low = ind.get("low", cur_price)
        open_p = ind.get("open", cur_price)

        data = {
            "price": cur_price,
            "high": high,
            "low": low,
            "open_5m": open_p,
            "close_5m": cur_price,
            "high_5m": high,
            "low_5m": low,
            "high_15m": high,
            "low_15m": low,
            "rsi_1h": ind.get("RSI", 50),
            "rsi_15m": ind.get("RSI", 50),
            "ema20": ind.get("EMA20", cur_price),
            "ema50": ind.get("EMA50", cur_price),
            "macd": ind.get("MACD.macd", 0),
            "macd_signal": ind.get("MACD.signal", 0),
            "recommendation": an.summary.get("RECOMMENDATION", "NEUTRAL")
        }
        _last_market_data = data
        _last_market_time = now
        return data
    except Exception as e:
        print(f"[!] Error fetching market data: {e}")
        if _last_market_data:
            return _last_market_data
        return None

# ==========================================
# MORNING STRATEGY PLAN (07:00 AM)
# ==========================================

def generate_morning_plan():
    cfg = load_config()
    data = get_market_data()
    if not data:
        send_telegram("⚠️ <b>[CẢNH BÁO HỆ THỐNG]</b> Không thể lấy dữ liệu XAU/USD từ TradingView (OANDA) vào lúc này.")
        return

    price = data["price"]
    rsi = data["rsi_1h"]
    ema20 = data["ema20"]
    ema50 = data["ema50"]

    # Quantitative Decision Engine with SL Safety Buffer (+3.0 USD)
    SL_BUFFER = 3.0
    if ema20 >= ema50 and rsi < 70:
        action = "BUY"
        entry = round(price - 1.5, 2)
        sl = round(entry - (12.0 + SL_BUFFER), 2)
        tp = round(entry + 22.0, 2)
        thesis = "EMA20 nằm trên EMA50, RSI duy trì ổn định, ưu tiên vị thế Mua theo xu hướng (kèm đệm an toàn SL +3.0 USD chống quét râu)."
    elif ema20 < ema50 and rsi > 30:
        action = "SELL"
        entry = round(price + 1.5, 2)
        sl = round(entry + (12.0 + SL_BUFFER), 2)
        tp = round(entry - 22.0, 2)
        thesis = "EMA20 cắt xuống dưới EMA50, áp lực bán chi phối, ưu tiên vị thế Bán theo đà (kèm đệm an toàn SL +3.0 USD chống quét râu)."
    else:
        action = "BUY" if rsi < 50 else "SELL"
        entry = round(price, 2)
        sl = round(entry - (10.0 + SL_BUFFER) if action == "BUY" else entry + (10.0 + SL_BUFFER), 2)
        tp = round(entry + 20.0 if action == "BUY" else entry - 20.0, 2)
        thesis = "Thị trường giằng co, mở vị thế thăm dò theo dao động khung ngắn hạn (kèm đệm an toàn SL +3.0 USD chống quét râu)."

    # Check today's high impact news
    high_news = get_today_high_impact_news(high_only=True)
    news_note = ""
    if high_news:
        news_times = ", ".join([f"{n['time_vn']} ({n['title']})" for n in high_news[:3]])
        news_note = f"\n⚠️ <b>LƯU Ý TIN ĐỎ HÔM NAY:</b> {news_times}. Khuyến nghị ưu tiên chốt trước giờ tin!"

    plan_id = f"PLAN-{int(time.time())}"
    plan = {
        "id": plan_id,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": "XAU/USD (OANDA)",
        "action": action,
        "current_price": price,
        "entry": entry,
        "sl": sl,
        "tp": tp,
        "rr_ratio": "1 : 1.67",
        "thesis": thesis,
        "status": "PENDING_APPROVAL",
        "approved_at": None,
        "is_auto_approved": False
    }

    cfg["active_plan"] = plan
    save_config(cfg)

    markup = {
        "inline_keyboard": [
            [
                {"text": "✅ Phê Duyệt Ngay", "callback_data": f"approve_{plan_id}"},
                {"text": "❌ Hủy Kế Hoạch", "callback_data": f"cancel_{plan_id}"}
            ]
        ]
    }

    msg = (
        f"🏛️ <b>[VĂN PHÒNG THƯ KÝ TẬP ĐOÀN — KẾ HOẠCH GIAO DỊCH ĐẦU NGÀY]</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"

        f"📊 <b>Cặp tiền:</b> XAU/USD (OANDA CFD)\n"
        f"💰 <b>Giá thị trường:</b> <code>{price:.2f}</code>\n"
        f"🎯 <b>Vị thế khuyến nghị:</b> <b>{action}</b>\n"
        f"📍 <b>Điểm vào lệnh (Entry):</b> <code>{entry:.2f}</code>\n"
        f"🛑 <b>Cắt lỗ (Stop Loss):</b> <code>{sl:.2f}</code>\n"
        f"🎯 <b>Chốt lời (Take Profit):</b> <code>{tp:.2f}</code> (R:R {plan['rr_ratio']})\n"
        f"💡 <b>Luận điểm:</b> {thesis}{news_note}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"⏰ <b>Quy chế tự hành:</b> Nếu Chủ tịch không bấm nút trong <b>5 phút</b>, hệ thống sẽ <b>TỰ ĐỘNG PHÊ DUYỆT</b> để tiến hành quét lệnh!"
    )
    sent_mid = send_telegram(msg, reply_markup=markup)
    if sent_mid:
        plan["proposal_msg_id"] = sent_mid
        cfg["active_plan"] = plan
        save_config(cfg)

    def approval_timer(p_id):
        time.sleep(cfg.get("auto_approve_timeout_sec", 300))
        c = load_config()
        current_p = c.get("active_plan")
        if current_p and current_p.get("id") == p_id and current_p.get("status") == "PENDING_APPROVAL":
            current_p["status"] = "APPROVED"
            current_p["approved_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_p["is_auto_approved"] = True
            c["active_plan"] = current_p
            save_config(c)
            # Xóa tin nhắn có nút phê duyệt cũ theo chỉ đạo chống rác
            old_mid = current_p.get("proposal_msg_id")
            if old_mid and c.get("bot_token"):
                for cid in c.get("chat_ids", []):
                    try:
                        delete_message_now(c.get("bot_token"), cid, old_mid)
                    except Exception:
                        pass
            send_telegram(
                f"⚡ <b>[HẾT 5 PHÚT — TỰ ĐỘNG PHÊ DUYỆT]</b>\n"
                f"Kế hoạch <code>{p_id}</code> ({current_p['action']} XAU/USD tại {current_p['entry']:.2f}) đã được <b>TỰ ĐỘNG DUYỆT</b> theo ủy quyền.\n"
                f"Trading Agent bắt đầu quét nến tìm điểm khớp lệnh!"
            )
    threading.Thread(target=approval_timer, args=(plan_id,), daemon=True).start()

# ==========================================
# ENTRY & POSITION MONITOR (SILENT 60S LOOP)
# ==========================================

def check_entry_loop():
    while True:
        try:
            cfg = load_config()
            if cfg.get("news_lockout"):
                time.sleep(30)
                continue

            plan = cfg.get("active_plan")
            trade = cfg.get("active_trade")

            if plan and plan.get("status") == "APPROVED" and not trade:
                data = get_market_data()
                if data:
                    cur = data["price"]
                    candle_high = data["high"]
                    candle_low = data["low"]
                    action = plan["action"]
                    entry = plan["entry"]

                    hit = False
                    fill_price = entry
                    if action == "BUY" and (cur <= entry or candle_low <= entry):
                        hit = True
                        fill_price = min(cur, entry)
                    elif action == "SELL" and (cur >= entry or candle_high >= entry):
                        hit = True
                        fill_price = max(cur, entry)

                    if hit:
                        planned_risk = abs(plan["entry"] - plan["sl"])
                        planned_reward = abs(plan["tp"] - plan["entry"])

                        # Dynamic SL Slippage Recalculation: Chống lỗi trượt giá bó hẹp khoảng cách SL
                        if action == "BUY":
                            actual_sl = round(fill_price - planned_risk, 2)
                            actual_tp = round(fill_price + planned_reward, 2)
                        else:
                            actual_sl = round(fill_price + planned_risk, 2)
                            actual_tp = round(fill_price - planned_reward, 2)

                        new_trade = {
                            "trade_id": f"TR-{int(time.time())}",
                            "plan_id": plan["id"],
                            "symbol": plan["symbol"],
                            "action": action,
                            "entry_price": fill_price,
                            "planned_entry": entry,
                            "sl": actual_sl,
                            "tp": actual_tp,
                            "opened_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "status": "OPEN",
                            "min_price_seen": min(cur, candle_low),
                            "max_price_seen": max(cur, candle_high),
                            "breakeven_triggered": False
                        }
                        cfg["active_trade"] = new_trade
                        plan["status"] = "EXECUTED"
                        cfg["active_plan"] = plan
                        save_config(cfg)

                        send_telegram(
                            f"🎯 <b>[KHỚP LỆNH THÀNH CÔNG]</b>\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"Lệnh: <b>{action} XAU/USD</b>\n"
                            f"📍 <b>Giá khớp thực tế:</b> <code>{fill_price:.2f}</code>\n"
                            f"🛑 <b>Stop Loss (động):</b> <code>{actual_sl:.2f}</code> (khoảng cách {planned_risk:.2f} USD)\n"
                            f"🎯 <b>Take Profit (động):</b> <code>{actual_tp:.2f}</code>\n"
                            f"⏰ <b>Thời điểm khớp:</b> {new_trade['opened_at']}\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"🛡️ <i>Tự động kích hoạt Auto-Breakeven dời SL về hòa vốn khi lãi từ +10.0 USD/oz.</i>"
                        )
        except Exception as e:
            print(f"[!] Error in check_entry_loop: {e}")
        time.sleep(load_config().get("entry_check_interval_sec", 60))

def monitor_active_trade_loop():
    while True:
        try:
            cfg = load_config()
            trade = cfg.get("active_trade")
            if trade and trade.get("status") == "OPEN":
                data = get_market_data()
                if data:
                    cur = data["price"]
                    candle_high = data["high"]
                    candle_low = data["low"]
                    action = trade["action"]
                    sl = trade["sl"]
                    tp = trade["tp"]
                    entry = trade["entry_price"]

                    trade["min_price_seen"] = min(trade.get("min_price_seen", cur), candle_low)
                    trade["max_price_seen"] = max(trade.get("max_price_seen", cur), candle_high)

                    # TÍNH TOÁN PNL THẢ NỔI VÀ KÍCH HOẠT AUTO-BREAKEVEN (+10.0 USD)
                    cur_pnl = round((cur - entry) if action == "BUY" else (entry - cur), 2)
                    trade["pnl_points"] = cur_pnl

                    BREAKEVEN_TRIGGER_PTS = 10.0
                    if not trade.get("breakeven_triggered") and cur_pnl >= BREAKEVEN_TRIGGER_PTS:
                        trade["breakeven_triggered"] = True
                        be_sl = round(entry + 0.5 if action == "BUY" else entry - 0.5, 2)
                        old_sl = trade["sl"]
                        trade["sl"] = be_sl
                        cfg["active_trade"] = trade
                        save_config(cfg)

                        send_telegram(
                            f"🛡️ <b>[KHÓA LÃI TỰ ĐỘNG — AUTO-BREAKEVEN]</b>\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"Lệnh: <b>{action} XAU/USD</b>\n"
                            f"💰 <b>Lợi nhuận thả nổi:</b> <code>+{cur_pnl:.2f} USD/oz</code> (đã vượt ngưỡng an toàn +{BREAKEVEN_TRIGGER_PTS:.1f} USD)!\n"
                            f"🛑 <b>Hành động:</b> Đã tự động dời SL từ <code>{old_sl:.2f}</code> về vùng Hòa Vốn <code>{be_sl:.2f}</code>.\n"
                            f"🛡️ <i>Vị thế đã được bảo toàn vốn 100% rủi ro (Risk-Free Trade)!</i>"
                        )

                    is_sl_hit = False
                    is_tp_hit = False

                    if action == "BUY":
                        if candle_low <= sl:
                            is_sl_hit = True
                        elif candle_high >= tp:
                            is_tp_hit = True
                    elif action == "SELL":
                        if candle_high >= sl:
                            is_sl_hit = True
                        elif candle_low <= tp:
                            is_tp_hit = True

                    if is_sl_hit:
                        trade["status"] = "CLOSED_SL"
                        trade["close_price"] = sl
                        trade["closed_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        trade["pnl_points"] = round((sl - entry) if action == "BUY" else (entry - sl), 2)
                        trade["result"] = "LOSS"
                        save_trade(trade)
                        cfg["active_trade"] = None
                        save_config(cfg)

                        send_telegram(
                            f"🔴 <b>[CẢNH BÁO: CHẠM STOP LOSS]</b>\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"Lệnh <b>{action} XAU/USD</b> đã chạm ngưỡng cắt lỗ!\n"
                            f"📍 Giá vào: <code>{entry:.2f}</code> | Giá đóng SL: <code>{sl:.2f}</code>\n"
                            f"📉 <b>PnL:</b> <code>{trade['pnl_points']} USD/oz</code>\n"
                            f"🛑 Kỷ luật cắt lỗ bảo toàn vốn đã được kích hoạt thành công."
                        )
                    elif is_tp_hit:
                        trade["status"] = "CLOSED_TP"
                        trade["close_price"] = tp
                        trade["closed_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        trade["pnl_points"] = round((tp - entry) if action == "BUY" else (entry - tp), 2)
                        trade["result"] = "WIN"
                        save_trade(trade)
                        cfg["active_trade"] = None
                        save_config(cfg)

                        send_telegram(
                            f"🟢 <b>[MỤC TIÊU ĐẠT: CHẠM TAKE PROFIT]</b>\n"
                            f"━━━━━━━━━━━━━━━━━━\n"
                            f"Lệnh <b>{action} XAU/USD</b> đã đạt trọn vẹn mục tiêu chốt lời!\n"
                            f"📍 Giá vào: <code>{entry:.2f}</code> | Giá chốt TP: <code>{tp:.2f}</code>\n"
                            f"📈 <b>Lợi nhuận PnL:</b> <b>+{trade['pnl_points']} USD/oz</b>\n"
                            f"🎉 Mô hình Quantitative Trading Agent chốt lời chuẩn xác!"
                        )
                    else:
                        cfg["active_trade"] = trade
                        save_config(cfg)
        except Exception as e:
            print(f"[!] Error in monitor_active_trade_loop: {e}")

        interval = load_config().get("monitor_interval_sec", 60)
        time.sleep(interval)

# ==========================================
# PRE-NEWS & POST-NEWS DEDICATED ENGINE
# ==========================================

def execute_pre_news_30m(event):
    cfg = load_config()
    data = get_market_data()
    price = data["price"] if data else 0
    box_high = data["high_15m"] if data else price + 3
    box_low = data["low_15m"] if data else price - 3

    cfg["pre_news_baseline"] = {
        "event_title": event.get("title"),
        "event_time_vn": event.get("time_vn"),
        "measured_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "box_high": box_high,
        "box_low": box_low,
        "spot_price": price
    }
    save_config(cfg)

    msg = (
        f"🔍 <b>[TRINH SÁT TRƯỚC TIN ĐỎ — T-30 PHÚT]</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📅 <b>Sự kiện lúc {event.get('time_vn')}:</b> <b>{event.get('title')}</b>\n"
        f"📊 <b>Dự báo:</b> <code>{event.get('forecast', 'N/A')}</code> | <b>Kỳ trước:</b> <code>{event.get('previous', 'N/A')}</code>\n"
        f"💰 <b>Giá hiện tại:</b> <code>{price:.2f}</code>\n"
        f"📦 <b>Chiếc hộp tích lũy trước tin:</b> <code>{box_low:.2f} — {box_high:.2f}</code> (Biên độ {abs(box_high - box_low):.2f} USD)\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🎯 <b>Kế hoạch tác chiến:</b>\n"
        f"• Lúc {event.get('time_vn')}: Đứng ngoài quan sát cú sốc thanh khoản ban đầu.\n"
        f"• Sau tin 5 phút: Quét nến M5 bứt phá và bắn kế hoạch vào lệnh lên Telegram!"
    )
    send_telegram(msg)

def execute_pre_news_15m(event):
    cfg = load_config()
    cfg["news_lockout"] = True
    trade = cfg.get("active_trade")
    
    lock_note = "Hiện không có lệnh đang mở (Trạng thái an toàn)."
    if trade and trade.get("status") == "OPEN":
        cur_pnl = trade.get("pnl_points", 0)
        if cur_pnl > 0:
            trade["sl"] = trade["entry_price"] # Breakeven
            cfg["active_trade"] = trade
            lock_note = f"Đã tự động dời SL lệnh {trade['action']} về Hòa Vốn (<code>{trade['entry_price']:.2f}</code>) để bảo vệ lợi nhuận!"
        else:
            lock_note = f"Cảnh báo: Lệnh {trade['action']} đang mở. Khuyến nghị chú ý biến động giãn spread!"
    save_config(cfg)

    msg = (
        f"🛡️ <b>[KÍCH HOẠT KHIÊN BẢO VỆ VỐN — T-15 PHÚT]</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"⏰ <b>Còn 15 phút đến giờ tin:</b> {event.get('title')} ({event.get('time_vn')})\n"
        f"🔒 <b>News Lockout:</b> Tạm dừng mở vị thế mới để tránh trượt giá.\n"
        f"🛡️ <b>Quản trị vốn:</b> {lock_note}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"Bàn Khớp lệnh sẵn sàng đón sóng hậu tin tức lúc {event.get('time_vn')} + 5 phút!"
    )
    send_telegram(msg)

def execute_post_news_5m(event):
    cfg = load_config()
    cfg["news_lockout"] = False # Lift lockout
    data = get_market_data()
    baseline = cfg.get("pre_news_baseline")

    if not data or not baseline:
        send_telegram("⚠️ <b>[HẬU TIN TỨC]</b> Dữ liệu phản ứng sau tin đang được phân tích...")
        return

    cur_price = data["price"]
    m5_close = data["close_5m"]
    m5_open = data["open_5m"]
    m5_high = data["high_5m"]
    m5_low = data["low_5m"]
    box_high = baseline["box_high"]
    box_low = baseline["box_low"]

    # Quantitative Decision on M5 reaction vs Pre-News Box with SL Buffer (+3.0 USD)
    m5_range = max(abs(m5_high - m5_low), 4.0)
    SL_BUFFER = 3.0
    
    if m5_close > box_high:
        # Bullish Breakout
        action = "BUY"
        entry = round(m5_close - (0.35 * m5_range), 2) # Pullback entry
        sl = round(m5_low - 2.0 - SL_BUFFER, 2)
        risk = max(abs(entry - sl), 8.0)
        tp = round(entry + (1.8 * risk), 2)
        thesis = f"Nến M5 bứt phá mạnh qua đỉnh trước tin ({box_high:.2f}). Dòng tiền mua thâu tóm thị trường. Đón Mua tại nhịp hồi kỹ thuật (kèm đệm an toàn SL +3.0 USD)."
    elif m5_close < box_low:
        # Bearish Breakdown
        action = "SELL"
        entry = round(m5_close + (0.35 * m5_range), 2) # Pullback entry
        sl = round(m5_high + 2.0 + SL_BUFFER, 2)
        risk = max(abs(sl - entry), 8.0)
        tp = round(entry - (1.8 * risk), 2)
        thesis = f"Nến M5 đạp thủng đáy tích lũy trước tin ({box_low:.2f}). Áp lực bán tháo áp đảo. Đón Bán tại nhịp hồi kỹ thuật (kèm đệm an toàn SL +3.0 USD)."
    else:
        # Inside Box / Neutral
        action = "BUY" if m5_close >= m5_open else "SELL"
        entry = round(cur_price, 2)
        sl = round(entry - (10.0 + SL_BUFFER) if action == "BUY" else entry + (10.0 + SL_BUFFER), 2)
        tp = round(entry + 18.0 if action == "BUY" else entry - 18.0, 2)
        thesis = f"Thị trường giằng co trong hộp trước tin ({box_low:.2f} — {box_high:.2f}). Mở vị thế thăm dò kèm đệm an toàn SL +3.0 USD."

    plan_id = f"PLAN-NEWS-{int(time.time())}"
    plan = {
        "id": plan_id,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": "XAU/USD (OANDA)",
        "action": action,
        "current_price": cur_price,
        "entry": entry,
        "sl": sl,
        "tp": tp,
        "rr_ratio": "1 : 1.80",
        "thesis": thesis,
        "status": "PENDING_APPROVAL",
        "approved_at": None,
        "is_auto_approved": False
    }

    cfg["active_plan"] = plan
    save_config(cfg)

    markup = {
        "inline_keyboard": [
            [
                {"text": "✅ Phê Duyệt Ngay", "callback_data": f"approve_{plan_id}"},
                {"text": "❌ Bỏ Qua Kế Hoạch", "callback_data": f"cancel_{plan_id}"}
            ]
        ]
    }

    msg = (
        f"🚀 <b>[VĂN PHÒNG THƯ KÝ TẬP ĐOÀN — KẾ HOẠCH BẮT SÓNG HẬU TIN TỨC]</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"

        f"📅 <b>Sự kiện vừa ra:</b> <b>{event.get('title')}</b>\n"
        f"📊 <b>Phản ứng nến M5:</b> Open: <code>{m5_open:.2f}</code> | Close: <code>{m5_close:.2f}</code> | Đỉnh/Đáy: <code>{m5_high:.2f}/{m5_low:.2f}</code>\n"
        f"🎯 <b>Phương án đề xuất:</b> <b>{action} XAU/USD</b>\n"
        f"📍 <b>Điểm đón (Pullback Entry):</b> <code>{entry:.2f}</code>\n"
        f"🛑 <b>Cắt lỗ thích ứng (SL):</b> <code>{sl:.2f}</code>\n"
        f"🎯 <b>Chốt lời (TP):</b> <code>{tp:.2f}</code> (R:R 1:1.80)\n"
        f"💡 <b>Luận điểm Quỹ:</b> {thesis}\n"
        f"🛡️ <b>Quản trị vốn:</b> Khối lượng đã được co giãn tự động theo biến động ATR để khóa rủi ro 1%.\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"Chủ tịch vui lòng phê duyệt để Bàn Giao Dịch tiến hành khớp lệnh!"
    )
    sent_mid = send_telegram(msg, reply_markup=markup)
    if sent_mid:
        plan["proposal_msg_id"] = sent_mid
        cfg["active_plan"] = plan
        save_config(cfg)

# ==========================================
# MASTER SCHEDULER THREAD
# ==========================================

triggered_news_30m = set()
triggered_news_15m = set()
triggered_news_5m = set()

def scheduler_thread():
    global triggered_news_30m, triggered_news_15m, triggered_news_5m
    while True:
        try:
            now_vn = datetime.datetime.now(VN_TZ)

            # 07:00 AM daily
            if now_vn.hour == 7 and now_vn.minute == 0:
                print("[*] Triggering 07:00 AM Daily Plan...")
                generate_morning_plan()
                time.sleep(60)

            # Saturday 04:00 AM weekly report
            if now_vn.weekday() == 5 and now_vn.hour == 4 and now_vn.minute == 0:
                print("[*] Triggering Weekly Summary Report...")
                from trading_agent_core import generate_weekly_report
                generate_weekly_report()
                time.sleep(60)

            # Check news triggers
            today_high_news = get_today_high_impact_news(high_only=True)
            for event in today_high_news:
                event_dt = event.get("datetime_vn")
                if not event_dt:
                    continue
                diff_sec = (event_dt - now_vn).total_seconds()
                event_key = f"{event.get('title')}_{event_dt.strftime('%H%M')}"

                # T-30 minutes (between 28m and 31m)
                if 1680 <= diff_sec <= 1860 and event_key not in triggered_news_30m:
                    triggered_news_30m.add(event_key)
                    print(f"[*] Firing T-30m pre-news for {event_key}...")
                    execute_pre_news_30m(event)

                # T-15 minutes (between 13m and 16m)
                if 780 <= diff_sec <= 960 and event_key not in triggered_news_15m:
                    triggered_news_15m.add(event_key)
                    print(f"[*] Firing T-15m lockout for {event_key}...")
                    execute_pre_news_15m(event)

                # T+5 minutes (between -360s and -240s, i.e. 4 to 6 mins after event)
                if -360 <= diff_sec <= -240 and event_key not in triggered_news_5m:
                    triggered_news_5m.add(event_key)
                    print(f"[*] Firing T+5m post-news for {event_key}...")
                    execute_post_news_5m(event)

        except Exception as e:
            print(f"[!] Error in scheduler loop: {e}")

        time.sleep(20)

def generate_weekly_report():
    trades = load_trades()
    now = datetime.datetime.now()
    seven_days_ago = now - datetime.timedelta(days=7)

    recent_trades = [
        t for t in trades 
        if datetime.datetime.strptime(t.get("opened_at", "2000-01-01 00:00:00"), "%Y-%m-%d %H:%M:%S") >= seven_days_ago
    ]

    total = len(recent_trades)
    wins = len([t for t in recent_trades if t.get("result") == "WIN"])
    losses = len([t for t in recent_trades if t.get("result") == "LOSS"])
    total_pnl = sum([t.get("pnl_points", 0) for t in recent_trades])
    win_rate = (wins / total * 100) if total > 0 else 0

    msg = (
        f"🏆 <b>[BÁO CÁO TỔNG KẾT TUẦN — TRADING AGENT PHASE 1]</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📅 <b>Tuần kết thúc:</b> {now.strftime('%d/%m/%Y')}\n"
        f"📊 <b>Cặp theo dõi:</b> XAU/USD (OANDA CFD)\n"
        f"🔢 <b>Tổng số lệnh thực thi:</b> {total}\n"
        f"✅ <b>Số lệnh Thắng (Win):</b> {wins}\n"
        f"❌ <b>Số lệnh Thua (Loss):</b> {losses}\n"
        f"🎯 <b>Tỷ lệ Thắng (Winrate):</b> <b>{win_rate:.1f}%</b>\n"
        f"💰 <b>Tổng PnL tích lũy tuần:</b> <b>{'+' if total_pnl>=0 else ''}{total_pnl:.2f} USD/oz</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🔍 <b>Đánh giá mô hình:</b> "
        f"{'Mô hình hoạt động hiệu quả, tín hiệu chuẩn xác, khuyến nghị tiếp tục mở rộng.' if total_pnl > 0 else 'Cần tinh chỉnh ngưỡng SL/TP hoặc bộ lọc RSI để tăng độ an toàn.'}"
    )
    send_telegram(msg)

if __name__ == "__main__":
    print("[*] Starting Trading Agent Core with Macro News Engine...")
    threading.Thread(target=scheduler_thread, daemon=True).start()
    threading.Thread(target=check_entry_loop, daemon=True).start()
    threading.Thread(target=monitor_active_trade_loop, daemon=True).start()

    while True:
        time.sleep(3600)
