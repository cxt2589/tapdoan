# -*- coding: utf-8 -*-
"""
HỆ THỐNG TÌNH BÁO HÃNG TÀU & VẬN TẢI QUỐC TẾ TẬP ĐOÀN
Bao gồm hơn 80+ Hãng tàu viễn dương, Hãng nội Á, Hãng tàu chuyên tuyến Nga & Á-Âu,
Tập đoàn Logistics NVOCC toàn cầu và Đội tàu container Việt Nam.
"""

import re

# BẢNG TỪ ĐIỂN 80+ HÃNG TÀU & TỔ CHỨC VẬN TẢI QUỐC TẾ (SCAC & BIC CODES)
CARRIER_REGISTRY = {
    # ========================================================
    # 1. KHỐI CHUYÊN TUYẾN LIÊN BANG NGA & Á - ÂU (RUSSIAN CORRIDORS)
    # ========================================================
    "FESU": {"name": "FESCO Transportation Group", "short": "FESCO", "country": "Russia", "hub": "Vladivostok / St. Petersburg", "type": "Nga - Chủ lực", "badge": "bg-rose-500/20 text-rose-300 border-rose-500/30"},
    "FESC": {"name": "FESCO Ocean Management", "short": "FESCO Lines", "country": "Russia", "hub": "Vladivostok / Novorossiysk", "type": "Nga - Chủ lực", "badge": "bg-rose-500/20 text-rose-300 border-rose-500/30"},
    "TRCU": {"name": "TransContainer PJSC (Delo Group)", "short": "TransContainer", "country": "Russia", "hub": "Moscow / Vladivostok", "type": "Nga - Đường sắt & Biển", "badge": "bg-amber-500/20 text-amber-300 border-amber-500/30"},
    "TRCO": {"name": "TransContainer Intermodal", "short": "TransContainer", "country": "Russia", "hub": "St. Petersburg / Vostochny", "type": "Nga - Đa phương thức", "badge": "bg-amber-500/20 text-amber-300 border-amber-500/30"},
    "RSCO": {"name": "Ruscon Container Logistics (Delo Group)", "short": "Ruscon", "country": "Russia", "hub": "Novorossiysk (Biển Đen)", "type": "Nga - Biển Đen", "badge": "bg-red-500/20 text-red-300 border-red-500/30"},
    "SASC": {"name": "Sakhalin Shipping Company (SASCO)", "short": "SASCO", "country": "Russia", "hub": "Kholmsk / Vladivostok", "type": "Nga - Viễn Đông", "badge": "bg-cyan-500/20 text-cyan-300 border-cyan-500/30"},
    "XINX": {"name": "New New Shipping Line (Torgmoll)", "short": "New New Shipping", "country": "Russia / China", "hub": "St. Petersburg (Tuyến NSR)", "type": "Nga - Bắc Băng Dương (NSR)", "badge": "bg-indigo-500/20 text-indigo-300 border-indigo-500/30"},
    "NNX":  {"name": "New New Shipping Express", "short": "New New Shipping", "country": "Russia / China", "hub": "Arkhangelsk / St. Petersburg", "type": "Nga - Tuyến Phương Bắc", "badge": "bg-indigo-500/20 text-indigo-300 border-indigo-500/30"},
    "SWFT": {"name": "Swift Transport International", "short": "Swift Line", "country": "Russia / HK", "hub": "St. Petersburg / Vostochny", "type": "Nga - Châu Á Express", "badge": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30"},
    "MODU": {"name": "Modul LLC Terminal & Shipping", "short": "Modul", "country": "Russia", "hub": "St. Petersburg (Baltic)", "type": "Nga - Biển Baltic", "badge": "bg-blue-500/20 text-blue-300 border-blue-500/30"},
    "OVPS": {"name": "OVP Shipping Logistics", "short": "OVP Shipping", "country": "Russia", "hub": "Vladivostok / Novorossiysk", "type": "Nga - Vận tải Biển", "badge": "bg-teal-500/20 text-teal-300 border-teal-500/30"},

    # ========================================================
    # 2. TOP 30 LIÊN MINH HÃNG TÀU CONTAINER VIỄN DƯƠNG TOÀN CẦU
    # ========================================================
    "MAEU": {"name": "A.P. Moller - Maersk Line", "short": "Maersk", "country": "Denmark", "hub": "Copenhagen / Rotterdam", "type": "Top 2 Toàn cầu", "badge": "bg-sky-500/20 text-sky-300 border-sky-500/30"},
    "MSK":  {"name": "Maersk Line Direct", "short": "Maersk", "country": "Denmark", "hub": "Rotterdam / Singapore", "type": "Top 2 Toàn cầu", "badge": "bg-sky-500/20 text-sky-300 border-sky-500/30"},
    "MEDU": {"name": "Mediterranean Shipping Company (MSC)", "short": "MSC", "country": "Switzerland", "hub": "Geneva / Antwerp", "type": "Top 1 Toàn cầu", "badge": "bg-yellow-500/20 text-yellow-300 border-yellow-500/30"},
    "MSCU": {"name": "MSC Mediterranean Shipping", "short": "MSC", "country": "Switzerland", "hub": "Geneva / Bremerhaven", "type": "Top 1 Toàn cầu", "badge": "bg-yellow-500/20 text-yellow-300 border-yellow-500/30"},
    "CMAU": {"name": "CMA CGM Group", "short": "CMA CGM", "country": "France", "hub": "Marseille / Le Havre", "type": "Top 3 Toàn cầu", "badge": "bg-red-500/20 text-red-300 border-red-500/30"},
    "CMA":  {"name": "CMA CGM Shipping", "short": "CMA CGM", "country": "France", "hub": "Marseille / Singapore", "type": "Top 3 Toàn cầu", "badge": "bg-red-500/20 text-red-300 border-red-500/30"},
    "COSU": {"name": "COSCO Shipping Lines", "short": "COSCO", "country": "China", "hub": "Shanghai / Ningbo", "type": "Top 4 Toàn cầu", "badge": "bg-blue-600/20 text-blue-300 border-blue-500/30"},
    "COS":  {"name": "China Ocean Shipping Company", "short": "COSCO", "country": "China", "hub": "Shanghai / Rotterdam", "type": "Top 4 Toàn cầu", "badge": "bg-blue-600/20 text-blue-300 border-blue-500/30"},
    "HLCU": {"name": "Hapag-Lloyd AG", "short": "Hapag-Lloyd", "country": "Germany", "hub": "Hamburg / Bremerhaven", "type": "Top 5 Toàn cầu", "badge": "bg-orange-500/20 text-orange-300 border-orange-500/30"},
    "HLC":  {"name": "Hapag-Lloyd Container Line", "short": "Hapag-Lloyd", "country": "Germany", "hub": "Hamburg / Rotterdam", "type": "Top 5 Toàn cầu", "badge": "bg-orange-500/20 text-orange-300 border-orange-500/30"},
    "ONEY": {"name": "Ocean Network Express (ONE)", "short": "ONE Line", "country": "Japan", "hub": "Tokyo / Singapore", "type": "Top 6 Toàn cầu", "badge": "bg-pink-500/20 text-pink-300 border-pink-500/30"},
    "ONE":  {"name": "Ocean Network Express", "short": "ONE Line", "country": "Japan", "hub": "Kobe / Singapore", "type": "Top 6 Toàn cầu", "badge": "bg-pink-500/20 text-pink-300 border-pink-500/30"},
    "EGLV": {"name": "Evergreen Marine Corp", "short": "Evergreen", "country": "Taiwan", "hub": "Kaohsiung / Taipei", "type": "Top 7 Toàn cầu", "badge": "bg-emerald-600/20 text-emerald-300 border-emerald-500/30"},
    "EGL":  {"name": "Evergreen Line Global", "short": "Evergreen", "country": "Taiwan", "hub": "Kaohsiung / Rotterdam", "type": "Top 7 Toàn cầu", "badge": "bg-emerald-600/20 text-emerald-300 border-emerald-500/30"},
    "HDMU": {"name": "HMM Company Limited (Hyundai Merchant)", "short": "HMM", "country": "South Korea", "hub": "Busan / Gwangyang", "type": "Top 8 Toàn cầu", "badge": "bg-red-600/20 text-red-300 border-red-500/30"},
    "HMM":  {"name": "HMM Container Service", "short": "HMM", "country": "South Korea", "hub": "Busan / Singapore", "type": "Top 8 Toàn cầu", "badge": "bg-red-600/20 text-red-300 border-red-500/30"},
    "YMLU": {"name": "Yang Ming Marine Transport", "short": "Yang Ming", "country": "Taiwan", "hub": "Keelung / Kaohsiung", "type": "Top 9 Toàn cầu", "badge": "bg-blue-500/20 text-blue-300 border-blue-500/30"},
    "YML":  {"name": "Yang Ming Line", "short": "Yang Ming", "country": "Taiwan", "hub": "Kaohsiung / Rotterdam", "type": "Top 9 Toàn cầu", "badge": "bg-blue-500/20 text-blue-300 border-blue-500/30"},
    "ZIMU": {"name": "ZIM Integrated Shipping Services", "short": "ZIM", "country": "Israel", "hub": "Haifa / New York", "type": "Top 10 Toàn cầu", "badge": "bg-indigo-500/20 text-indigo-300 border-indigo-500/30"},
    "ZIM":  {"name": "ZIM Line Express", "short": "ZIM", "country": "Israel", "hub": "Haifa / Shanghai", "type": "Top 10 Toàn cầu", "badge": "bg-indigo-500/20 text-indigo-300 border-indigo-500/30"},
    "WHLC": {"name": "Wan Hai Lines", "short": "Wan Hai", "country": "Taiwan", "hub": "Taipei / Singapore", "type": "Top 11 Toàn cầu", "badge": "bg-cyan-600/20 text-cyan-300 border-cyan-500/30"},
    "WHL":  {"name": "Wan Hai Shipping", "short": "Wan Hai", "country": "Taiwan", "hub": "Kaohsiung / Cát Lái", "type": "Top 11 Toàn cầu", "badge": "bg-cyan-600/20 text-cyan-300 border-cyan-500/30"},
    "PILU": {"name": "Pacific International Lines (PIL)", "short": "PIL", "country": "Singapore", "hub": "Singapore / Jurong", "type": "Top 12 Toàn cầu", "badge": "bg-amber-600/20 text-amber-300 border-amber-500/30"},
    "PCLL": {"name": "Pacific Carrier Line", "short": "PIL Lines", "country": "Singapore", "hub": "Singapore", "type": "Top 12 Toàn cầu", "badge": "bg-amber-600/20 text-amber-300 border-amber-500/30"},
    "MATS": {"name": "Matson Navigation Company", "short": "Matson", "country": "USA", "hub": "Honolulu / Long Beach", "type": "Mỹ - Xuyên Thái Bình Dương", "badge": "bg-blue-400/20 text-blue-300 border-blue-400/30"},
    "SMLU": {"name": "SM Line Corporation", "short": "SM Line", "country": "South Korea", "hub": "Busan / Los Angeles", "type": "Hàn Quốc - Transpacific", "badge": "bg-rose-600/20 text-rose-300 border-rose-500/30"},
    "ARKU": {"name": "Arkas Line", "short": "Arkas", "country": "Turkey", "hub": "Istanbul / Izmir", "type": "Địa Trung Hải & Biển Đen", "badge": "bg-teal-500/20 text-teal-300 border-teal-500/30"},
    "GRIU": {"name": "Grimaldi Group", "short": "Grimaldi", "country": "Italy", "hub": "Naples / Antwerp", "type": "Ro-Ro & Container", "badge": "bg-yellow-600/20 text-yellow-300 border-yellow-500/30"},
    "UNIF": {"name": "Unifeeder Group (DP World)", "short": "Unifeeder", "country": "Denmark", "hub": "Aarhus / Rotterdam", "type": "Feeder Bắc Âu & Baltic", "badge": "bg-sky-600/20 text-sky-300 border-sky-500/30"},
    "CNCO": {"name": "Swire Shipping (China Navigation)", "short": "Swire Shipping", "country": "Singapore / UK", "hub": "Singapore / Sydney", "type": "Châu Đại Dương & APAC", "badge": "bg-purple-500/20 text-purple-300 border-purple-500/30"},
    "SAMU": {"name": "Samudera Shipping Line", "short": "Samudera", "country": "Indonesia / Singapore", "hub": "Jakarta / Singapore", "type": "Đông Nam Á", "badge": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30"},
    "ESLU": {"name": "Emirates Shipping Line", "short": "Emirates Line", "country": "UAE", "hub": "Dubai / Jebel Ali", "type": "Trung Đông & Ấn Độ", "badge": "bg-amber-500/20 text-amber-300 border-amber-500/30"},
    "SEAU": {"name": "Seaboard Marine", "short": "Seaboard", "country": "USA", "hub": "Miami / Caribbean", "type": "Châu Mỹ & Caribbean", "badge": "bg-blue-500/20 text-blue-300 border-blue-500/30"},
    "LMCU": {"name": "Ignazio Messina & C.", "short": "Messina Line", "country": "Italy", "hub": "Genoa / Middle East", "type": "Địa Trung Hải & Châu Phi", "badge": "bg-red-400/20 text-red-300 border-red-400/30"},
    "NSCS": {"name": "Bahri (National Shipping Co. of Saudi Arabia)", "short": "Bahri", "country": "Saudi Arabia", "hub": "Riyadh / Jeddah", "type": "Trung Đông & Vùng Vịnh", "badge": "bg-emerald-600/20 text-emerald-300 border-emerald-500/30"},

    # ========================================================
    # 3. KHỐI HÃNG TÀU NỘI Á & TRUNG CHUYỂN (INTRA-ASIA & REGIONAL FEEDERS)
    # ========================================================
    "SITC": {"name": "SITC International Holdings", "short": "SITC", "country": "China", "hub": "Qingdao / Shanghai", "type": "Nội Á Cao Tốc", "badge": "bg-cyan-500/20 text-cyan-300 border-cyan-500/30"},
    "KMTC": {"name": "Korea Marine Transport Co (KMTC)", "short": "KMTC", "country": "South Korea", "hub": "Seoul / Busan", "type": "Nội Á Hàng Đầu", "badge": "bg-blue-500/20 text-blue-300 border-blue-500/30"},
    "TSLU": {"name": "TS Lines Ltd", "short": "TS Lines", "country": "Hong Kong / Taiwan", "hub": "Taipei / Hong Kong", "type": "Nội Á & Viễn Đông", "badge": "bg-purple-500/20 text-purple-300 border-purple-500/30"},
    "ATNT": {"name": "Antong Holdings (QASC)", "short": "Antong Line", "country": "China", "hub": "Quanzhou / Shanghai", "type": "Nội Địa Trung Quốc", "badge": "bg-amber-500/20 text-amber-300 border-amber-500/30"},
    "ZGCU": {"name": "Zhonggu Logistics Corp", "short": "Zhonggu", "country": "China", "hub": "Shanghai / Tianjin", "type": "Nội Á & Trung Quốc", "badge": "bg-red-500/20 text-red-300 border-red-500/30"},
    "SNKO": {"name": "Sinokor Merchant Marine", "short": "Sinokor", "country": "South Korea", "hub": "Seoul / Vladivostok", "type": "Hàn - Trung - Nga", "badge": "bg-indigo-500/20 text-indigo-300 border-indigo-500/30"},
    "REGU": {"name": "Regional Container Lines (RCL)", "short": "RCL", "country": "Thailand", "hub": "Bangkok / Singapore", "type": "Đông Nam Á Feeder", "badge": "bg-teal-500/20 text-teal-300 border-teal-500/30"},
    "OOLU": {"name": "Orient Overseas Container Line (OOCL)", "short": "OOCL", "country": "Hong Kong", "hub": "Hong Kong / Shanghai", "type": "Hồng Kông Viễn Dương", "badge": "bg-rose-500/20 text-rose-300 border-rose-500/30"},
    "HASU": {"name": "Heung-A Line", "short": "Heung-A", "country": "South Korea", "hub": "Busan / Incheon", "type": "Nội Á & Hóa Chất", "badge": "bg-blue-400/20 text-blue-300 border-blue-400/30"},
    "DSTA": {"name": "Dong Young Shipping", "short": "Dong Young", "country": "South Korea", "hub": "Busan", "type": "Hàn - Nhật - Việt Nam", "badge": "bg-sky-500/20 text-sky-300 border-sky-500/30"},
    "CKLU": {"name": "CK Line Co Ltd", "short": "CK Line", "country": "South Korea", "hub": "Seoul / Shanghai", "type": "Đông Á Tuyến Ngắn", "badge": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30"},

    # ========================================================
    # 4. TOP 15 TẬP ĐOÀN LOGISTICS & VẬN ĐƠN THỨ CẤP QUỐC TẾ (GLOBAL NVOCCs / FORWARDERS)
    # ========================================================
    "KHNN": {"name": "Kuehne + Nagel International AG", "short": "Kuehne+Nagel", "country": "Switzerland", "hub": "Schindellegi / Bremen", "type": "Top 1 NVOCC Toàn cầu", "badge": "bg-blue-600/20 text-blue-300 border-blue-500/30"},
    "NAKU": {"name": "Kuehne + Nagel Logistics", "short": "Kuehne+Nagel", "country": "Switzerland", "hub": "Rotterdam / Singapore", "type": "Top 1 NVOCC Toàn cầu", "badge": "bg-blue-600/20 text-blue-300 border-blue-500/30"},
    "DHLU": {"name": "DHL Global Forwarding (Danmar Lines)", "short": "DHL Global", "country": "Germany", "hub": "Bonn / Frankfurt", "type": "Top 2 NVOCC Toàn cầu", "badge": "bg-yellow-500/20 text-yellow-300 border-yellow-500/30"},
    "DGF":  {"name": "DHL Global Forwarding Freight", "short": "DHL Logistics", "country": "Germany", "hub": "Singapore / Hamburg", "type": "Top 2 NVOCC Toàn cầu", "badge": "bg-yellow-500/20 text-yellow-300 border-yellow-500/30"},
    "DSVU": {"name": "DSV Panalpina A/S", "short": "DSV Logistics", "country": "Denmark", "hub": "Hedehusene / Antwerp", "type": "Top 3 NVOCC Toàn cầu", "badge": "bg-sky-500/20 text-sky-300 border-sky-500/30"},
    "SCHU": {"name": "DB Schenker Logistics", "short": "DB Schenker", "country": "Germany", "hub": "Essen / Frankfurt", "type": "Top 4 NVOCC Toàn cầu", "badge": "bg-teal-500/20 text-teal-300 border-teal-500/30"},
    "EXPD": {"name": "Expeditors International of Washington", "short": "Expeditors", "country": "USA", "hub": "Seattle / Hong Kong", "type": "Top NVOCC Hoa Kỳ", "badge": "bg-red-500/20 text-red-300 border-red-500/30"},
    "SNTO": {"name": "Sinotrans Limited", "short": "Sinotrans", "country": "China", "hub": "Beijing / Shanghai", "type": "Đại Tập Đoàn TQ", "badge": "bg-amber-600/20 text-amber-300 border-amber-500/30"},
    "CHRB": {"name": "C.H. Robinson Worldwide", "short": "C.H. Robinson", "country": "USA", "hub": "Eden Prairie / Chicago", "type": "Vận tải Đa phương thức", "badge": "bg-indigo-500/20 text-indigo-300 border-indigo-500/30"},
    "CEVA": {"name": "CEVA Logistics (CMA CGM Subsidiary)", "short": "CEVA", "country": "France / Switzerland", "hub": "Marseille / Baar", "type": "Supply Chain Quốc tế", "badge": "bg-rose-500/20 text-rose-300 border-rose-500/30"},
    "NIPX": {"name": "Nippon Express Holdings", "short": "Nippon Express", "country": "Japan", "hub": "Tokyo / Osaka", "type": "Tập đoàn Nhật Bản", "badge": "bg-purple-500/20 text-purple-300 border-purple-500/30"},
    "KLGI": {"name": "Kerry Logistics Network", "short": "Kerry Logistics", "country": "Hong Kong", "hub": "Hong Kong / Bangkok", "type": "Châu Á & Toàn cầu", "badge": "bg-orange-500/20 text-orange-300 border-orange-500/30"},
    "GEOD": {"name": "Geodis Logistics (SNCF)", "short": "Geodis", "country": "France", "hub": "Levallois-Perret", "type": "Hàng hải Châu Âu", "badge": "bg-blue-400/20 text-blue-300 border-blue-400/30"},
    "HELL": {"name": "Hellmann Worldwide Logistics", "short": "Hellmann", "country": "Germany", "hub": "Osnabruck / Hamburg", "type": "Đức Toàn cầu", "badge": "bg-teal-600/20 text-teal-300 border-teal-500/30"},
    "KWEC": {"name": "Kintetsu World Express (KWE)", "short": "KWE", "country": "Japan", "hub": "Tokyo", "type": "Nhật Bản Giao nhận", "badge": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30"},
    "YUSN": {"name": "Yusen Logistics (NYK Group)", "short": "Yusen", "country": "Japan", "hub": "Tokyo / London", "type": "Chuỗi Cung ứng Toàn cầu", "badge": "bg-cyan-500/20 text-cyan-300 border-cyan-500/30"},
    "BLLR": {"name": "Bollore Transport & Logistics", "short": "Bollore", "country": "France", "hub": "Puteaux / Le Havre", "type": "Châu Phi & Pháp", "badge": "bg-amber-500/20 text-amber-300 border-amber-500/30"},

    # ========================================================
    # 5. KHỐI ĐỘI TÀU CONTAINER & FEEDER VIỆT NAM (VIETNAMESE CARRIERS)
    # ========================================================
    "VIMU": {"name": "Vietnam Maritime Corporation (VIMC / Vinalines)", "short": "VIMC Lines", "country": "Vietnam", "hub": "Hải Phòng / Cát Lái", "type": "Quốc gia Việt Nam", "badge": "bg-emerald-500/25 text-emerald-300 border-emerald-500/40"},
    "VML":  {"name": "Vinalines Container Lines", "short": "Vinalines", "country": "Vietnam", "hub": "Hải Phòng / TP.HCM", "type": "Quốc gia Việt Nam", "badge": "bg-emerald-500/25 text-emerald-300 border-emerald-500/40"},
    "HACU": {"name": "Hai An Transport & Stevedoring (HATS)", "short": "Hải An Lines", "country": "Vietnam", "hub": "Hải Phòng / Cái Mép", "type": "Hàng hải Hải An", "badge": "bg-cyan-500/25 text-cyan-300 border-cyan-500/40"},
    "HATS": {"name": "Hai An Lines Express", "short": "Hải An", "country": "Vietnam", "hub": "Hải Phòng / Cát Lái", "type": "Đội tàu Hải An", "badge": "bg-cyan-500/25 text-cyan-300 border-cyan-500/40"},
    "VOSC": {"name": "Vietnam Ocean Shipping JSC (VOSCO)", "short": "VOSCO", "country": "Vietnam", "hub": "Hải Phòng", "type": "Vận tải Biển Bắc", "badge": "bg-blue-500/25 text-blue-300 border-blue-500/40"},
    "BDSU": {"name": "Bien Dong Shipping Company", "short": "Biển Đông", "country": "Vietnam", "hub": "Hải Phòng / TP.HCM", "type": "Biển Đông Container", "badge": "bg-sky-500/25 text-sky-300 border-sky-500/40"},
    "TCSP": {"name": "Tan Cang Shipping JSC (Saigon Newport)", "short": "Tân Cảng Shipping", "country": "Vietnam", "hub": "Cát Lái / Cái Mép / Hải Phòng", "type": "Tân Cảng Sài Gòn", "badge": "bg-emerald-600/25 text-emerald-300 border-emerald-500/40"},
    "GMD":  {"name": "Gemadept Shipping Lines", "short": "Gemadept", "country": "Vietnam", "hub": "Gemalink Cái Mép / Đình Vũ", "type": "Tập đoàn Gemadept", "badge": "bg-amber-500/25 text-amber-300 border-amber-500/40"},
    "VNF":  {"name": "Vinafco Joint Stock Company", "short": "Vinafco", "country": "Vietnam", "hub": "Hải Phòng / Đà Nẵng / Cát Lái", "type": "Vận tải Vinafco", "badge": "bg-purple-500/25 text-purple-300 border-purple-500/40"},
}

# DANH MỤC CẢNG BIỂN CHIẾN LƯỢC LIÊN BANG NGA (RUSSIAN STRATEGIC SEA PORTS)
RUSSIAN_STRATEGIC_PORTS = {
    "RUSPB": {"code": "RUSPB", "name": "Cảng Lớn St. Petersburg (Bolshoy Port)", "basin": "Biển Baltic (Tây Bắc Nga)", "type": "Cửa ngõ cà phê, chè, gạo & tiêu VN sang Moscow/Tây Bắc", "flag": "🇷🇺"},
    "RUBRO": {"code": "RUBRO", "name": "Cảng Container Đa năng Bronka", "basin": "Biển Baltic (Vịnh Phần Lan)", "type": "Cảng nước sâu hiện đại, thông quan container cao tốc", "flag": "🇷🇺"},
    "RUULU": {"code": "RUULU", "name": "Cảng Biển Sâu Ust-Luga", "basin": "Biển Baltic", "type": "Đầu mối phân bón Kali, Urê & hóa chất xuất khẩu", "flag": "🇷🇺"},
    "RUNVS": {"code": "RUNVS", "name": "Cảng Novorossiysk", "basin": "Biển Đen (Miền Nam Nga)", "type": "Cảng xuất khẩu lúa mì, phân bón & ngũ cốc lớn nhất Nga", "flag": "🇷🇺"},
    "RUVVO": {"code": "RUVVO", "name": "Cảng Thương Mại Quốc Tế Vladivostok (VMTP)", "basin": "Viễn Đông Nga (Biển Nhật Bản)", "type": "Tuyến biển kết nối Việt Nam trực tiếp nhanh nhất (9-12 ngày)", "flag": "🇷🇺"},
    "RUVYP": {"code": "RUVYP", "name": "Cảng Container Vostochny", "basin": "Viễn Đông Nga (Vịnh Wrangel)", "type": "Trạm trung chuyển container lớn nhất tuyến Á - Âu", "flag": "🇷🇺"},
    "RUNHK": {"code": "RUNHK", "name": "Cảng Nakhodka", "basin": "Viễn Đông Nga", "type": "Cảng tổng hợp và tiếp nhận tàu container Châu Á", "flag": "🇷🇺"},
    "RUMMK": {"code": "RUMMK", "name": "Cảng Biển Không Đóng Băng Murmansk", "basin": "Bắc Băng Dương / Biển Barents", "type": "Cửa ngõ Tuyến hàng hải phương Bắc (NSR)", "flag": "🇷🇺"},
    "RUARH": {"code": "RUARH", "name": "Cảng Arkhangelsk", "basin": "Bạch Hải / Bắc Băng Dương", "type": "Trạm tiếp nhận tàu hàng New New Shipping từ Trung Quốc/Việt Nam", "flag": "🇷🇺"},
    "RUKGD": {"code": "RUKGD", "name": "Cảng Kaliningrad", "basin": "Biển Baltic (Vùng ngoại lãnh thổ)", "type": "Cảng thương mại trung chuyển Châu Âu", "flag": "🇷🇺"},
}

# CỔNG TRA CỨU HÃNG TÀU TRỰC TIẾP (OFFICIAL CARRIER DIRECT TRACKING PORTALS)
OFFICIAL_TRACKING_PORTALS = {
    # Khối Viễn Dương Toàn Cầu
    "MAEU": "https://www.maersk.com/tracking/{bl}",
    "MSK":  "https://www.maersk.com/tracking/{bl}",
    "MEDU": "https://www.msc.com/en/track-a-shipment?reference={bl}",
    "MSCU": "https://www.msc.com/en/track-a-shipment?reference={bl}",
    "CMAU": "https://www.cma-cgm.com/ebusiness/tracking/search?SearchBy=BL&SearchValue={bl}",
    "CMA":  "https://www.cma-cgm.com/ebusiness/tracking/search?SearchBy=BL&SearchValue={bl}",
    "COSU": "https://lines.coscoshipping.com/ebusiness/cargoTracking?trackingType=BILLOFLADING&number={bl}",
    "COS":  "https://lines.coscoshipping.com/ebusiness/cargoTracking?trackingType=BILLOFLADING&number={bl}",
    "HLCU": "https://www.hapag-lloyd.com/en/online-business/track/track-by-booking-solution.html?blno={bl}",
    "HLC":  "https://www.hapag-lloyd.com/en/online-business/track/track-by-booking-solution.html?blno={bl}",
    "ONEY": "https://ecomm.one-line.com/one-ecom/manage-shipment/cargo-tracking?trackingNumber={bl}",
    "ONE":  "https://ecomm.one-line.com/one-ecom/manage-shipment/cargo-tracking?trackingNumber={bl}",
    "EGLV": "https://www.shipmentlink.com/servlet/TTrk_Tracking?quick_type=BL&quick_no={bl}",
    "EGL":  "https://www.shipmentlink.com/servlet/TTrk_Tracking?quick_type=BL&quick_no={bl}",
    "HDMU": "https://www.hmm21.com/cms/business/ebusiness/trackTrace/trackTrace/index.jsp?type=1&number={bl}",
    "HMM":  "https://www.hmm21.com/cms/business/ebusiness/trackTrace/trackTrace/index.jsp?type=1&number={bl}",
    "YMLU": "https://www.yangming.com/e-service/track_trace/track_trace_cargo_tracking.aspx?type=BL&num={bl}",
    "YML":  "https://www.yangming.com/e-service/track_trace/track_trace_cargo_tracking.aspx?type=BL&num={bl}",
    "ZIMU": "https://www.zim.com/tools/track-a-shipment?consignment={bl}",
    "ZIM":  "https://www.zim.com/tools/track-a-shipment?consignment={bl}",
    "WHLC": "https://www.wanhai.com/views/cargoTracking/cargoTracking.xhtml?q_type=BL&q_num={bl}",
    "WHL":  "https://www.wanhai.com/views/cargoTracking/cargoTracking.xhtml?q_type=BL&q_num={bl}",
    "PILU": "https://www.pilship.com/en-our-track-and-trace-cargo-tracking/120.html?ref={bl}",
    "PCLL": "https://www.pilship.com/en-our-track-and-trace-cargo-tracking/120.html?ref={bl}",
    "SITC": "https://www.sitc.com/en/tracking.html?bl={bl}",
    "KMTC": "https://www.ekmtc.com/cargoTracking?blNo={bl}",
    "OOLU": "https://www.oocl.com/eng/ourservices/eservices/cargotracking/Pages/cargotracking.aspx?cargo_tracking_number={bl}",
    
    # Khối Chuyên Tuyến Nga & Á - Âu
    "FESU": "https://www.fesco.ru/en/clients/tracking/?number={bl}",
    "FESC": "https://www.fesco.ru/en/clients/tracking/?number={bl}",
    "TRCU": "https://trcont.com/en/tracking?number={bl}",
    "TRCO": "https://trcont.com/en/tracking?number={bl}",
    "RSCO": "https://ruscon.delo-group.com/en/services/tracking/?number={bl}",
    "SASC": "https://sasco.ru/en/tracking?bl={bl}",
    "SWFT": "https://swifttransport.ru/en/tracking?bl={bl}",
    "XINX": "https://newnewshipping.com/en/tracking?bl={bl}",

    # Khối Việt Nam & NVOCCs
    "TCSP": "https://saigonnewport.com.vn/e-port?bl={bl}",
    "HACU": "https://haian.vn/tra-cuu-van-don?bl={bl}",
    "HATS": "https://haian.vn/tra-cuu-van-don?bl={bl}",
    "VIMU": "https://vimc.co/dich-vu-hang-hai/tra-cuu-tau-hang/?bl={bl}",
    "VML":  "https://vimc.co/dich-vu-hang-hai/tra-cuu-tau-hang/?bl={bl}",
    "GMD":  "https://www.gemadept.com.vn/e-port/?bl={bl}",
    "KHNN": "https://mykn.kuehne-nagel.com/public-tracking?query={bl}",
    "NAKU": "https://mykn.kuehne-nagel.com/public-tracking?query={bl}",
    "DHLU": "https://www.dhl.com/global-en/home/tracking.html?tracking-id={bl}",
    "DGF":  "https://www.dhl.com/global-en/home/tracking.html?tracking-id={bl}",
    "DSVU": "https://www.dsv.com/en/our-solutions/modes-of-transport/sea-freight/track-and-trace-sea?trackId={bl}",
    "SCHU": "https://www.dbschenker.com/global/eservices/tracking?trackingNumber={bl}",
    "EXPD": "https://www.expeditors.com/tracking?reference={bl}",
}

def get_carrier_tracking_url(bl_number, carrier_key=None):
    """
    Tạo link tra cứu vận đơn trực tiếp trên Cổng hãng tàu chính thống.
    Tuyệt đối không chuyển hướng sang Google Search.
    """
    clean_bl = str(bl_number or "").strip()
    key = str(carrier_key or "").strip().upper()
    
    if key and key in OFFICIAL_TRACKING_PORTALS:
        return OFFICIAL_TRACKING_PORTALS[key].replace("{bl}", clean_bl)
    
    # Thử bóc tách prefix từ chính mã vận đơn
    compact_bl = re.sub(r'[^A-Za-z0-9]', '', clean_bl).upper()
    for prefix_len in (4, 3, 2):
        if len(compact_bl) >= prefix_len:
            p = compact_bl[:prefix_len]
            if p in OFFICIAL_TRACKING_PORTALS:
                return OFFICIAL_TRACKING_PORTALS[p].replace("{bl}", clean_bl)
                
    # Fallback tiêu chuẩn sang Cổng tra cứu container hàng hải quốc tế Đa hãng tàu (SeaRates by DP World)
    return f"https://www.searates.com/container/tracking/?number={clean_bl}"

def detect_carrier_info(bl_number):
    """
    Tự động phân tích mã B/L để bóc tách Tiền tố và nhận diện Hãng tàu quốc tế.
    Hỗ trợ cả chuẩn SCAC 4 ký tự, mã 3 ký tự và các tiền tố hãng tàu Nga / VN.
    """
    if not bl_number:
        return None
    
    clean_bl = re.sub(r'[^A-Za-z0-9]', '', str(bl_number)).upper()
    if len(clean_bl) < 3:
        return None

    def _pack_res(entry, code_key):
        res = dict(entry)
        res["code"] = code_key
        res["scac"] = code_key
        res["tracking_url"] = get_carrier_tracking_url(bl_number, code_key)
        return res

    # 1. Thử khớp 4 ký tự đầu (Chuẩn SCAC quốc tế)
    prefix_4 = clean_bl[:4]
    if prefix_4 in CARRIER_REGISTRY:
        return _pack_res(CARRIER_REGISTRY[prefix_4], prefix_4)

    # 2. Thử khớp 3 ký tự đầu
    prefix_3 = clean_bl[:3]
    if prefix_3 in CARRIER_REGISTRY:
        return _pack_res(CARRIER_REGISTRY[prefix_3], prefix_3)

    # 3. Thử tìm kiếm theo tiền tố trước dấu gạch ngang (nếu chuỗi gốc có dạng ONE-SGN..., FES-2026...)
    parts = re.split(r'[-_/]', str(bl_number))
    if len(parts) > 1:
        first_part = parts[0].strip().upper()
        if first_part in CARRIER_REGISTRY:
            return _pack_res(CARRIER_REGISTRY[first_part], first_part)
        if first_part[:4] in CARRIER_REGISTRY:
            return _pack_res(CARRIER_REGISTRY[first_part[:4]], first_part[:4])
        if first_part[:3] in CARRIER_REGISTRY:
            return _pack_res(CARRIER_REGISTRY[first_part[:3]], first_part[:3])

    # 4. Nhận diện các mã quốc gia đặt làm tiền tố (ví dụ DE-..., RU-..., CH-..., US-..., SG-...)
    country_prefix_map = {
        "RU": {"name": "Hải Quan & Hãng Tàu Liên Bang Nga", "short": "Tuyến Nga 🇷🇺", "country": "Russia", "hub": "Vladivostok / St. Petersburg", "type": "Chuyên Tuyến Nga", "badge": "bg-rose-500/25 text-rose-300 border-rose-500/40"},
        "DE": {"name": "Hải Quan CHLB Đức & Hapag/Maersk", "short": "Đức / EU 🇩🇪", "country": "Germany", "hub": "Hamburg / Bremerhaven", "type": "Châu Âu Cấp 1", "badge": "bg-amber-500/20 text-amber-300 border-amber-500/30"},
        "CH": {"name": "Thụy Sĩ / Địa Trung Hải (MSC)", "short": "Thụy Sĩ 🇨🇭", "country": "Switzerland", "hub": "Geneva / Basel", "type": "Châu Âu", "badge": "bg-red-500/20 text-red-300 border-red-500/30"},
        "US": {"name": "CBP Hải Quan Hoa Kỳ", "short": "Hoa Kỳ 🇺🇸", "country": "USA", "hub": "Long Beach / New York", "type": "Bắc Mỹ", "badge": "bg-blue-500/20 text-blue-300 border-blue-500/30"},
        "SG": {"name": "Cảng Trung Chuyển Quốc Tế Singapore", "short": "Singapore 🇸🇬", "country": "Singapore", "hub": "Cảng PSA Singapore", "type": "Trung Chuyển Quốc Tế", "badge": "bg-cyan-500/20 text-cyan-300 border-cyan-500/30"},
        "VN": {"name": "Hải Quan & Cảng Biển Việt Nam", "short": "Việt Nam 🇻🇳", "country": "Vietnam", "hub": "Cát Lái / Hải Phòng", "type": "Cảng Xuất Nội Địa", "badge": "bg-emerald-500/25 text-emerald-300 border-emerald-500/40"},
    }

    if len(clean_bl) >= 2:
        cc2 = clean_bl[:2]
        if cc2 in country_prefix_map:
            res = dict(country_prefix_map[cc2])
            res["code"] = cc2
            res["scac"] = cc2
            res["tracking_url"] = get_carrier_tracking_url(bl_number, cc2)
            return res

    # Mặc định: Vận đơn quốc tế độc lập
    res = {
        "name": "Vận Tải Biển Quốc Tế (Carrier Manifest)",
        "short": "Hàng Hải QT",
        "country": "Global",
        "hub": "Global Trade Line",
        "type": "Vận Đơn Tiêu Chuẩn",
        "badge": "bg-slate-700/40 text-slate-300 border-slate-600/40",
        "code": "INTL",
        "scac": "INTL",
        "tracking_url": get_carrier_tracking_url(bl_number)
    }
    return res

def clean_key_for_search(text):
    """Chuẩn hóa ký tự mềm: loại bỏ ký tự đặc biệt, gạch ngang, khoảng trắng, viết thường."""
    if not text:
        return ""
    return re.sub(r'[^a-zA-Z0-9\u00C0-\u1EF9]', '', str(text)).lower()
