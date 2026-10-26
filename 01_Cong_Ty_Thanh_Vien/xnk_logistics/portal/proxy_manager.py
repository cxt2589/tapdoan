#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HỆ THỐNG CỔNG QUẢN TRỊ MẠNG & PROXY CHỜ "CẮM-LÀ-CHẠY" (PLUG-AND-PLAY PROXY GATEWAY)
Tập đoàn Holding - Phân hệ Tình Báo Ngoại Thương & Quét Dữ Liệu Hải Quan

Cơ chế:
1. Mặc định: Chạy ở chế độ "DIRECT" (Kết nối trực tiếp từ máy chủ Singapore, kèm Stealth Headers
   và giãn cách thông minh).
2. Khi bổ sung hệ thống Proxy: Chỉ cần nhập cấu hình vào proxy_config.json hoặc gọi API
   POST /api/proxy/config, hệ thống tự động kích hoạt xoay vòng (Rotating Proxy) và định tuyến
   theo quốc gia mà không cần khởi động lại máy chủ!
"""

import os
import sys
import json
import random
import time
import socket
import urllib.request
import urllib.error
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Đảm bảo UTF-8 cho Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "data", "proxy_config.json")

# Danh sách User-Agents thực tế của Chrome/Safari/Edge hiện đại
STEALTH_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
]

DEFAULT_CONFIG = {
    "enabled": False,
    "mode": "DIRECT",  # DIRECT, STATIC_POOL, ROTATING_API, RESIDENTIAL_GATEWAY
    "api_endpoint": "",
    "api_key": "",
    "proxies_pool": [],
    "auth": {
        "username": "",
        "password": ""
    },
    "country_routing": {
        "us": "",
        "eu": "",
        "cn": "",
        "ru": "",
        "kr": "",
        "jp": "",
        "ae": "",
        "vn": ""
    },
    "rotation_strategy": "round_robin",
    "max_retries": 3,
    "timeout_seconds": 12,
    "last_updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
}

_pool_index = 0

def load_proxy_config():
    """Tải cấu hình proxy từ file hoặc tạo mặc định"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                # Đảm bảo có đủ các key mặc định
                for k, v in DEFAULT_CONFIG.items():
                    if k not in cfg:
                        cfg[k] = v
                return cfg
        except Exception as e:
            print(f"[ProxyManager] Lỗi đọc {CONFIG_FILE}: {e}")
    
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    save_proxy_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG

