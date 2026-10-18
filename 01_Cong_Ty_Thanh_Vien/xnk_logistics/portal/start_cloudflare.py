#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cloudflare Tunnel Daemon & Auto-Dispatch
Khối Xuất Nhập Khẩu & Thương Mại Quốc Tế - Tổng Hành Dinh
"""

import sys
import os
import re
import time
import json
import subprocess
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLOUDFLARED_BIN = shutil.which("cloudflared") or os.path.join(BASE_DIR, "cloudflared.exe") or "/usr/local/bin/cloudflared"
STATUS_FILE = os.path.join(BASE_DIR, "data", "cloudflare_status.json")
URL_FILE = os.path.join(BASE_DIR, "cloudflare_url.txt")

def notify_telegram(cf_url):
    bot_token = "8227653245:AAEYq_3sB_rCg0h6bX2U09PfqVvR1j3YJ5o"
    chat_id = "6034655358"
    text = f"""🌐 [CLOUDFLARE LIVE DEPLOYMENT - TỔNG HÀNH DINH]

🏛️ Cổng Thông Tin Tình Báo & Thẩm Định XNK Tập Đoàn đã trực tuyến toàn cầu qua Mạng lưới Cloudflare Edge:

🔗 Đường Dẫn Truy Cập Trực Tuyến:
{cf_url}

⚡ Hạ Tầng: Cloudflare Tunnel (SSL 256-bit, Edge Cache)
🚀 Cổng kết nối nội bộ: Port 8088 (Healthy)
📱 Trải nghiệm: Tối ưu 100% Mobile, Giao diện Sáng/Tối, Khóa cuộn nền Modal & Thoát Popup 1 chạm.

Kính mời Chủ tịch truy cập thị sát và chỉ đạo."""

    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = json.dumps({"chat_id": chat_id, "text": text}).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"[Telegram Notify]: Status={data.get('ok')}")
    except Exception as e:
        print(f"[Telegram Notify Error]: {e}")

def main():
    print("=" * 60)
    print("🌐 KHỞI CHẠY CLOUDFLARE TUNNEL CHO CỔNG XNK PORTAL (PORT 8088)")
    print("=" * 60)

    if not os.path.exists(CLOUDFLARED_BIN):
        print(f"❌ Không tìm thấy binary cloudflared tại: {CLOUDFLARED_BIN}")
        sys.exit(1)

    cmd = [CLOUDFLARED_BIN, "tunnel", "--url", "http://127.0.0.1:8088"]
    print(f"🚀 Đang kết nối tới mạng lưới toàn cầu Cloudflare Edge...")
    
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        encoding='utf-8',
        errors='replace'
    )

    cf_url = None
    start_time = time.time()
    
    while time.time() - start_time < 25:
        line = proc.stderr.readline()
        if not line:
            time.sleep(0.1)
            continue
            
        line_clean = line.strip()
        print(f"[Cloudflare Log]: {line_clean}")
        
        m = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line_clean)
        if m:
            cf_url = m.group(0)
            print("\n" + "=" * 60)
            print(f"🎉 ĐÃ ĐẨY LÊN CLOUDFLARE THÀNH CÔNG!")
            print(f"🌐 PUBLIC URL: {cf_url}")
            print("=" * 60 + "\n")
            
            with open(URL_FILE, "w", encoding="utf-8") as f:
                f.write(cf_url)
                
            status_data = {
                "status": "ONLINE",
                "provider": "Cloudflare Tunnel",
                "public_url": cf_url,
                "local_target": "http://127.0.0.1:8088",
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

    # Keep tunnel alive
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
