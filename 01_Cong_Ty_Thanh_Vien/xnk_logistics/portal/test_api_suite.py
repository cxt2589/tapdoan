# -*- coding: utf-8 -*-
"""
test_api_suite.py
Suite kiểm thử tự động toàn diện cho bộ API Nền Tảng Tình Báo & Thẩm Định Ngoại Thương
Phát triển theo chuẩn API Platform Engineer & API Tester.
"""

import sys
import json
import urllib.request
import urllib.parse
import urllib.error

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE_URL = "http://127.0.0.1:8088"
passed_count = 0
total_count = 0

def log_test(title, success, detail=""):
    global passed_count, total_count
    total_count += 1
    if success:
        passed_count += 1
        print(f"  [PASS] Test {total_count:02d}: {title}")
        if detail:
            print(f"         {detail}")
    else:
        print(f"  [FAIL] Test {total_count:02d}: {title}")
        if detail:
            print(f"         Error: {detail}")

def http_get(path):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "TradeApiTester/1.0"})
    with urllib.request.urlopen(req, timeout=10) as res:
        return res.status, json.loads(res.read().decode("utf-8"))

def http_get_raw(path):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "TradeApiTester/1.0"})
    with urllib.request.urlopen(req, timeout=10) as res:
        return res.status, res.headers.get("Content-Type", ""), res.read().decode("utf-8")

def http_post(path, payload):
    url = f"{BASE_URL}{path}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        "User-Agent": "TradeApiTester/1.0"
    })
    with urllib.request.urlopen(req, timeout=10) as res:
        return res.status, json.loads(res.read().decode("utf-8"))

