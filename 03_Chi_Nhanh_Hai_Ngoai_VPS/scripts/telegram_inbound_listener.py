#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Inbound Directive Listener Daemon
Runs 24/7 on VPS 1 (Singapore Node).
Listens for commands/directives sent by Chairman Cao Xuân Trường (@tapdoan_bot),
logs them to SSOT audit trail, and acknowledges immediately.
"""

import os
import sys
import time
import json
import urllib.request
import urllib.parse
from datetime import datetime

BOT_TOKEN = "8821881768:AAFysU6f0IGu4qHHVeN5P-b1fqgFHNPcECI"
CHAIRMAN_CHAT_ID = 6034655358

BASE_DIR = "/root/tapdoan"
LOG_DIR = os.path.join(BASE_DIR, "03_Chi_Nhanh_Hai_Ngoai_VPS", "logs")
DIRECTIVES_LOG = os.path.join(LOG_DIR, "telegram_directives.jsonl")
OFFSET_FILE = os.path.join(LOG_DIR, "telegram_offset.txt")

def send_ack(chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = urllib.parse.urlencode({
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            pass
    except Exception as e:
        print(f"[Error send_ack]: {e}")

def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    print("=" * 60)
    print("🤖 TELEGRAM INBOUND DIRECTIVE LISTENER DAEMON STARTED")
    print(f"📡 Target Bot: @tapdoan_bot | Chairman ID: {CHAIRMAN_CHAT_ID}")
    print("=" * 60)

    offset = None
    if os.path.exists(OFFSET_FILE):
        try:
            with open(OFFSET_FILE, "r") as f:
                offset = int(f.read().strip())
        except Exception:
            offset = None

    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?timeout=30"
            if offset is not None:
                url += f"&offset={offset}"

            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=40) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            if not data.get("ok"):
                time.sleep(5)
                continue

            updates = data.get("result", [])
            for u in updates:
                update_id = u["update_id"]
                offset = update_id + 1
                with open(OFFSET_FILE, "w") as f:
                    f.write(str(offset))

                msg = u.get("message") or u.get("edited_message")
                if not msg:
                    continue

                from_user = msg.get("from", {})
                chat_id = msg.get("chat", {}).get("id")
                text = msg.get("text", "")
                date_ts = msg.get("date", int(time.time()))
                date_str = datetime.fromtimestamp(date_ts).strftime("%Y-%m-%d %H:%M:%S")

                print(f"[{date_str}] Message from {from_user.get('first_name')} ({chat_id}): {text}")

                record = {
                    "update_id": update_id,
                    "date": date_str,
                    "timestamp": date_ts,
                    "chat_id": chat_id,
                    "from_user": from_user,
                    "text": text
                }

                with open(DIRECTIVES_LOG, "a", encoding="utf-8") as f_log:
                    f_log.write(json.dumps(record, ensure_ascii=False) + "\n")

                if chat_id == CHAIRMAN_CHAT_ID:
                    ack_text = f"""🏛️ <b>[VĂN PHÒNG THƯ KÝ TỔNG HÀNH DINH — ĐÃ TIẾP NHẬN CHỈ THỊ]</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Kính thưa Chủ tịch Cao Xuân Trường,</b>

Hệ thống điều hành trung tâm đã tiếp nhận chỉ đạo của Chủ tịch vào lúc <b>{date_str}</b>:
<blockquote><i>« {text} »</i></blockquote>

⚡ <b>Trạng thái tác chiến:</b>
• Lệnh đã được ghi nhận vào Sổ tay Chỉ thị Tổng Hành Dinh (SSOT).
• Group CEO và Ban Thư ký đang điều phối các khối chuyên môn thực thi ngay lập tức.

<i>Kính trình Chủ tịch an tâm.</i>
#TiepNhanChiThi #VanPhongThuKy #TongHanhDinh"""
                    send_ack(chat_id, ack_text)

        except Exception as e:
            print(f"[Loop Exception]: {e}")
            time.sleep(3)

if __name__ == "__main__":
    main()
