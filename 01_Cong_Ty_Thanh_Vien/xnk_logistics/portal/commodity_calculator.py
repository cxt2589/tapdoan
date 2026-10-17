#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Commodity Unit Normalizer & Arbitrage Spread Calculator
Khối Xuất Nhập Khẩu & Thương Mại Quốc Tế — Tổng Hành Dinh
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRICES_FILE = os.path.join(BASE_DIR, "data", "multi_exchange_commodity_prices.json")

# Quy đổi tất cả các đơn vị ngoại thương sang Metric Ton (MT)
UNIT_TO_MT = {
    "mt": 1.0,
    "ton": 1.0,
    "tan": 1.0,
    "kg": 0.001,
    "kilogram": 0.001,
    "lbs": 1.0 / 2204.62262,
    "pound": 1.0 / 2204.62262,
    "bag_60kg": 0.06,
    "bao_60kg": 0.06,
    "bag_50kg": 0.05,
    "bao_50kg": 0.05,
    "cwt": 0.045359237,  # Hundredweight (Mỹ: 100 lbs)
}

def convert_units_and_currency(value, from_unit="mt", to_unit="mt", price_usd=None, exchange_rate_vnd=25450.0):
    from_u = str(from_unit).lower().strip()
    to_u = str(to_unit).lower().strip()

    from_factor = UNIT_TO_MT.get(from_u, 1.0)
    to_factor = UNIT_TO_MT.get(to_u, 1.0)

    try:
        val = float(value)
    except Exception:
        val = 0.0

    mt_volume = val * from_factor
    converted_val = round(mt_volume / to_factor, 4)

    res = {
        "ok": True,
        "input_value": val,
        "from_unit": from_u,
        "to_unit": to_u,
        "converted_value": converted_val,
        "metric_tons": round(mt_volume, 4),
        "kilograms": round(mt_volume * 1000.0, 2),
        "pounds_lbs": round(mt_volume * 2204.62262, 2),
    }

    if price_usd is not None:
        try:
            p_usd = float(price_usd)
            # Nếu giá đưa vào là theo from_unit
            price_per_mt = p_usd / from_factor
            vnd_kg = (price_per_mt * float(exchange_rate_vnd)) / 1000.0
            res["price_analysis"] = {
                "input_price_usd": p_usd,
                "equivalent_usd_per_mt": round(price_per_mt, 2),
                "equivalent_usd_per_kg": round(price_per_mt / 1000.0, 4),
                "equivalent_usd_per_lbs": round(price_per_mt / 2204.62262, 4),
                "equivalent_vnd_per_kg": round(vnd_kg, 0),
                "exchange_rate_vnd": float(exchange_rate_vnd)
            }
        except Exception as e:
            res["price_error"] = str(e)

    return res

def calculate_arbitrage_spread(commodity_id, buy_tier="DOMESTIC_FARM", sell_tier="DESTINATION_CIF", estimated_freight_usd=80.0):
    if not os.path.exists(PRICES_FILE):
        return {"ok": False, "error": "Prices database not found"}

    try:
        with open(PRICES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return {"ok": False, "error": str(e)}

    sectors = data.get("sectors", [])
    comm = None
    c_id_low = str(commodity_id).lower().strip()

    for s in sectors:
        if s.get("commodity_id", "").lower() == c_id_low or \
           c_id_low in s.get("commodity_name", "").lower() or \
           c_id_low == s.get("hs_code", ""):
            comm = s
            break

    if not comm:
        return {"ok": False, "error": f"Commodity '{commodity_id}' not found in benchmark exchange"}

    benchmarks = comm.get("benchmarks", [])
    tier_map = {}
    for b in benchmarks:
        tier_map[b.get("tier_type", "")] = b

    # Chuẩn hóa tier
    b_tier_key = str(buy_tier).upper().strip()
    s_tier_key = str(sell_tier).upper().strip()

    # Fallbacks nếu nhập dạng thường
    if "FARM" in b_tier_key: b_tier_key = "DOMESTIC_FARM"
    elif "FOB" in b_tier_key: b_tier_key = "EXPORT_FOB"
    elif "CIF" in b_tier_key: b_tier_key = "DESTINATION_CIF"
    elif "BENCHMARK" in b_tier_key or "GLOBAL" in b_tier_key: b_tier_key = "GLOBAL_BENCHMARK"

    if "CIF" in s_tier_key: s_tier_key = "DESTINATION_CIF"
    elif "BENCHMARK" in s_tier_key or "GLOBAL" in s_tier_key: s_tier_key = "GLOBAL_BENCHMARK"
    elif "FOB" in s_tier_key: s_tier_key = "EXPORT_FOB"
    elif "FARM" in s_tier_key: s_tier_key = "DOMESTIC_FARM"

    buy_bm = tier_map.get(b_tier_key) or benchmarks[-1]
    sell_bm = tier_map.get(s_tier_key) or benchmarks[0]

    buy_price = float(buy_bm.get("price_usd_mt", 0))
    sell_price = float(sell_bm.get("price_usd_mt", 0))

    try:
        freight = float(estimated_freight_usd)
    except Exception:
        freight = 80.0

    gross_spread = sell_price - buy_price
    net_spread = gross_spread - freight
    net_margin_pct = round((net_spread / buy_price) * 100, 2) if buy_price > 0 else 0.0

    viable = net_spread > 0 and net_margin_pct >= 4.0

    recommendation = (
        f"Biên lợi nhuận ròng hấp dẫn (+{net_margin_pct}%), khuyến nghị lập RFQ mua nội địa và chào bán quốc tế ngay."
        if viable else
        f"Biên lợi nhuận mỏng ({net_margin_pct}%) hoặc rủi ro cước tàu cao, cần đàm phán giảm giá đầu vào tối thiểu {abs(round(net_spread, 1))} USD/MT."
    )

    return {
        "ok": True,
        "commodity_id": comm.get("commodity_id"),
        "commodity_name": comm.get("commodity_name"),
        "hs_code": comm.get("hs_code"),
        "buy_leg": {
            "tier": buy_bm.get("tier_type"),
            "exchange": buy_bm.get("exchange_name"),
            "price_usd_mt": buy_price,
            "original_quote": buy_bm.get("price_original")
        },
        "sell_leg": {
            "tier": sell_bm.get("tier_type"),
            "exchange": sell_bm.get("exchange_name"),
            "price_usd_mt": sell_price,
            "original_quote": sell_bm.get("price_original")
        },
        "freight_logistics_usd_mt": freight,
        "gross_spread_usd_mt": round(gross_spread, 2),
        "net_spread_usd_mt": round(net_spread, 2),
        "net_margin_percent": net_margin_pct,
        "arbitrage_viable": viable,
        "recommendation": recommendation
    }