def run_suite():
    print("==================================================================")
    print("🚀 BẮT ĐẦU KIỂM THỬ TỰ ĐỘNG BỘ API TRADE INTELLIGENCE PLATFORM")
    print(f"🎯 Điểm cuối kiểm thử: {BASE_URL}")
    print("==================================================================")

    # 1. API Catalog & Metadata
    try:
        status, data = http_get("/api")
        ok = status == 200 and data.get("ok") is True and len(data.get("categories", [])) >= 10
        log_test("API Root & Category Catalog (/api)", ok, f"Categories: {len(data.get('categories', []))}")
    except Exception as e:
        log_test("API Root & Category Catalog (/api)", False, str(e))

    # 2. OpenAPI 3.1.0 Contract
    try:
        status, data = http_get("/api/openapi.json")
        ok = status == 200 and data.get("openapi") == "3.1.0" and len(data.get("paths", {})) >= 35
        log_test("OpenAPI 3.1.0 JSON Spec (/api/openapi.json)", ok, f"Paths: {len(data.get('paths', {}))}, Schemas: {len(data.get('components', {}).get('schemas', {}))}")
    except Exception as e:
        log_test("OpenAPI 3.1.0 JSON Spec (/api/openapi.json)", False, str(e))

    # 3. Interactive Developer Portal / Swagger UI
    try:
        status, ctype, body = http_get_raw("/api/docs")
        ok = status == 200 and "swagger-ui" in body and "text/html" in ctype
        log_test("Developer Portal & Swagger UI (/api/docs)", ok, f"Content-Type: {ctype}, Size: {len(body)} bytes")
    except Exception as e:
        log_test("Developer Portal & Swagger UI (/api/docs)", False, str(e))

    # 4. Universal Commodity Unit & Currency Conversion
    try:
        payload = {"value": 5, "from_unit": "MT", "to_unit": "lbs", "price_usd": 4800, "exchange_rate_vnd": 25450}
        status, data = http_post("/api/prices/convert", payload)
        ok = status == 200 and data.get("ok") is True and data.get("metric_tons") == 5.0 and data.get("price_analysis", {}).get("equivalent_usd_per_kg") == 4.8
        log_test("Commodity Unit & Currency Converter (/api/prices/convert)", ok, f"5 MT = {data.get('pounds_lbs')} lbs, {data.get('price_analysis', {}).get('equivalent_vnd_per_kg'):,} VND/kg")
    except Exception as e:
        log_test("Commodity Unit & Currency Converter (/api/prices/convert)", False, str(e))

    # 5. Multi-Exchange Arbitrage & Spread Calculator
    try:
        payload = {"commodity_id": "coffee_robusta", "buy_tier": "spot_farmgate", "sell_tier": "ice_london_futures", "estimated_freight_usd": 80}
        status, data = http_post("/api/prices/arbitrage", payload)
        ok = status == 200 and data.get("ok") is True and "gross_spread_usd_mt" in data and "arbitrage_viable" in data
        log_test("Cross-Exchange Arbitrage Calculator (/api/prices/arbitrage)", ok, f"Gross spread: {data.get('gross_spread_usd_mt')} USD/MT, Viable: {data.get('arbitrage_viable')}")
    except Exception as e:
        log_test("Cross-Exchange Arbitrage Calculator (/api/prices/arbitrage)", False, str(e))

    # 6. Telegram Alert Dispatch Engine (Dry-Run Mode)
    try:
        payload = {
            "title": "Cảnh Báo Chênh Lệch Giá Cà Phê Xuất Khẩu",
            "details": ["Giá ICE London vọt lên 4,785 USD/MT", "Nông dân Tây Nguyên chào bán 116,500 đ/kg", "Biên độ spread gộp: +205 USD/MT"],
            "status_icon": "💰",
            "action_required": "Khối KD xúc tiến chốt hợp đồng FOB Cát Lái ngay trong ngày",
            "dry_run": True
        }
        status, data = http_post("/api/telegram/alert", payload)
        ok = status == 200 and data.get("ok") is True and data.get("dry_run") is True
        log_test("Executive Telegram Alert Engine (/api/telegram/alert)", ok, f"Status: {data.get('status')}, Chars: {data.get('message_length')}")
    except Exception as e:
        log_test("Executive Telegram Alert Engine (/api/telegram/alert)", False, str(e))

    # 7. System Health Endpoint
    try:
        status, data = http_get("/api/health")
        ok = status == 200 and data.get("status") == "ONLINE" and "db_stats" in data
        log_test("System Health Monitor (/api/health)", ok, f"Status: {data.get('status')}, Leads: {data.get('db_stats', {}).get('industry_leads')}")
    except Exception as e:
        log_test("System Health Monitor (/api/health)", False, str(e))

    # 8. Sourcing Industries Catalog
    try:
        status, data = http_get("/api/industries")
        ok = status == 200 and isinstance(data, list) and len(data) >= 5
        log_test("Industries Catalog (/api/industries)", ok, f"Industries count: {len(data)}")
    except Exception as e:
        log_test("Industries Catalog (/api/industries)", False, str(e))

    # 9. Leads & Discovery by Industry
    try:
        status, data = http_get("/api/leads/by-industry?industry=agri_food")
        ok = status == 200 and data.get("total", 0) >= 4 and len(data.get("data", [])) > 0
        log_test("Leads Query by Industry (/api/leads/by-industry)", ok, f"Found {data.get('total')} leads in Agri-Food")
    except Exception as e:
        log_test("Leads Query by Industry (/api/leads/by-industry)", False, str(e))

    # 10. Global Suppliers & Master Agent Network
    try:
        status, data = http_get("/api/suppliers?type=tier1_master_agent")
        ok = status == 200 and isinstance(data, list) and len(data) > 0
        log_test("Global Suppliers Query (/api/suppliers)", ok, f"Found {len(data)} Tier-1 Master Agents")
    except Exception as e:
        log_test("Global Suppliers Query (/api/suppliers)", False, str(e))

    # 11. Trade Matchmaker Metrics
    try:
        status, data = http_get("/api/matches/metrics")
        ok = status == 200 and ("total_active_pairs" in data or "top_diamond_deals" in data or data.get("ok") is True)
        log_test("Trade Matchmaker Metrics (/api/matches/metrics)", ok, f"Metrics retrieved successfully")
    except Exception as e:
        log_test("Trade Matchmaker Metrics (/api/matches/metrics)", False, str(e))

    # 12. Trade Matchmaker Pair Analysis
    try:
        payload = {"buyer_id": "LEAD-AGRI-001", "supplier_id": "SP-002"}
        status, data = http_post("/api/matches/analyze", payload)
        ok = status == 200 and data.get("ok") is True and "match" in data
        score = data.get("match", {}).get("total_score", 0)
        log_test("Trade 6D Match Matrix Analysis (/api/matches/analyze)", ok, f"Match Total Score: {score}/100")
    except Exception as e:
        log_test("Trade 6D Match Matrix Analysis (/api/matches/analyze)", False, str(e))

    # 13. HS Nomenclature & Strategic Products Summary
    try:
        status, data = http_get("/api/hs/summary")
        ok = status == 200 and data.get("chapters_count") == 97
        log_test("HS Nomenclature Summary (/api/hs/summary)", ok, f"Total Chapters: {data.get('chapters_count')}, Sections: {data.get('sections_count')}")
    except Exception as e:
        log_test("HS Nomenclature Summary (/api/hs/summary)", False, str(e))

    # 14. Regulatory Radar Active Policies
    try:
        status, data = http_get("/api/regulations/active")
        ok = status == 200 and data.get("status") == "SUCCESS" and len(data.get("regulations", [])) >= 4
        log_test("Regulatory Radar Active Policies (/api/regulations/active)", ok, f"Active policies: {len(data.get('regulations', []))}")
    except Exception as e:
        log_test("Regulatory Radar Active Policies (/api/regulations/active)", False, str(e))

    # 15. Trade Tags & Terminology Dictionary
    try:
        status, data = http_get("/api/trade-tags/catalog")
        ok = status == 200 and data.get("status") == "SUCCESS" and data.get("total", 0) >= 10
        log_test("Trade Tags Catalog (/api/trade-tags/catalog)", ok, f"Total Trade Tags: {data.get('total')}")
    except Exception as e:
        log_test("Trade Tags Catalog (/api/trade-tags/catalog)", False, str(e))

    # 16. Multi-Exchange Commodity Price Benchmarks
    try:
        status, data = http_get("/api/prices/benchmarks")
        ok = status == 200 and data.get("ok") is True and "sectors" in data.get("data", {}) and len(data["data"]["sectors"]) >= 6
        log_test("Commodity Multi-Exchange Benchmarks (/api/prices/benchmarks)", ok, f"Tracked commodities: {len(data['data']['sectors'])}")
    except Exception as e:
        log_test("Commodity Multi-Exchange Benchmarks (/api/prices/benchmarks)", False, str(e))

    print("==================================================================")
    print(f"🎉 TỔNG KẾT: {passed_count}/{total_count} BÀI KIỂM THỬ API THÀNH CÔNG ({(passed_count/total_count*100):.1f}%)")
    print("==================================================================")

    if passed_count == total_count:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    run_suite()
