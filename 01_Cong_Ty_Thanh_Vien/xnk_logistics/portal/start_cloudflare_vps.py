#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cloudflare Tunnel Daemon for VPS 1 (Singapore Node)
Auto-generates public HTTPS tunnel, writes status files and notifies Telegram.
"""

import sys
import os
import re
import time
import json
import subprocess
import urllib.request
import urllib.parse

BASE_DIR = "/root/tapdoan/01_Cong_Ty_Thanh_Vien/xnk_logistics/portal"
CLOUDFLARED_BIN = "/usr/bin/cloudflared"
STATUS_FILE = os.path.join(BASE_DIR, "data", "cloudflare_status.json")
URL_FILE = os.path.join(BASE_DIR, "cloudflare_url.txt")

BOT_TOKEN = "8821881768:AAFysU6f0IGu4qHHVeN5P-b1fqgFHNPcECI"
CHAT_ID = "6034655358"

def notify_telegram(cf_url):
    text = f"""🌐 <b>[CỔNG XNK ĐÃ TRỰC TUYẾN TRÊN VPS 1 - SINGAPORE]</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Kính gửi Chủ tịch Cao Xuân Trường!</b>

Nền tảng Tình Báo & Thẩm Định Ngoại Thương B2B đã được đưa lên cụm máy chủ <b>VPS 1 (Singapore Node - 103.228.74.58)</b> thành công:

🔗 <b>Đường dẫn HTTPS Toàn cầu (Cloudflare SSL):</b>
<code>{cf_url}</code>

🌐 <b>Đường dẫn Trực tiếp IP Cổng 80 (Nginx Reverse Proxy):</b>
<code>http://103.228.74.58/</code>

⚡ <b>Hạ tầng:</b>
• Dịch vụ nền: <code>tapdoan-portal.service</code> (Python 3.10 Daemon Port 8088)
• Web Server: Nginx 1.18 Reverse Proxy (Port 80)
• Đường truyền: Cloudflare Edge Network (SSL 256-bit, DDoS Protection)
• Trải nghiệm: Tối ưu 100% Mobile, Giao diện Sáng/Tối, Khóa cuộn nền Modal & Reset Cuộn Top 10/10 Popup.

<i>Kính mời Chủ tịch truy cập thị sát và chỉ đạo!</i>
#TapDoanHolding #PortalXNK #DeployVPS1 #TrinhChuTich"""

    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = urllib.parse.urlencode({
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"[Telegram Notify]: Success={data.get('ok')}")
    except Exception as e:
        print(f"[Telegram Notify Error]: {e}")

def main():
    print("=" * 60)
    print("🌐 KHỞI CHẠY CLOUDFLARE TUNNEL TRÊN VPS 1 CHO CỔNG XNK PORTAL (PORT 8088)")
    print("=" * 60)

    if not os.path.exists(CLOUDFLARED_BIN):
        print(f"❌ Không tìm thấy binary cloudflared tại: {CLOUDFLARED_BIN}")
        sys.exit(1)

    cmd = [CLOUDFLARED_BIN, "tunnel", "--protocol", "http2", "--url", "http://127.0.0.1:8088"]
    print("🚀 Đang khởi tạo kết nối Cloudflare Tunnel (HTTP/2 Mode)...")

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        encoding="utf-8",
        errors="replace"
    )

    cf_url = None
    start_time = time.time()

    while time.time() - start_time < 30:
        line = proc.stderr.readline()
        if not line:
            time.sleep(0.1)
            continue

        line_clean = line.strip()
        print(f"[Cloudflare Log]: {line_clean}")

        m = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line_clean)
        if m:
            cf_url = m.group(0)
            print("\n" + "=" * 60)
            print(f"🎉 ĐÃ CẤP PHÁT CLOUDFLARE URL THÀNH CÔNG!")
            print(f"🌐 PUBLIC URL: {cf_url}")
            print("=" * 60 + "\n")

            with open(URL_FILE, "w", encoding="utf-8") as f:
                f.write(cf_url)

            os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
            status_data = {
                "status": "ONLINE",
                "provider": "Cloudflare Tunnel (VPS 1)",
                "public_url": cf_url,
                "local_target": "http://127.0.0.1:8088",
                "direct_ip_url": "http://103.228.74.58/",
                "connected_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "ssl": "Cloudflare Universal SSL"
            }
            with open(STATUS_FILE, "w", encoding="utf-8") as f:
                json.dump(status_data, f, ensure_ascii=False, indent=2)

            notify_telegram(cf_url)
            break

    if not cf_url:
        print("⚠️ Hết thời gian chờ cấp phát URL từ Cloudflare.")
        proc.terminate()
        sys.exit(1)

    try:
        while proc.poll() is None:
            line = proc.stderr.readline()
            if line:
                pass
            time.sleep(1)
    except KeyboardInterrupt:
        print("Đang dừng Cloudflare Tunnel...")
        proc.terminate()

if __name__ == "__main__":
    main()
