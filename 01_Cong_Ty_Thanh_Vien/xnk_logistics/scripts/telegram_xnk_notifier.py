#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hệ thống Phát Tin & Cảnh Báo Điều Hành Xuất Nhập Khẩu qua Telegram Bot
Khối Xuất Nhập Khẩu & Thương Mại Quốc Tế Tập Đoàn
Bot: @tapdoan_bot
"""

import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BOT_TOKEN = "8821881768:AAFysU6f0IGu4qHHVeN5P-b1fqgFHNPcECI"

def send_xnk_telegram_alert(
    title: str,
    shipment_id: str,
    commodity: str,
    status_icon: str, # 🟢, 🟡, 🔴
    details: list,
    action_required: str,
    chat_id: str = None
):
    """
    Gửi thông điệp điều hành XNK chuẩn mực Executive Telegram Dual-Format
    """
    now_str = datetime.now().strftime("%H:%M %d/%m/%Y")
    
    # Soạn thảo nội dung theo chuẩn executive-admin-telegram-drafter
    text_lines = [
        f"🚢 [KHỐI XNK & THƯƠNG MẠI QUỐC TẾ - BÁO CÁO ĐIỀU HÀNH]",
        f"⏰ Thời khắc: {now_str}",
        f"📌 Lô hàng: {shipment_id} | {commodity}",
        f"----------------------------------------",
        f"{status_icon} TRẠNG THÁI: {title}",
        f""
    ]
    for d in details:
        text_lines.append(f"• {d}")
        
    text_lines.append(f"")
    text_lines.append(f"⚡ CHỈ ĐẠO & HÀNH ĐỘNG TIẾP THEO:")
    text_lines.append(f"👉 {action_required}")
    text_lines.append(f"----------------------------------------")
    text_lines.append(f"🏛️ Văn phòng Thư ký Khối XNK kính trình Chủ tịch!")

    full_text = "\n".join(text_lines)
    print(full_text)

    # Nếu chưa có chat_id, thử lấy từ getUpdates
    if not chat_id:
        try:
            updates_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
            req = urllib.request.Request(updates_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                results = data.get("result", [])
                if results:
                    last_msg = results[-1]
                    chat_id = last_msg.get("message", {}).get("chat", {}).get("id")
        except Exception as e:
            print(f"[DEBUG] getUpdates error: {e}")

    if not chat_id:
        print("\n[THÔNG BÁO] Chưa phát hiện chat_id tương tác với bot. Bản tin được lưu trữ nội bộ.")
        return False

    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": full_text
    }
    try:
        req_data = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(send_url, data=req_data, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            res = json.loads(resp.read().decode())
            if res.get("ok"):
                print(f"\n[SUCCESS] Đã gửi thông báo điều hành XNK thành công tới chat_id: {chat_id}!")
                return True
    except Exception as e:
        print(f"\n[ERROR] Không thể gửi tới Telegram: {e}")
        return False

if __name__ == "__main__":
    # Ví dụ thông báo tàu cập cảng và đếm ngược hạn DEM/DET
    send_xnk_telegram_alert(
        title="TÀU ĐÃ CẬP CẢNG HẢI PHÒNG - BẮT ĐẦU ĐẾM NGƯỢC FREE TIME",
        shipment_id="PO-2026-XNK-001",
        commodity="Hệ thống máy cắt Laser CNC tự động (10 Bộ)",
        status_icon="🟢",
        details=[
            "Hãng tàu: Maersk Line | Tàu: MAERSK MC-KINNEY MOLLER",
            "Cảng đến: Tân Cảng Đình Vũ (Hải Phòng)",
            "Số container: MSKU1234567 (40'HC)",
            "Thời gian miễn phí (Free time kết hợp DEM/DET): 14 ngày (Đến 29/10/2026)",
            "Tờ khai hải quan: Đã truyền IDA, chuẩn bị nộp thuế điện tử"
        ],
        action_required="Đội Hiện trường hoàn tất lấy lệnh D/O và nộp thuế để thông quan trước 17h00 ngày 16/10/2026."
    )
