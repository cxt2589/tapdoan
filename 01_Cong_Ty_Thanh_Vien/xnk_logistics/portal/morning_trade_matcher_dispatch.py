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

def run_morning_dispatch():
    if not os.path.exists(DATA_FILE):
        print(f"[ERROR] Database file not found at: {DATA_FILE}")
        return False

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)

    metrics = trade_matcher.get_daily_matching_metrics(db)
    portal_url = get_portal_url()
    matchmaker_url = f"{portal_url}#tab-matchmaker"

    # Giờ hiện tại GMT+7
    now_vn = datetime.now(timezone(timedelta(hours=7)))
    date_str = now_vn.strftime("%d/%m/%Y")
    time_str = now_vn.strftime("%H:%M")

    pipe_millions = round(metrics["total_pipeline_val_usd"] / 1_000_000, 1)

    # Xây dựng nội dung HTML tinh gọn
    lines = [
        f"🏛️ <b>TỔNG HÀNH DINH — TÌNH BÁO KHỚP GIAO DỊCH B2B</b>",
        f"<i>Bản tin thường nhật 06:30 | Ngày {date_str}</i>",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "🎯 <b>TỔNG QUAN KHỚP LỆNH HÔM NAY:</b>",
        f"• 💎 <b>Khớp Kim Cương (≥85đ):</b> <b>{metrics['diamond_count']} thương vụ</b> <i>(Xác suất chốt &gt;90%)</i>",
        f"• 🥇 <b>Khớp Hoàng Kim (70-84đ):</b> <b>{metrics['gold_count']} thương vụ</b> <i>(Khả quan)</i>",
        f"• 🏭 <b>Nhà Cung Cấp Kết Nối:</b> <b>{metrics.get('total_scanned_suppliers', 20)} NCC & Đại Lý Cấp 1</b> <i>(12 Quốc gia)</i>",
        f"• 💰 <b>Tổng Giá Trị Pipeline:</b> <b>${pipe_millions}M USD</b>",
        "",
        "📊 <b>PHÂN BỔ THEO NGÀNH HÀNG MŨI NHỌN:</b>"
    ]

    for ind, count in metrics.get("industry_breakdown", {}).items():
        icon = "🌾" if "Nông sản" in ind else ("🧪" if "Phân bón" in ind else ("🐟" if "Thủy" in ind else "📦"))
        lines.append(f"• {icon} {ind}: <b>{count}</b> thương vụ")

    lines.append("")
    lines.append("⭐ <b>TOP 3 THƯƠNG VỤ KIM CƯƠNG NỔI BẬT:</b>")

    for idx, d in enumerate(metrics.get("top_diamond_deals", [])[:3]):
        b_name = d.get("buyer_name", "")
        b_c = d.get("buyer_country", "")
        s_name = d.get("supplier_short_name", "")
        s_full = d.get("supplier_name", "")
        s_c = d.get("supplier_country", "")
        s_type = d.get("supplier_type", "")
        item = d.get("matched_commodity", "")
        hs = d.get("matched_hs", "")
        score = d.get("total_score", 0)
        val_m = round(d.get("deal_value_usd", 0) / 1_000_000, 2)
        lines.append(f"<b>{idx+1}️⃣ {b_name} ({b_c}) ⇄ {s_name} ({s_c})</b>")
        lines.append(f"   • 🏢 <b>Nhà Cung Cấp:</b> {s_full or s_name} [{s_type} - {s_c}]")
        lines.append(f"   • 👤 <b>Khách Hàng (Buyer):</b> {b_name} [{b_c}]")
        lines.append(f"   • 📦 <b>Hàng hóa:</b> {item} (HS {hs}) • 🎯 Điểm: <b>{score}đ</b> • 💰 ~<b>${val_m}M USD</b>")

    lines.append("")
    lines.append(f"💡 <i>Gợi ý: Nhấn nút bên dưới để mở Bàn Khớp Lệnh trên Portal xem toàn bộ đối chiếu ma trận 6 chiều.</i>")

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
    run_morning_dispatch()