def save_proxy_config(config_dict):
    """Lưu cấu hình proxy"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    config_dict["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_dict, f, ensure_ascii=False, indent=2)
    return config_dict

def get_stealth_headers(custom_headers=None):
    """Sinh header trình duyệt thật để tránh bị nhận diện bot"""
    headers = {
        "User-Agent": random.choice(STEALTH_USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
    }
    if custom_headers:
        headers.update(custom_headers)
    return headers

def get_active_proxy(country_code=None):
    """
    Lấy proxy phù hợp theo quốc gia hoặc theo chiến lược xoay vòng.
    Nếu đang ở chế độ DIRECT, trả về None.
    """
    global _pool_index
    cfg = load_proxy_config()
    if not cfg.get("enabled", False) or cfg.get("mode") == "DIRECT":
        return None

    c_code = (country_code or "").lower().strip()
    c_routing = cfg.get("country_routing", {})
    if c_code and c_routing.get(c_code):
        return c_routing[c_code]

    pool = cfg.get("proxies_pool", [])
    if not pool:
        return None

    strategy = cfg.get("rotation_strategy", "round_robin")
    if strategy == "random":
        return random.choice(pool)
    else:
        # Round-robin
        proxy = pool[_pool_index % len(pool)]
        _pool_index += 1
        return proxy

def build_urllib_opener(country_code=None):
    """Xây dựng urllib opener có gắn proxy và handlers phù hợp"""
    proxy_url = get_active_proxy(country_code)
    handlers = []
    
    if proxy_url:
        proxy_handler = urllib.request.ProxyHandler({
            "http": proxy_url,
            "https": proxy_url
        })
        handlers.append(proxy_handler)
        
    opener = urllib.request.build_opener(*handlers)
    return opener, proxy_url

def test_proxy_connectivity(proxy_url=None):
    """
    Kiểm tra kết nối và đo độ trễ của IP hiện tại (hoặc qua proxy chỉ định).
    """
    cfg = load_proxy_config()
    target_proxy = proxy_url if proxy_url is not None else get_active_proxy()
    
    test_urls = [
        "https://api.ipify.org?format=json",
        "https://httpbin.org/ip"
    ]
    
    start_t = time.time()
    for t_url in test_urls:
        try:
            handlers = []
            if target_proxy:
                handlers.append(urllib.request.ProxyHandler({"http": target_proxy, "https": target_proxy}))
            opener = urllib.request.build_opener(*handlers)
            
            req = urllib.request.Request(t_url, headers=get_stealth_headers())
            with opener.open(req, timeout=cfg.get("timeout_seconds", 10)) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                latency_ms = int((time.time() - start_t) * 1000)
                out_ip = data.get("ip") or data.get("origin") or "Unknown"
                return {
                    "ok": True,
                    "mode": "PROXY" if target_proxy else "DIRECT_SINGAPORE",
                    "proxy_used": target_proxy or "Direct Node",
                    "outbound_ip": out_ip,
                    "latency_ms": latency_ms,
                    "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        except Exception as e:
            continue
            
    return {
        "ok": False,
        "mode": "PROXY" if target_proxy else "DIRECT_SINGAPORE",
        "error": f"Không thể kết nối qua cổng kiểm thử: {target_proxy or 'Direct'}",
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def check_single_proxy_alive(proxy_item, timeout_seconds=1.2):
    """Kiểm tra socket TCP nhanh để xác thực proxy có phản hồi và đo độ trễ ms"""
    host = proxy_item.get("host")
    port = proxy_item.get("port")
    if not host or not port:
        return None
    t0 = time.time()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout_seconds)
        s.connect((host, int(port)))
        s.close()
        latency_ms = int((time.time() - t0) * 1000)
        c_code = proxy_item.get("geolocation", {}).get("country", {}).get("iso_code", "GLOBAL").upper()
        proto = proxy_item.get("protocol", "http").lower()
        if proto not in ["http", "https"]:
            proto = "http"
        return {
            "proxy": f"{proto}://{host}:{port}",
            "raw_ip_port": f"{host}:{port}",
            "country": c_code,
            "latency_ms": latency_ms,
            "protocol": proto
        }
    except Exception:
        return None

def auto_harvest_and_verify_proxies(force=False, max_candidates=60, timeout_per_proxy=1.2):
    """
    Tự động thu hoạch và kiểm định proxy trước mỗi chu kỳ quét:
    1. Kéo danh sách proxy tươi từ nguồn mở GitHub (monosans, TheSpeedX).
    2. Lọc ứng viên từ các quốc gia mục tiêu: US, EU (DE, FR, NL), CN, VN, RU, JP, KR, IN, SG.
    3. Kiểm định đa luồng (multi-threaded ping test) trong < 2.5 giây.
    4. Cập nhật tự động vào proxy_config.json với country_routing và static pool.
    5. Tự động fallback về DIRECT nếu không có proxy sống.
    """
    cfg = load_proxy_config()
    
    # Kiểm tra cache (nếu đã quét cách đây < 30 phút và không ép buộc thì tái sử dụng)
    last_harvest = cfg.get("last_harvested_at")
    if not force and last_harvest:
        try:
            last_dt = datetime.strptime(last_harvest, "%Y-%m-%dT%H:%M:%SZ")
            if (datetime.now() - last_dt).total_seconds() < 1800 and cfg.get("proxies_pool"):
                return {
                    "ok": True,
                    "cached": True,
                    "mode": cfg.get("mode", "DIRECT"),
                    "alive_count": len(cfg.get("proxies_pool", [])),
                    "harvest_stats": cfg.get("harvest_stats", {}),
                    "message": "Sử dụng dải proxy sống vừa được kiểm định trong vòng 30 phút qua."
                }
        except Exception:
            pass
            
    print("🔍 [AUTO-HARVEST] Đang kéo dải proxy tươi từ GitHub và kiểm định kết nối...")
    
    raw_candidates = []
    # Nguồn 1: monosans/proxy-list (có Geolocation 76 quốc gia)
    try:
        url = "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_pretty.json"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            
        target_countries = {"US", "DE", "FR", "NL", "CN", "VN", "RU", "IN", "SG", "JP", "KR", "AE", "GB"}
        by_country = {}
        for p in data:
            c = p.get("geolocation", {}).get("country", {}).get("iso_code", "")
            if c in target_countries:
                by_country.setdefault(c, []).append(p)
                
        # Lấy tối đa 5 proxy mỗi quốc gia mục tiêu
        for c, plist in by_country.items():
            raw_candidates.extend(plist[:5])
    except Exception as e:
        print(f"⚠️ [AUTO-HARVEST] Không thể kéo từ monosans ({e}), thử nguồn TheSpeedX...")
        try:
            url_fallback = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
            req = urllib.request.Request(url_fallback, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                lines = resp.read().decode("utf-8").splitlines()
                for line in lines[:40]:
                    if ":" in line:
                        h, pt = line.strip().split(":")
                        raw_candidates.append({
                            "host": h,
                            "port": pt,
                            "protocol": "http",
                            "geolocation": {"country": {"iso_code": "GLOBAL"}}
                        })
        except Exception as e2:
            print(f"⚠️ [AUTO-HARVEST] Không thể kéo fallback: {e2}")

    if not raw_candidates:
        print("ℹ️ [AUTO-HARVEST] Không lấy được ứng viên proxy mới, duy trì kết nối Direct Singapore an toàn.")
        return {
            "ok": True,
            "mode": "DIRECT",
            "alive_count": 0,
            "message": "Không có ứng viên proxy, hệ thống tự động chạy DIRECT từ Node Singapore."
        }

    # Kiểm định đa luồng siêu tốc
    t_start = time.time()
    alive_results = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for res in executor.map(lambda p: check_single_proxy_alive(p, timeout_per_proxy), raw_candidates[:max_candidates]):
            if res:
                alive_results.append(res)

    duration = round(time.time() - t_start, 2)
    print(f"⏱️ [AUTO-HARVEST] Kiểm định hoàn tất trong {duration}s: {len(alive_results)}/{len(raw_candidates[:max_candidates])} IP phản hồi tốt.")

    if alive_results:
        # Sắp xếp theo ping nhanh nhất
        alive_results.sort(key=lambda x: x["latency_ms"])
        
        # Cập nhật Country Routing
        country_routing = dict(cfg.get("country_routing", {}))
        for item in alive_results:
            c = item["country"].lower()
            if c == "us" and not country_routing.get("us"):
                country_routing["us"] = item["proxy"]
            elif c in ["de", "fr", "nl", "gb"] and not country_routing.get("eu"):
                country_routing["eu"] = item["proxy"]
            elif c == "cn" and not country_routing.get("cn"):
                country_routing["cn"] = item["proxy"]
            elif c == "vn" and not country_routing.get("vn"):
                country_routing["vn"] = item["proxy"]
            elif c == "ru" and not country_routing.get("ru"):
                country_routing["ru"] = item["proxy"]
            elif c == "jp" and not country_routing.get("jp"):
                country_routing["jp"] = item["proxy"]
            elif c == "kr" and not country_routing.get("kr"):
                country_routing["kr"] = item["proxy"]
            elif c == "ae" and not country_routing.get("ae"):
                country_routing["ae"] = item["proxy"]

        pool = [item["proxy"] for item in alive_results[:20]]
        avg_lat = int(sum(item["latency_ms"] for item in alive_results) / len(alive_results))
        countries_cov = list(set(item["country"] for item in alive_results))

        now_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        cfg["enabled"] = True
        cfg["mode"] = "STATIC_POOL"
        cfg["proxies_pool"] = pool
        cfg["country_routing"] = country_routing
        cfg["last_harvested_at"] = now_iso
        cfg["harvest_stats"] = {
            "total_candidates": len(raw_candidates[:max_candidates]),
            "alive_count": len(alive_results),
            "countries_covered": countries_cov,
            "avg_latency_ms": avg_lat,
            "duration_seconds": duration,
            "tested_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_proxy_config(cfg)

        return {
            "ok": True,
            "mode": "STATIC_POOL",
            "alive_count": len(alive_results),
            "countries_covered": countries_cov,
            "avg_latency_ms": avg_lat,
            "duration_seconds": duration,
            "message": f"Tự động kích hoạt {len(alive_results)} Proxy sống, phủ {len(countries_cov)} quốc gia (Ping TB {avg_lat}ms)."
        }
    else:
        # Không có proxy sống -> Tự động chuyển DIRECT
        cfg["enabled"] = False
        cfg["mode"] = "DIRECT"
        save_proxy_config(cfg)
        return {
            "ok": True,
            "mode": "DIRECT",
            "alive_count": 0,
            "message": "Không có proxy miễn phí đạt chuẩn ping, tự động chuyển chế độ DIRECT Node Singapore an toàn."
        }

def get_public_status():
    """Lấy thông tin trạng thái công khai (ẩn mật khẩu) để hiển thị Dashboard"""
    cfg = load_proxy_config()
    safe_auth = {}
    if cfg.get("auth", {}).get("username"):
        safe_auth["username"] = cfg["auth"]["username"]
        safe_auth["has_password"] = bool(cfg["auth"].get("password"))

    return {
        "enabled": cfg.get("enabled", False),
        "mode": cfg.get("mode", "DIRECT"),
        "total_proxies_in_pool": len(cfg.get("proxies_pool", [])),
        "rotation_strategy": cfg.get("rotation_strategy", "round_robin"),
        "country_routes_configured": [k for k, v in cfg.get("country_routing", {}).items() if v],
        "api_endpoint_configured": bool(cfg.get("api_endpoint")),
        "auth_configured": bool(safe_auth.get("username")),
        "timeout_seconds": cfg.get("timeout_seconds", 12),
        "last_updated": cfg.get("last_updated"),
        "last_harvested_at": cfg.get("last_harvested_at"),
        "auto_harvest_stats": cfg.get("harvest_stats", {})
    }

if __name__ == "__main__":
    print("=== KIỂM THỬ PROXY MANAGER & CỔNG CHỜ ===")
    cfg = load_proxy_config()
    print("Cấu hình hiện tại:", json.dumps(get_public_status(), indent=2, ensure_ascii=False))
    print("\nKiểm tra IP ngoại mạng hiện tại:")
    res = test_proxy_connectivity()
    print(json.dumps(res, indent=2, ensure_ascii=False))
