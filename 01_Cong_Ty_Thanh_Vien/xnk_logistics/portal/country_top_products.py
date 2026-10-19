# -*- coding: utf-8 -*-
"""
Country Top Products & Multi-Year Market Dynamics Engine
Khối Xuất Nhập Khẩu & Thương Mại Quốc Tế — Tổng Hành Dinh

Cung cấp danh mục sản phẩm hàng đầu về quy mô, sản lượng và doanh thu xuất nhập khẩu
của các quốc gia trọng điểm: Việt Nam, Brazil, Indonesia, Hoa Kỳ, Trung Quốc, Ấn Độ, Nga, Thái Lan...
Đầy đủ các chu kỳ biến động giá: 24h, 7 ngày, 1 tháng, 6 tháng, 1 năm.
"""

COUNTRY_TOP_PRODUCTS = [
    # --- VIỆT NAM (VN) ---
    {
        "id": "vn-coffee-robusta",
        "commodity_id": "coffee_robusta",
        "product_name": "Cà Phê Robusta Đắk Lắk (Loại 2, S18)",
        "country": "Việt Nam",
        "country_code": "VN",
        "flag": "🇻🇳",
        "hs_code": "0901.11",
        "market_scale": "1.75 Triệu Tấn / $4.8 Tỷ USD",
        "metric_rank": "Top 1 Thế Giới",
        "price_usd_mt": 4785,
        "price_original": "4,785 USD/MT (121,500 đ/kg)",
        "exchange_name": "Sàn ICE London & FOB Cát Lái",
        "change_24h": "+1.8%",
        "change_7d": "+4.2%",
        "change_1m": "+7.5%",
        "change_6m": "+18.2%",
        "change_1y": "+31.1%",
        "category": "agri_food"
    },
    {
        "id": "vn-rice-st25",
        "commodity_id": "rice_st25",
        "product_name": "Gạo Trắng Xuất Khẩu 5% Tấm & Gạo ST25",
        "country": "Việt Nam",
        "country_code": "VN",
        "flag": "🇻🇳",
        "hs_code": "1006.30",
        "market_scale": "8.1 Triệu Tấn / $4.6 Tỷ USD",
        "metric_rank": "Top 2 Thế Giới",
        "price_usd_mt": 585,
        "price_original": "585 USD/MT (FOB Sài Gòn)",
        "exchange_name": "Hiệp Hội Lương Thực VN (VFA) & FOB Sài Gòn",
        "change_24h": "-0.8%",
        "change_7d": "-1.5%",
        "change_1m": "-2.8%",
        "change_6m": "+8.3%",
        "change_1y": "+14.7%",
        "category": "agri_food"
    },
    {
        "id": "vn-black-pepper",
        "commodity_id": "black_pepper",
        "product_name": "Hồ Tiêu Đen Chư Sê / Gia Lai (FAQ 500g/l)",
        "country": "Việt Nam",
        "country_code": "VN",
        "flag": "🇻🇳",
        "hs_code": "0904.11",
        "market_scale": "260,000 Tấn / $1.1 Tỷ USD",
        "metric_rank": "Top 1 Thế Giới",
        "price_usd_mt": 6800,
        "price_original": "6,800 USD/MT (172,000 đ/kg)",
        "exchange_name": "Hiệp Hội Hồ Tiêu VN (VPA) & IPC",
        "change_24h": "+2.2%",
        "change_7d": "+5.1%",
        "change_1m": "+11.4%",
        "change_6m": "+38.6%",
        "change_1y": "+64.5%",
        "category": "agri_food"
    },
    {
        "id": "vn-natural-rubber",
        "commodity_id": "natural_rubber",
        "product_name": "Cao Su Thiên Nhiên SVR 3L & SVR 10",
        "country": "Việt Nam",
        "country_code": "VN",
        "flag": "🇻🇳",
        "hs_code": "4001.22",
        "market_scale": "2.1 Triệu Tấn / $3.2 Tỷ USD",
        "metric_rank": "Top 3 Thế Giới",
        "price_usd_mt": 2420,
        "price_original": "2,420 USD/MT",
        "exchange_name": "Sàn SGX SICOM & Cảng Cái Mép",
        "change_24h": "+1.2%",
        "change_7d": "+2.8%",
        "change_1m": "+5.2%",
        "change_6m": "+19.4%",
        "change_1y": "+28.7%",
        "category": "industrial"
    },
    {
        "id": "vn-cashew-w320",
        "commodity_id": "cashew_w320",
        "product_name": "Hạt Điều Nhân Xuất Khẩu Loại W320 Bình Phước",
        "country": "Việt Nam",
        "country_code": "VN",
        "flag": "🇻🇳",
        "hs_code": "0801.32",
        "market_scale": "640,000 Tấn / $4.1 Tỷ USD",
        "metric_rank": "Top 1 Thế Giới",
        "price_usd_mt": 6850,
        "price_original": "3.11 USD/lbs (6,850 USD/MT)",
        "exchange_name": "Hiệp Hội Điều VN (VINACAS) & FOB HCM",
        "change_24h": "+0.5%",
        "change_7d": "+1.8%",
        "change_1m": "+3.9%",
        "change_6m": "+12.1%",
        "change_1y": "+16.8%",
        "category": "agri_food"
    },
    {
        "id": "vn-shrimp-seafood",
        "commodity_id": "seafood_shrimp",
        "product_name": "Tôm Thẻ Chân Trắng & Tôm Sú Đông Lạnh Cà Mau",
        "country": "Việt Nam",
        "country_code": "VN",
        "flag": "🇻🇳",
        "hs_code": "0306.17",
        "market_scale": "1.1 Triệu Tấn / $3.8 Tỷ USD",
        "metric_rank": "Top 3 Thế Giới",
        "price_usd_mt": 9200,
        "price_original": "9,200 USD/MT (FOB Cát Lái)",
        "exchange_name": "VASEP & CIF Tokyo / Rotterdam",
        "change_24h": "+0.7%",
        "change_7d": "+1.4%",
        "change_1m": "+2.9%",
        "change_6m": "+7.5%",
        "change_1y": "+11.2%",
        "category": "agri_food"
    },
    {
        "id": "vn-urea-fertilizer",
        "commodity_id": "fertilizer_urea",
        "product_name": "Phân Bón Urê Hạt Đục / Hạt Trong Phú Mỹ - Cà Mau",
        "country": "Việt Nam",
        "country_code": "VN",
        "flag": "🇻🇳",
        "hs_code": "3102.10",
        "market_scale": "2.6 Triệu Tấn / $950 Triệu USD",
        "metric_rank": "Top Xuất Khẩu ASEAN",
        "price_usd_mt": 365,
        "price_original": "365 USD/MT (9,300 đ/kg)",
        "exchange_name": "FOB Cảng Cái Mép & Biển Đen / Vịnh Ba Tư",
        "change_24h": "-1.4%",
        "change_7d": "-2.1%",
        "change_1m": "-4.5%",
        "change_6m": "+6.8%",
        "change_1y": "-12.3%",
        "category": "chemicals"
    },

    # --- BRAZIL (BR) ---
    {
        "id": "br-coffee-arabica",
        "commodity_id": "coffee_arabica",
        "product_name": "Cà Phê Arabica Santos (Brazil NY 2)",
        "country": "Brazil",
        "country_code": "BR",
        "flag": "🇧🇷",
        "hs_code": "0901.11",
        "market_scale": "3.8 Triệu Tấn / $9.2 Tỷ USD",
        "metric_rank": "Top 1 Thế Giới",
        "price_usd_mt": 5480,
        "price_original": "248.50 ¢/lb (5,480 USD/MT)",
        "exchange_name": "Sàn ICE Futures US (New York)",
        "change_24h": "+0.9%",
        "change_7d": "+3.1%",
        "change_1m": "+8.4%",
        "change_6m": "+24.5%",
        "change_1y": "+42.8%",
        "category": "agri_food"
    },
    {
        "id": "br-soybean",
        "commodity_id": "soybean",
        "product_name": "Đậu Nành Hạt Xuất Khẩu (Paranaguá FOB)",
        "country": "Brazil",
        "country_code": "BR",
        "flag": "🇧🇷",
        "hs_code": "1201.90",
        "market_scale": "103 Triệu Tấn / $53 Tỷ USD",
        "metric_rank": "Top 1 Thế Giới",
        "price_usd_mt": 435,
        "price_original": "435 USD/MT (FOB Paranaguá)",
        "exchange_name": "Sàn B3 Sao Paulo & CBOT Chicago",
        "change_24h": "-0.6%",
        "change_7d": "+1.2%",
        "change_1m": "-1.5%",
        "change_6m": "-5.8%",
        "change_1y": "-14.2%",
        "category": "agri_food"
    },
    {
        "id": "br-raw-sugar",
        "commodity_id": "raw_sugar",
        "product_name": "Đường Thô Hạng 11 (Sugar No. 11 Santos)",
        "country": "Brazil",
        "country_code": "BR",
        "flag": "🇧🇷",
        "hs_code": "1701.14",
        "market_scale": "32 Triệu Tấn / $18 Tỷ USD",
        "metric_rank": "Top 1 Thế Giới",
        "price_usd_mt": 485,
        "price_original": "22.10 ¢/lb (485 USD/MT)",
        "exchange_name": "Sàn ICE Futures US & FOB Santos",
        "change_24h": "+1.5%",
        "change_7d": "+3.8%",
        "change_1m": "+6.2%",
        "change_6m": "-2.4%",
        "change_1y": "+11.7%",
        "category": "agri_food"
    },

    # --- INDONESIA (ID) ---
    {
        "id": "id-cpo-palm-oil",
        "commodity_id": "cpo_palm_oil",
        "product_name": "Dầu Cọ Thô CPO (Crude Palm Oil Belawan)",
        "country": "Indonesia",
        "country_code": "ID",
        "flag": "🇮🇩",
        "hs_code": "1511.10",
        "market_scale": "48 Triệu Tấn / $34 Tỷ USD",
        "metric_rank": "Top 1 Thế Giới",
        "price_usd_mt": 965,
        "price_original": "4,320 MYR/MT (965 USD/MT)",
        "exchange_name": "Sàn Bursa Malaysia (BMD) & ICDX",
        "change_24h": "+1.1%",
        "change_7d": "+2.9%",
        "change_1m": "+5.8%",
        "change_6m": "+14.2%",
        "change_1y": "+21.5%",
        "category": "agri_food"
    },
    {
        "id": "id-thermal-coal",
        "commodity_id": "thermal_coal",
        "product_name": "Than Đá Nhiệt Điện (Thermal Coal ICI 4)",
        "country": "Indonesia",
        "country_code": "ID",
        "flag": "🇮🇩",
        "hs_code": "2701.12",
        "market_scale": "510 Triệu Tấn / $41 Tỷ USD",
        "metric_rank": "Top 1 Thế Giới",
        "price_usd_mt": 92,
        "price_original": "92 USD/MT (FOB Kalimantan)",
        "exchange_name": "Indonesian Coal Index & FOB Cảng",
        "change_24h": "-0.5%",
        "change_7d": "-1.1%",
        "change_1m": "-3.2%",
        "change_6m": "-11.5%",
        "change_1y": "-23.4%",
        "category": "minerals"
    },

    # --- HOA KỲ (US) ---
    {
        "id": "us-corn-cbot",
        "commodity_id": "corn_cbot",
        "product_name": "Ngô Bắp Vàng Hạng 2 (Corn No. 2 Yellow)",
        "country": "Hoa Kỳ",
        "country_code": "US",
        "flag": "🇺🇸",
        "hs_code": "1005.90",
        "market_scale": "385 Triệu Tấn / $14 Tỷ USD",
        "metric_rank": "Top 1 Thế Giới",
        "price_usd_mt": 178,
        "price_original": "425 ¢/bu (178 USD/MT)",
        "exchange_name": "Sàn CME Group (CBOT Chicago)",
        "change_24h": "+0.4%",
        "change_7d": "+1.1%",
        "change_1m": "+2.5%",
        "change_6m": "-7.8%",
        "change_1y": "-18.5%",
        "category": "agri_food"
    },
    {
        "id": "us-wheat-srw",
        "commodity_id": "wheat_srw",
        "product_name": "Lúa Mì Mùa Đông Đỏ Mềm (SRW Wheat CBOT)",
        "country": "Hoa Kỳ",
        "country_code": "US",
        "flag": "🇺🇸",
        "hs_code": "1001.99",
        "market_scale": "50 Triệu Tấn / $7.5 Tỷ USD",
        "metric_rank": "Top 3 Thế Giới",
        "price_usd_mt": 218,
        "price_original": "595 ¢/bu (218 USD/MT)",
        "exchange_name": "Sàn CME CBOT & FOB Gulf of Mexico",
        "change_24h": "-1.2%",
        "change_7d": "-0.5%",
        "change_1m": "+1.8%",
        "change_6m": "-4.2%",
        "change_1y": "-15.1%",
        "category": "agri_food"
    },

    # --- NGA (RU) ---
    {
        "id": "ru-wheat-milling",
        "commodity_id": "ru_wheat",
        "product_name": "Lúa Mì Thực Phẩm 12.5% Protein (Black Sea FOB)",
        "country": "Nga",
        "country_code": "RU",
        "flag": "🇷🇺",
        "hs_code": "1001.99",
        "market_scale": "53 Triệu Tấn / $12 Tỷ USD",
        "metric_rank": "Top 1 Thế Giới",
        "price_usd_mt": 235,
        "price_original": "235 USD/MT (FOB Novorossiysk)",
        "exchange_name": "Sàn MOEX & FOB Biển Đen",
        "change_24h": "+0.8%",
        "change_7d": "+1.7%",
        "change_1m": "+4.1%",
        "change_6m": "+8.9%",
        "change_1y": "-6.5%",
        "category": "agri_food"
    },
    {
        "id": "ru-potash-fertilizer",
        "commodity_id": "potash_fertilizer",
        "product_name": "Phân Bón Kali MOP (Muriate of Potash Uralkali)",
        "country": "Nga",
        "country_code": "RU",
        "flag": "🇷🇺",
        "hs_code": "3104.20",
        "market_scale": "14 Triệu Tấn / $4.2 Tỷ USD",
        "metric_rank": "Top 2 Thế Giới",
        "price_usd_mt": 295,
        "price_original": "295 USD/MT (FOB Baltic)",
        "exchange_name": "Uralkali & FOB St. Petersburg",
        "change_24h": "0.0%",
        "change_7d": "+0.5%",
        "change_1m": "-1.2%",
        "change_6m": "-8.5%",
        "change_1y": "-21.0%",
        "category": "chemicals"
    },

    # --- ẤN ĐỘ (IN) ---
    {
        "id": "in-basmati-rice",
        "commodity_id": "basmati_rice",
        "product_name": "Gạo Thơm Hạt Dài Basmati 1121 Pusa",
        "country": "Ấn Độ",
        "country_code": "IN",
        "flag": "🇮🇳",
        "hs_code": "1006.30",
        "market_scale": "5.2 Triệu Tấn / $5.4 Tỷ USD",
        "metric_rank": "Top 1 Thế Giới",
        "price_usd_mt": 980,
        "price_original": "980 USD/MT (FOB Mundra)",
        "exchange_name": "NCDEX Mumbai & FOB Mundra",
        "change_24h": "+1.4%",
        "change_7d": "+2.6%",
        "change_1m": "+4.8%",
        "change_6m": "+11.5%",
        "change_1y": "+18.9%",
        "category": "agri_food"
    },
    {
        "id": "in-cotton-shankar",
        "commodity_id": "cotton_shankar",
        "product_name": "Bông Xơ Tự Nhiên Shankar-6 (Cotton Gujarat)",
        "country": "Ấn Độ",
        "country_code": "IN",
        "flag": "🇮🇳",
        "hs_code": "5201.00",
        "market_scale": "6.1 Triệu Tấn / $8.1 Tỷ USD",
        "metric_rank": "Top 2 Thế Giới",
        "price_usd_mt": 1820,
        "price_original": "82.50 ¢/lb (1,820 USD/MT)",
        "exchange_name": "MCX Cotton & ICE Cotton No. 2",
        "change_24h": "-0.3%",
        "change_7d": "+0.8%",
        "change_1m": "+1.9%",
        "change_6m": "-5.2%",
        "change_1y": "-8.7%",
        "category": "textiles"
    },

    # --- THÁI LAN (TH) ---
    {
        "id": "th-jasmine-rice",
        "commodity_id": "jasmine_rice",
        "product_name": "Gạo Thơm Jasmine Hom Mali 100% Grade A",
        "country": "Thái Lan",
        "country_code": "TH",
        "flag": "🇹🇭",
        "hs_code": "1006.30",
        "market_scale": "8.8 Triệu Tấn / $5.2 Tỷ USD",
        "metric_rank": "Top 3 Thế Giới",
        "price_usd_mt": 860,
        "price_original": "860 USD/MT (FOB Bangkok)",
        "exchange_name": "Thai Rice Exporters Association (TREA)",
        "change_24h": "-0.2%",
        "change_7d": "+0.5%",
        "change_1m": "+1.2%",
        "change_6m": "+6.4%",
        "change_1y": "+15.3%",
        "category": "agri_food"
    },
    {
        "id": "th-rss1-rubber",
        "commodity_id": "rubber_rss1",
        "product_name": "Cao Su Hun Khói Tờ RSS 1 & RSS 3 (FOB Songkhla)",
        "country": "Thái Lan",
        "country_code": "TH",
        "flag": "🇹🇭",
        "hs_code": "4001.21",
        "market_scale": "4.8 Triệu Tấn / $6.9 Tỷ USD",
        "metric_rank": "Top 1 Thế Giới",
        "price_usd_mt": 2510,
        "price_original": "2,510 USD/MT",
        "exchange_name": "Rubber Authority of Thailand (RAOT) & SGX",
        "change_24h": "+1.5%",
        "change_7d": "+3.4%",
        "change_1m": "+6.8%",
        "change_6m": "+22.1%",
        "change_1y": "+32.4%",
        "category": "industrial"
    }
]

def get_country_top_products(country_code=None, category=None):
    """Lọc danh sách sản phẩm top theo quốc gia hoặc ngành hàng"""
    results = COUNTRY_TOP_PRODUCTS
    if country_code and country_code.upper() != "ALL":
        c_up = country_code.upper().strip()
        results = [p for p in results if p.get("country_code") == c_up]
    if category and category.upper() != "ALL":
        cat_low = category.lower().strip()
        results = [p for p in results if p.get("category") == cat_low]
    return results

def get_country_product_by_id_or_code(key):
    """Tìm sản phẩm theo id, commodity_id, hs_code hoặc từ khóa liên quan"""
    if not key:
        return None
    k_clean = str(key).strip().lower()
    for p in COUNTRY_TOP_PRODUCTS:
        if p.get("id", "").lower() == k_clean:
            return p
        if p.get("commodity_id", "").lower() == k_clean:
            return p
        hs = p.get("hs_code", "").lower()
        if hs == k_clean or hs.replace(".", "") == k_clean.replace(".", ""):
            return p
    return None
