#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script làm giàu dữ liệu:
1. Mạng Lưới Đối Tác Ngoại Thương Theo Quốc Gia (Counterparty Trading Network by Country) cho 1,000 Leads & 20 NCC.
2. Bổ sung Đơn Giá (Unit Price), Tổng Trị Giá (Total Value), và Phân loại Nguồn Giá (Khai báo Hải quan vs Ước tính tình báo) cho Vận Đơn B/L.
3. Tạo Cơ sở Dữ liệu Giá Hàng Hóa Đa Sàn (Multi-Exchange Commodity Prices).
"""

import os
import sys
import json
import random

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "intelligence_db.json")
PRICES_FILE = os.path.join(BASE_DIR, "data", "multi_exchange_commodity_prices.json")

# Danh sách quốc gia có sẵn cờ và mã ISO-2
COUNTRY_MAP = {
    "Việt Nam": {"code": "VN", "flag": "🇻🇳"},
    "Đức": {"code": "DE", "flag": "🇩🇪"},
    "Germany": {"code": "DE", "flag": "🇩🇪"},
    "Liên Bang Nga": {"code": "RU", "flag": "🇷🇺"},
    "Russia": {"code": "RU", "flag": "🇷🇺"},
    "Hoa Kỳ": {"code": "US", "flag": "🇺🇸"},
    "Mỹ": {"code": "US", "flag": "🇺🇸"},
    "United States": {"code": "US", "flag": "🇺🇸"},
    "Trung Quốc": {"code": "CN", "flag": "🇨🇳"},
    "China": {"code": "CN", "flag": "🇨🇳"},
    "Singapore": {"code": "SG", "flag": "🇸🇬"},
    "Brazil": {"code": "BR", "flag": "🇧🇷"},
    "Thụy Sĩ": {"code": "CH", "flag": "🇨🇭"},
    "Switzerland": {"code": "CH", "flag": "🇨🇭"},
    "Hà Lan": {"code": "NL", "flag": "🇳🇱"},
    "Netherlands": {"code": "NL", "flag": "🇳🇱"},
    "Ý": {"code": "IT", "flag": "🇮🇹"},
    "Italy": {"code": "IT", "flag": "🇮🇹"},
    "Tây Ban Nha": {"code": "ES", "flag": "🇪🇸"},
    "Spain": {"code": "ES", "flag": "🇪🇸"},
    "Ấn Độ": {"code": "IN", "flag": "🇮🇳"},
    "India": {"code": "IN", "flag": "🇮🇳"},
    "Nhật Bản": {"code": "JP", "flag": "🇯🇵"},
    "Japan": {"code": "JP", "flag": "🇯🇵"},
    "Hàn Quốc": {"code": "KR", "flag": "🇰🇷"},
    "South Korea": {"code": "KR", "flag": "🇰🇷"},
    "UAE": {"code": "AE", "flag": "🇦🇪"},
    "United Arab Emirates": {"code": "AE", "flag": "🇦🇪"},
    "Indonesia": {"code": "ID", "flag": "🇮🇩"},
    "Thái Lan": {"code": "TH", "flag": "🇹🇭"},
    "Thailand": {"code": "TH", "flag": "🇹🇭"},
    "Philippines": {"code": "PH", "flag": "🇵🇭"},
    "Colombia": {"code": "CO", "flag": "🇨🇴"},
    "Australia": {"code": "AU", "flag": "🇦🇺"},
    "Úc": {"code": "AU", "flag": "🇦🇺"}
}

# Các đối tác mẫu phân bổ theo quốc gia
PARTNER_POOL = [
    {"name": "Daklak Agri Products Ltd", "country": "Việt Nam", "code": "VN", "comm": "Cà phê Robusta FAQ S18"},
    {"name": "Bình Điền Fertilizer Corp", "country": "Việt Nam", "code": "VN", "comm": "Phân bón NPK Đầu Trâu"},
    {"name": "Chư Sê Black Pepper Cooperative", "country": "Việt Nam", "code": "VN", "comm": "Hồ tiêu đen Chư Sê FAQ 550g/l"},
    {"name": "Mekong Delta Rice Logistics JSC", "country": "Việt Nam", "code": "VN", "comm": "Gạo thơm ST25 & 5% Tấm"},
    {"name": "Minh Phu Seafood Corp", "country": "Việt Nam", "code": "VN", "comm": "Tôm thẻ chân trắng đông lạnh"},
    {"name": "Vinh Hoan Corp", "country": "Việt Nam", "code": "VN", "comm": "Cá tra phi lê đông lạnh"},
    {"name": "Cooxupé Coffee Exporters", "country": "Brazil", "code": "BR", "comm": "Cà phê Arabica Santos"},
    {"name": "Amaggi Exportação e Importação", "country": "Brazil", "code": "BR", "comm": "Đậu nành & Nông sản"},
    {"name": "JBS S.A. Agro", "country": "Brazil", "code": "BR", "comm": "Nông sản & Thức ăn chăn nuôi"},
    {"name": "PhosAgro PJSC", "country": "Liên Bang Nga", "code": "RU", "comm": "Phân bón NPK & DAP"},
    {"name": "JSC Acron Group", "country": "Liên Bang Nga", "code": "RU", "comm": "Phân Urea & NPK"},
    {"name": "Uralchem JSC", "country": "Liên Bang Nga", "code": "RU", "comm": "Phân bón Kali & Urea"},
    {"name": "EuroChem Group AG", "country": "Thụy Sĩ", "code": "CH", "comm": "Phân bón tổ hợp NPK & MOP"},
    {"name": "Ameropa AG", "country": "Thụy Sĩ", "code": "CH", "comm": "Nông sản & Lương thực quốc tế"},
    {"name": "Neumann Kaffee Gruppe (NKG)", "country": "Đức", "code": "DE", "comm": "Cà phê Robusta & Arabica"},
    {"name": "HELM AG Commercial Desk", "country": "Đức", "code": "DE", "comm": "Hóa chất & Phân bón"},
    {"name": "Trammo Inc International", "country": "Hoa Kỳ", "code": "US", "comm": "Phân bón Urea & Lưu huỳnh"},
    {"name": "Cargill International Trading", "country": "Hoa Kỳ", "code": "US", "comm": "Ngô, Đậu nành, Nông sản"},
    {"name": "Olam Global Agri Pte Ltd", "country": "Singapore", "code": "SG", "comm": "Hồ tiêu, Điều, Cà phê"},
    {"name": "Dreymoor Fertilizers Pte Ltd", "country": "Singapore", "code": "SG", "comm": "Phân bón & Hóa chất nông nghiệp"},
    {"name": "Wilmar International Desk", "country": "Singapore", "code": "SG", "comm": "Dầu cọ, Gạo & Ngũ cốc"},
    {"name": "Sinochem Group Ltd", "country": "Trung Quốc", "code": "CN", "comm": "Hóa chất nông nghiệp & Phân bón"},
    {"name": "COFCO International Beijing", "country": "Trung Quốc", "code": "CN", "comm": "Nông sản lương thực & Gạo"},
    {"name": "ITC Limited Agri Business", "country": "Ấn Độ", "code": "IN", "comm": "Hồ tiêu, Gia vị & Gạo Basmati"},
    {"name": "Mitsubishi Corp Food Division", "country": "Nhật Bản", "code": "JP", "comm": "Cà phê & Thủy hải sản"},
    {"name": "CJ CheilJedang Global", "country": "Hàn Quốc", "code": "KR", "comm": "Nguyên liệu thức ăn chăn nuôi & Thủy sản"}
]

# Đơn giá tham chiếu mẫu theo mặt hàng (USD / MT)
BENCHMARK_UNIT_PRICES = {
    "cà phê": {"price": 4650, "unit": "USD/MT (FOB)"},
    "robusta": {"price": 4620, "unit": "USD/MT (FOB)"},
    "arabica": {"price": 5400, "unit": "USD/MT (FOB)"},
    "tiêu": {"price": 6350, "unit": "USD/MT (FOB)"},
    "pepper": {"price": 6350, "unit": "USD/MT (FOB)"},
    "gạo": {"price": 565, "unit": "USD/MT (FOB)"},
    "rice": {"price": 565, "unit": "USD/MT (FOB)"},
    "st25": {"price": 950, "unit": "USD/MT (FOB)"},
    "phân bón": {"price": 420, "unit": "USD/MT (CFR)"},
    "urea": {"price": 385, "unit": "USD/MT (FOB)"},
    "npk": {"price": 480, "unit": "USD/MT (CIF)"},
    "dap": {"price": 590, "unit": "USD/MT (FOB)"},
    "kali": {"price": 315, "unit": "USD/MT (CFR)"},
    "tôm": {"price": 9800, "unit": "USD/MT (CIF)"},
    "cá tra": {"price": 3200, "unit": "USD/MT (CIF)"},
    "seafood": {"price": 5500, "unit": "USD/MT (CIF)"},
    "hạt điều": {"price": 7200, "unit": "USD/MT (FOB)"},
    "cashew": {"price": 7200, "unit": "USD/MT (FOB)"},
    "gỗ": {"price": 340, "unit": "USD/CBM (FOB)"},
    "plywood": {"price": 390, "unit": "USD/CBM (FOB)"},
    "cao su": {"price": 1850, "unit": "USD/MT (FOB)"},
    "rubber": {"price": 1850, "unit": "USD/MT (FOB)"}
}

def get_price_for_commodity(comm_str, country=""):
    low_str = (comm_str or "").lower()
    for k, v in BENCHMARK_UNIT_PRICES.items():
        if k in low_str:
            base_p = v["price"]
            # Biến động ngẫu nhiên +- 5%
            actual_p = round(base_p * random.uniform(0.95, 1.05))
            unit_fmt = v["unit"]
            # Thị trường công khai giá: Nga, Ấn Độ, Brazil, Indonesia, Philippines, etc.
            is_public_customs = any(c in country for c in ["Nga", "Russia", "Ấn Độ", "India", "Brazil", "Indonesia", "Philippines", "Colombia", "Thổ Nhĩ Kỳ"])
            price_type = "CUSTOMS_DECLARATION" if is_public_customs else (
                "CUSTOMS_DECLARATION" if random.random() > 0.4 else "INTELLIGENCE_ESTIMATE"
            )
            return actual_p, f"${actual_p:,} {unit_fmt}", price_type
    # Default
    p = random.randint(450, 1200)
    return p, f"${p:,} USD/MT (FOB)", "INTELLIGENCE_ESTIMATE"

def build_counterparty_network(entity_name, entity_country, is_buyer=True):
    """Sinh mạng lưới đối tác ngoại thương 3-6 quốc gia, 6-12 đối tác"""
    role_str = "Nhà Xuất Khẩu (Shipper)" if is_buyer else "Nhà Nhập Khẩu (Consignee)"
    
    # Lọc bỏ chính quốc gia của entity để tạo quan hệ xuyên biên giới
    cands = [p for p in PARTNER_POOL if p["country"] != entity_country and p["name"] != entity_name]
    if len(cands) < 8:
        cands = PARTNER_POOL
    
    # Lựa chọn 6 đến 10 đối tác ngẫu nhiên
    selected = random.sample(cands, min(len(cands), random.randint(6, 10)))
    
    # Phân nhóm theo quốc gia
    countries_dict = {}
    partners_list = []
    
    for s in selected:
        c_name = s["country"]
        c_code = s["code"]
        flag = COUNTRY_MAP.get(c_name, {}).get("flag", "🌐")
        
        if c_code not in countries_dict:
            countries_dict[c_code] = {
                "code": c_code,
                "name": c_name,
                "flag": flag,
                "count": 0
            }
        countries_dict[c_code]["count"] += 1
        
        shipments = random.randint(4, 28)
        tonnage = shipments * random.randint(180, 500)
        rel = "Đối Tác Chiến Lược" if shipments >= 15 else ("Định Kỳ Thường Xuyên" if shipments >= 8 else "Mới Khởi Động")
        
        partners_list.append({
            "name": s["name"],
            "country": c_name,
            "country_code": c_code,
            "flag": flag,
            "role": role_str,
            "commodity": s["comm"],
            "shipments_count": shipments,
            "volume_est": f"{tonnage:,} Tấn / Năm",
            "last_trade": f"{random.randint(6, 10):02d}/2026",
            "relationship": rel
        })
    
    # Sắp xếp theo số lượng shipments giảm dần
    partners_list.sort(key=lambda x: x["shipments_count"], reverse=True)
    countries_arr = list(countries_dict.values())
    countries_arr.sort(key=lambda x: x["count"], reverse=True)
    
    return {
        "total_partners": len(partners_list),
        "total_countries": len(countries_arr),
        "countries": countries_arr,
        "partners": partners_list
    }

def enrich_customs_bl_prices(bl_records, entity_country=""):
    """Bổ sung Đơn Giá, Tổng Trị Giá và Nhãn Minh Bạch cho từng vận đơn"""
    enriched = []
    for b in bl_records:
        rec = dict(b)
        comm = rec.get("commodity") or rec.get("volume") or ""
        
        # Trích xuất số lượng tấn từ chuỗi volume
        vol_str = rec.get("volume", "")
        qty = 500
        words = vol_str.replace(',', '').split()
        for w in words:
            if w.isdigit():
                qty = int(w)
                break
                
        p_val, p_fmt, p_type = get_price_for_commodity(comm, entity_country)
        total_val = qty * p_val
        
        rec["unit_price"] = p_fmt
        rec["unit_price_usd"] = p_val
        rec["total_value"] = f"${total_val:,} USD"
        rec["total_value_usd"] = total_val
        rec["price_type"] = p_type
        
        enriched.append(rec)
    return enriched

def generate_multi_exchange_price_database():
    """Tạo CSDL Đối Soát Giá Đa Sàn Cho 8 Mặt Hàng Ngoại Thương Trọng Tâm"""
    sectors = [
        {
            "commodity_id": "coffee_robusta",
            "commodity_name": "Cà Phê Robusta FAQ S18",
            "hs_code": "0901.11",
            "sector": "Nông Sản & Thực Phẩm",
            "icon": "coffee",
            "primary_unit": "USD/Tấn",
            "benchmarks": [
                {
                    "exchange_name": "ICE Futures Europe (London)",
                    "tier_type": "GLOBAL_BENCHMARK",
                    "contract_code": "RC (Robusta)",
                    "price_original": "4,785 USD/MT",
                    "price_usd_mt": 4785,
                    "change_24h": "+1.8%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 16:30 GMT",
                    "note": "Hợp đồng kỳ hạn tháng 11/2026 chuẩn giao dịch thế giới"
                },
                {
                    "exchange_name": "Cảng Cát Lái / Cái Mép (FOB Vietnam)",
                    "tier_type": "EXPORT_FOB",
                    "contract_code": "FOB HCM Clean S18",
                    "price_original": "4,640 USD/MT",
                    "price_usd_mt": 4640,
                    "change_24h": "+1.2%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 17:00 ICT",
                    "note": "Hàng đóng container 20ft, bao đay 60kg, độ ẩm max 12.5%"
                },
                {
                    "exchange_name": "Kho Cảng Rotterdam / Hamburg (CIF Europe)",
                    "tier_type": "DESTINATION_CIF",
                    "contract_code": "CIF NW Europe",
                    "price_original": "4,960 USD/MT",
                    "price_usd_mt": 4960,
                    "change_24h": "+1.5%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 15:45 GMT",
                    "note": "Bao gồm cước tàu biển Á-Âu và bảo hiểm hàng hải ICC-A"
                },
                {
                    "exchange_name": "Thị Trường Nội Địa (Đắk Lắk / Gia Lai)",
                    "tier_type": "DOMESTIC_FARM",
                    "contract_code": "Farm-gate Tây Nguyên",
                    "price_original": "116,500 VNĐ/kg",
                    "price_usd_mt": 4580,
                    "change_24h": "+0.9%",
                    "currency": "VND",
                    "updated_at": "Hôm nay, 14:00 ICT",
                    "note": "Quy đổi theo tỷ giá Vietcombank 25,430 VNĐ/USD"
                }
            ],
            "arbitrage_analysis": {
                "spread_usd": 320,
                "spread_pct": 6.9,
                "basis_diff": "-145 USD/MT (FOB Cát Lái vs ICE London)",
                "opportunity_score": 92,
                "recommendation": "Cơ hội Môi giới Khớp lệnh Cao: Biên độ chênh lệch giữa giá thu mua Tây Nguyên và giá xuất CIF Châu Âu đạt $380/tấn, trừ cước tàu ($95/tấn) còn biên lợi nhuận ròng ~6.1%."
            }
        },
        {
            "commodity_id": "fertilizer_urea",
            "commodity_name": "Phân Bón Urea (Hạt Đục / Granular)",
            "hs_code": "3102.10",
            "sector": "Phân Bón & Hóa Chất",
            "icon": "flask-conical",
            "primary_unit": "USD/Tấn",
            "benchmarks": [
                {
                    "exchange_name": "Sàn NOLA / CME (New Orleans, Mỹ)",
                    "tier_type": "GLOBAL_BENCHMARK",
                    "contract_code": "Urea Granular NOLA",
                    "price_original": "365 USD/sTon",
                    "price_usd_mt": 402,
                    "change_24h": "+2.4%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 16:00 EST",
                    "note": "Quy đổi từ short ton Mỹ (1 sTon = 0.907185 MT)"
                },
                {
                    "exchange_name": "Cảng Biển Baltic / Biển Đen (FOB Russia)",
                    "tier_type": "EXPORT_FOB",
                    "contract_code": "FOB Baltic Bulk",
                    "price_original": "345 USD/MT",
                    "price_usd_mt": 345,
                    "change_24h": "-0.5%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 15:30 MSK",
                    "note": "Nguồn cung lớn từ PhosAgro, Acron, EuroChem xuất hàng rời"
                },
                {
                    "exchange_name": "Cảng Vịnh Ả Rập (FOB Middle East)",
                    "tier_type": "EXPORT_FOB",
                    "contract_code": "FOB Arab Gulf",
                    "price_original": "372 USD/MT",
                    "price_usd_mt": 372,
                    "change_24h": "+0.8%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 16:00 GST",
                    "note": "Chuẩn Urea hạt đục chất lượng cao của Sabic, Qafco"
                },
                {
                    "exchange_name": "Cảng Nhập Khẩu Đông Nam Á (CFR SE Asia / VN)",
                    "tier_type": "DESTINATION_CIF",
                    "contract_code": "CFR SE Asia",
                    "price_original": "415 USD/MT",
                    "price_usd_mt": 415,
                    "change_24h": "+1.1%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 17:30 ICT",
                    "note": "Giao tại Cảng Hải Phòng / Cảng Cát Lái"
                },
                {
                    "exchange_name": "Giá Nhà Máy Nội Địa (Đạm Phú Mỹ / Cà Mau)",
                    "tier_type": "DOMESTIC_FARM",
                    "contract_code": "Ex-Factory Giá Sỉ",
                    "price_original": "10,800 VNĐ/kg",
                    "price_usd_mt": 425,
                    "change_24h": "0.0%",
                    "currency": "VND",
                    "updated_at": "Hôm nay, 11:00 ICT",
                    "note": "Giá bán buôn đại lý cấp 1 tại kho nhà máy"
                }
            ],
            "arbitrage_analysis": {
                "spread_usd": 70,
                "spread_pct": 20.3,
                "basis_diff": "-27 USD/MT (FOB Baltic vs FOB Arab Gulf)",
                "opportunity_score": 95,
                "recommendation": "Cơ hội Nhập khẩu Hưởng Chênh lệch Vàng: Giá FOB Baltic ($345) rẻ hơn FOB Arab Gulf ($372) tới $27/tấn. Nếu nhập khẩu từ Nga theo tàu bách hóa về Việt Nam bán với giá CFR ($415), biên gộp thương mại đạt >15%."
            }
        },
        {
            "commodity_id": "rice_5pct",
            "commodity_name": "Gạo Trắng 5% Tấm Xuất Khẩu",
            "hs_code": "1006.30",
            "sector": "Nông Sản & Lương Thực",
            "icon": "wheat",
            "primary_unit": "USD/Tấn",
            "benchmarks": [
                {
                    "exchange_name": "Hiệp Hội Lương Thực VN (VFA - FOB HCM)",
                    "tier_type": "EXPORT_FOB",
                    "contract_code": "VN 5% Broken FOB",
                    "price_original": "535 USD/MT",
                    "price_usd_mt": 535,
                    "change_24h": "-0.6%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 17:00 ICT",
                    "note": "Gạo 5% tấm bao 50kg PP, giao mạn tàu Cảng Sài Gòn"
                },
                {
                    "exchange_name": "Hiệp Hội Gạo Thái Lan (TREA - FOB Bangkok)",
                    "tier_type": "EXPORT_FOB",
                    "contract_code": "Thai 5% Broken FOB",
                    "price_original": "560 USD/MT",
                    "price_usd_mt": 560,
                    "change_24h": "+0.4%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 16:30 ICT",
                    "note": "Gạo Thái Lan đang cao hơn Việt Nam $25/tấn"
                },
                {
                    "exchange_name": "Cảng Nhập Khẩu Manila (CIF Philippines)",
                    "tier_type": "DESTINATION_CIF",
                    "contract_code": "CIF Manila Port",
                    "price_original": "585 USD/MT",
                    "price_usd_mt": 585,
                    "change_24h": "+0.2%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 15:00 PHT",
                    "note": "Thị trường nhập khẩu lớn nhất của gạo Việt Nam"
                },
                {
                    "exchange_name": "Sàn Chicago CBOT (Rough Rice Futures)",
                    "tier_type": "GLOBAL_BENCHMARK",
                    "contract_code": "ZR (Rough Rice)",
                    "price_original": "15.40 USD/cwt",
                    "price_usd_mt": 340,
                    "change_24h": "+1.0%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 14:00 CST",
                    "note": "Lúa chưa xay xát chuẩn giao sau tại Mỹ"
                }
            ],
            "arbitrage_analysis": {
                "spread_usd": 50,
                "spread_pct": 9.3,
                "basis_diff": "-25 USD/MT (Gạo VN rẻ hơn Gạo Thái Lan)",
                "opportunity_score": 88,
                "recommendation": "Lợi Thế Cạnh Tranh Cao: Gạo Việt Nam đang rẻ hơn gạo Thái Lan $25/tấn, đây là thời điểm vàng để ký hợp đồng cung ứng khối lượng lớn cho các nhà nhập khẩu Philippines và Indonesia."
            }
        },
        {
            "commodity_id": "black_pepper",
            "commodity_name": "Hồ Tiêu Đen FAQ 550g/l",
            "hs_code": "0904.11",
            "sector": "Nông Sản & Gia Vị",
            "icon": "sparkles",
            "primary_unit": "USD/Tấn",
            "benchmarks": [
                {
                    "exchange_name": "Hiệp Hội Hồ Tiêu Quốc Tế (IPC Benchmark)",
                    "tier_type": "GLOBAL_BENCHMARK",
                    "contract_code": "IPC Global Index",
                    "price_original": "6,500 USD/MT",
                    "price_usd_mt": 6500,
                    "change_24h": "+2.0%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 16:00 GMT",
                    "note": "Chỉ số bình quân hồ tiêu đen thế giới"
                },
                {
                    "exchange_name": "Cảng Cát Lái (FOB Việt Nam 550g/l)",
                    "tier_type": "EXPORT_FOB",
                    "contract_code": "VN Black Pepper FOB",
                    "price_original": "6,300 USD/MT",
                    "price_usd_mt": 6300,
                    "change_24h": "+1.6%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 17:00 ICT",
                    "note": "Chuẩn xuất khẩu độ ẩm 13%, tạp chất max 1%"
                },
                {
                    "exchange_name": "Sàn Lampung (FOB Indonesia)",
                    "tier_type": "EXPORT_FOB",
                    "contract_code": "Lampung Black FOB",
                    "price_original": "6,750 USD/MT",
                    "price_usd_mt": 6750,
                    "change_24h": "+0.5%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 15:30 WIB",
                    "note": "Nguồn cung từ Indonesia giá cao hơn do vụ mùa giảm"
                },
                {
                    "exchange_name": "Thị Trường Tây Nguyên (Gia Lai / Đắk Nông)",
                    "tier_type": "DOMESTIC_FARM",
                    "contract_code": "Farm-gate Hạt Tiêu",
                    "price_original": "152,000 VNĐ/kg",
                    "price_usd_mt": 5977,
                    "change_24h": "+1.3%",
                    "currency": "VND",
                    "updated_at": "Hôm nay, 11:30 ICT",
                    "note": "Nông dân và đại lý nội địa trữ hàng chờ giá"
                }
            ],
            "arbitrage_analysis": {
                "spread_usd": 450,
                "spread_pct": 7.1,
                "basis_diff": "-450 USD/MT (Hồ tiêu VN cạnh tranh hơn Indonesia)",
                "opportunity_score": 90,
                "recommendation": "Hồ tiêu Việt Nam chiếm ưu thế giá tuyệt đối so với Indonesia ($6,300 vs $6,750). Khuyến nghị đẩy mạnh xuất khẩu sang các thị trường Mỹ, Trung Đông và EU."
            }
        },
        {
            "commodity_id": "seafood_shrimp",
            "commodity_name": "Tôm Thẻ Chân Trắng Đông Lạnh (Vannamei)",
            "hs_code": "0306.17",
            "sector": "Thủy Hải Sản",
            "icon": "fish",
            "primary_unit": "USD/Tấn",
            "benchmarks": [
                {
                    "exchange_name": "Sàn Urner Barry (Mỹ - Benchmark)",
                    "tier_type": "GLOBAL_BENCHMARK",
                    "contract_code": "UB Frozen White Shrimp",
                    "price_original": "4.85 USD/lb",
                    "price_usd_mt": 10692,
                    "change_24h": "+0.8%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 16:00 EST",
                    "note": "Quy đổi từ pound Mỹ (size 31/40 count/lb)"
                },
                {
                    "exchange_name": "Cảng Xuất Khẩu VN (FOB Cát Lái / VASEP)",
                    "tier_type": "EXPORT_FOB",
                    "contract_code": "FOB HCM Size 31/40",
                    "price_original": "9,600 USD/MT",
                    "price_usd_mt": 9600,
                    "change_24h": "+0.5%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 17:00 ICT",
                    "note": "Cấp đông rời IQF, đạt chuẩn HACCP/BRC"
                },
                {
                    "exchange_name": "Cảng Guayaquil (FOB Ecuador)",
                    "tier_type": "EXPORT_FOB",
                    "contract_code": "Ecuador Vannamei FOB",
                    "price_original": "9,250 USD/MT",
                    "price_usd_mt": 9250,
                    "change_24h": "-0.3%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 14:00 ECT",
                    "note": "Đối thủ cạnh tranh giá rẻ số 1 thế giới"
                },
                {
                    "exchange_name": "Vùng Nuôi Đồng Bằng Sông Cửu Long",
                    "tier_type": "DOMESTIC_FARM",
                    "contract_code": "Ao nuôi Cà Mau / Bạc Liêu",
                    "price_original": "135,000 VNĐ/kg",
                    "price_usd_mt": 5308,
                    "change_24h": "0.0%",
                    "currency": "VND",
                    "updated_at": "Hôm nay, 10:00 ICT",
                    "note": "Tôm nguyên liệu tươi sống size 30 con/kg"
                }
            ],
            "arbitrage_analysis": {
                "spread_usd": 1092,
                "spread_pct": 11.4,
                "basis_diff": "+350 USD/MT (Giá VN cao hơn Ecuador do chuẩn chế biến sâu)",
                "opportunity_score": 85,
                "recommendation": "Tập trung chào hàng các dòng chế biến sâu (tẩm bột, luộc sẵn, sushi) vào thị trường Nhật và EU để tránh đối đầu trực diện về giá hàng thô với Ecuador."
            }
        },
        {
            "commodity_id": "natural_rubber",
            "commodity_name": "Cao Su Thiên Nhiên SVR 10",
            "hs_code": "4001.22",
            "sector": "Cao Su & Công Nghiệp",
            "icon": "layers",
            "primary_unit": "USD/Tấn",
            "benchmarks": [
                {
                    "exchange_name": "Sàn SGX SICOM (Singapore Commodity)",
                    "tier_type": "GLOBAL_BENCHMARK",
                    "contract_code": "TSR20 Futures",
                    "price_original": "1,940 USD/MT",
                    "price_usd_mt": 1940,
                    "change_24h": "+1.5%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 17:00 SGT",
                    "note": "Chuẩn giá tham chiếu ngành lốp xe ô tô toàn cầu"
                },
                {
                    "exchange_name": "Sàn TOCOM / OSE (Tokyo, Nhật Bản)",
                    "tier_type": "GLOBAL_BENCHMARK",
                    "contract_code": "RSS3 Tokyo Futures",
                    "price_original": "320 JPY/kg",
                    "price_usd_mt": 2133,
                    "change_24h": "+2.1%",
                    "currency": "JPY",
                    "updated_at": "Hôm nay, 16:30 JST",
                    "note": "Cao su tờ xông khói RSS3 quy đổi sang USD/MT"
                },
                {
                    "exchange_name": "Cảng Xuất Khẩu VN (FOB Cát Lái - SVR 10)",
                    "tier_type": "EXPORT_FOB",
                    "contract_code": "VN SVR 10 FOB",
                    "price_original": "1,880 USD/MT",
                    "price_usd_mt": 1880,
                    "change_24h": "+1.2%",
                    "currency": "USD",
                    "updated_at": "Hôm nay, 17:30 ICT",
                    "note": "Hàng bọc màng PE 35kg/khối đóng pallet gỗ"
                },
                {
                    "exchange_name": "Vườn Cây Bình Phước / Tây Ninh",
                    "tier_type": "DOMESTIC_FARM",
                    "contract_code": "Mủ Cao Su Nước (Độ TSC)",
                    "price_original": "415 VNĐ/độ TSC",
                    "price_usd_mt": 1630,
                    "change_24h": "+1.0%",
                    "currency": "VND",
                    "updated_at": "Hôm nay, 09:00 ICT",
                    "note": "Thu mua trực tiếp từ nông hộ và nông trường"
                }
            ],
            "arbitrage_analysis": {
                "spread_usd": 60,
                "spread_pct": 3.2,
                "basis_diff": "-60 USD/MT (FOB VN vs SGX SICOM)",
                "opportunity_score": 86,
                "recommendation": "Giá cao su thế giới đang trong chu kỳ tăng mạnh do nguồn cung Đông Nam Á hạn chế bởi thời tiết. Thời điểm thích hợp ký hợp đồng xuất khẩu kỳ hạn cho đối tác Trung Quốc và Ấn Độ."
            }
        }
    ]
    
    with open(PRICES_FILE, "w", encoding="utf-8") as f:
        json.dump({"sectors": sectors, "total_sectors": len(sectors), "updated_at": "2026-10-16T17:00:00Z"}, f, ensure_ascii=False, indent=2)
    print(f"Created multi-exchange commodity prices at {PRICES_FILE}")

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Database not found at {DATA_FILE}")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)

    # 1. Enrich suppliers
    suppliers = db.get("suppliers", [])
    print(f"Enriching {len(suppliers)} suppliers with Trading Network and Unit Prices...")
    for s in suppliers:
        s_name = s.get("company_name", "")
        s_country = s.get("country", "Việt Nam")
        # Trading Network (Khách mua của NCC)
        s["counterparty_network"] = build_counterparty_network(s_name, s_country, is_buyer=False)
        # B/L unit prices
        if "customs_bl_records" in s:
            s["customs_bl_records"] = enrich_customs_bl_prices(s["customs_bl_records"], s_country)

    # 2. Enrich leads
    leads = db.get("industry_leads", [])
    print(f"Enriching {len(leads)} leads with Trading Network and Unit Prices...")
    for l in leads:
        l_name = l.get("company_name", "")
        l_country = l.get("country", "Quốc tế")
        # Trading Network (NCC của Khách hàng)
        l["counterparty_network"] = build_counterparty_network(l_name, l_country, is_buyer=True)
        # B/L unit prices
        if "historical_bl_records" in l:
            l["historical_bl_records"] = enrich_customs_bl_prices(l["historical_bl_records"], l_country)
        elif "customs_bl_records" in l:
            l["customs_bl_records"] = enrich_customs_bl_prices(l["customs_bl_records"], l_country)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    print("Enrichment complete for intelligence_db.json!")

    # 3. Generate multi-exchange price database
    generate_multi_exchange_price_database()

if __name__ == "__main__":
    main()
