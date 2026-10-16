# -*- coding: utf-8 -*-
"""
Hệ Thống Phân Loại & Danh Mục Mã Ngành Toàn Biểu HS (Universal WCO HS & Industry Catalog)
Khối Xuất Nhập Khẩu & Thương Mại Quốc Tế Tập Đoàn

Bao gồm:
- 21 Phần (Sections) theo chuẩn WCO
- 97 Chương (Chapters 01 - 97) bao phủ 100% hàng hóa toàn cầu
- 4 Chế độ sắp xếp trải nghiệm tìm kiếm:
  1. 'volume': Top Kim Ngạch Xuất Nhập Khẩu & Tần Suất Giao Dịch
  2. 'clusters': 6 Cụm Chuỗi Giá Trị & Mục Đích Sử Dụng
  3. 'alphabet': Bảng Chữ Cái (A -> Z)
  4. 'wco': Thứ Tự Số Học Chuẩn Hải Quan (Chương 01 -> 97 theo 21 Phần)
- Công cụ tìm kiếm tức thì (Omni-Search Autocomplete) theo từ khóa và mã HS
"""

WCO_SECTIONS = [
    {"section": 1, "roman": "I", "name_vi": "Động vật sống và các sản phẩm từ động vật", "chapters": "01-05"},
    {"section": 2, "roman": "II", "name_vi": "Các sản phẩm thực vật (Nông sản & Lương thực)", "chapters": "06-14"},
    {"section": 3, "roman": "III", "name_vi": "Mỡ và dầu động vật hoặc thực vật", "chapters": "15"},
    {"section": 4, "roman": "IV", "name_vi": "Thực phẩm chế biến; đồ uống, rượu và giấm; thuốc lá", "chapters": "16-24"},
    {"section": 5, "roman": "V", "name_vi": "Khoáng sản & Nhiên liệu khoáng", "chapters": "25-27"},
    {"section": 6, "roman": "VI", "name_vi": "Sản phẩm của ngành công nghiệp hóa chất hoặc liên quan", "chapters": "28-38"},
    {"section": 7, "roman": "VII", "name_vi": "Plastic (Nhựa) và cao su và các sản phẩm từ chúng", "chapters": "39-40"},
    {"section": 8, "roman": "VIII", "name_vi": "Da sống, da thuộc, lông thú, túi xách, va li", "chapters": "41-43"},
    {"section": 9, "roman": "IX", "name_vi": "Gỗ và các mặt hàng bằng gỗ; than củi; mây tre đan", "chapters": "44-46"},
    {"section": 10, "roman": "X", "name_vi": "Bột giấy từ gỗ, giấy, bìa và các sản phẩm in ấn", "chapters": "47-49"},
    {"section": 11, "roman": "XI", "name_vi": "Nguyên liệu dệt và các sản phẩm dệt may", "chapters": "50-63"},
    {"section": 12, "roman": "XII", "name_vi": "Giày, dép, mũ, nón, ô dù, hoa giả", "chapters": "64-67"},
    {"section": 13, "roman": "XIII", "name_vi": "Sản phẩm bằng đá, thạch cao, xi măng, gốm sứ, thủy tinh", "chapters": "68-70"},
    {"section": 14, "roman": "XIV", "name_vi": "Ngọc trai, đá quý, kim loại quý và đồ trang sức", "chapters": "71"},
    {"section": 15, "roman": "XV", "name_vi": "Kim loại cơ bản và các sản phẩm bằng kim loại cơ bản (Sắt, thép, nhôm)", "chapters": "72-83"},
    {"section": 16, "roman": "XVI", "name_vi": "Máy vi tính, máy móc thiết bị điện, điện tử và cơ khí", "chapters": "84-85"},
    {"section": 17, "roman": "XVII", "name_vi": "Phương tiện vận tải (Ô tô, xe máy, tàu thuyền, máy bay)", "chapters": "86-89"},
    {"section": 18, "roman": "XVIII", "name_vi": "Dụng cụ quang học, y tế, đồng hồ, nhạc cụ", "chapters": "90-92"},
    {"section": 19, "roman": "XIX", "name_vi": "Vũ khí và đạn dược; các bộ phận và phụ kiện", "chapters": "93"},
    {"section": 20, "roman": "XX", "name_vi": "Hàng tạp trị khác (Đồ nội thất, giường nệm, đồ chơi)", "chapters": "94-96"},
    {"section": 21, "roman": "XXI", "name_vi": "Tác phẩm nghệ thuật, đồ sưu tầm và đồ cổ", "chapters": "97"}
]

END_USE_CLUSTERS = {
    "agri_food": {
        "id": "agri_food",
        "name_vi": "Nông - Lâm - Thủy Sản & Thực Phẩm Chế Biến",
        "icon": "wheat",
        "badge_color": "emerald",
        "description": "Các sản phẩm nông nghiệp, thủy sản, đồ uống, dầu thực vật và thực phẩm chế biến xuất khẩu",
        "chapters": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "44"]
    },
    "fashion_footwear": {
        "id": "fashion_footwear",
        "name_vi": "Thời Trang, Dệt May, Da Giày & Phụ Liệu",
        "icon": "shirt",
        "badge_color": "pink",
        "description": "Quần áo may mặc dệt kim, dệt thoi, xơ sợi dệt, da thuộc, túi xách, giày dép xuất khẩu",
        "chapters": ["50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "41", "42", "43"]
    },
    "tech_machinery": {
        "id": "tech_machinery",
        "name_vi": "Công Nghệ, Điện Tử & Cơ Khí Chế Tạo",
        "icon": "cpu",
        "badge_color": "cyan",
        "description": "Máy tính, điện thoại, vi mạch điện tử, máy móc công nghiệp, động cơ và thiết bị quang học",
        "chapters": ["84", "85", "90", "91"]
    },
    "materials_chemicals": {
        "id": "materials_chemicals",
        "name_vi": "Nguyên Liệu Công Nghiệp, Hóa Chất, Nhựa & Thép",
        "icon": "flask-conical",
        "badge_color": "blue",
        "description": "Hóa chất cơ bản, phân bón, hạt nhựa, cao su, sắt thép, kim loại màu và khoáng sản",
        "chapters": ["25", "26", "27", "28", "29", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "72", "73", "74", "75", "76", "78", "79", "80", "81", "82", "83"]
    },
    "construction_furniture": {
        "id": "construction_furniture",
        "name_vi": "Xây Dựng, Vật Liệu & Đồ Gỗ Nội Thất",
        "icon": "home",
        "badge_color": "amber",
        "description": "Đồ gỗ nội ngoại thất, ván ép, xi măng, gạch ốp lát, gốm sứ mỹ nghệ, kính xây dựng",
        "chapters": ["44", "45", "46", "68", "69", "70", "94"]
    },
    "transport_logistics": {
        "id": "transport_logistics",
        "name_vi": "Vận Tải, Xe Cộ, Tàu Thuyền & Thiết Bị Chuyên Dụng",
        "icon": "truck",
        "badge_color": "purple",
        "description": "Ô tô, xe máy, phụ tùng linh kiện xe hơi, tàu biển, xà lan, toa xe lửa và thiết bị bay",
        "chapters": ["86", "87", "88", "89"]
    },
    "special_consumer": {
        "id": "special_consumer",
        "name_vi": "Dược Phẩm, Hàng Tiêu Dùng Khác & Mỹ Nghệ",
        "icon": "package",
        "badge_color": "slate",
        "description": "Dược phẩm, dụng cụ y tế, đồ chơi trẻ em, nhạc cụ, tác phẩm mỹ nghệ, vàng bạc đá quý",
        "chapters": ["30", "47", "48", "49", "71", "92", "93", "95", "96", "97"]
    }
}

# Danh bạ 97 Chương WCO đầy đủ (Chương 01 -> 97, Chương 77 dự phòng)
ALL_97_CHAPTERS = [
    # Nhóm Nông Nghiệp & Động Vật (Ch. 01 - 05)
    {
        "code": "01",
        "name_vi": "Động vật sống (Gia súc, gia cầm, ngựa, bò, lợn)",
        "name_en": "Live animals",
        "section": 1,
        "cluster": "agri_food",
        "volume_rank": 45,
        "alpha_letter": "D",
        "keywords": ["dong vat song", "bo", "heo", "lon", "ga", "ngua", "live animals", "cattle"],
        "sample_hs": [{"hs": "0102.29", "name": "Bò sống thuần chủng giống"}, {"hs": "0105.11", "name": "Gà giống bố mẹ"}]
    },
    {
        "code": "02",
        "name_vi": "Thịt và phụ phẩm dạng thịt ăn được sau giết mổ",
        "name_en": "Meat and edible meat offal",
        "section": 1,
        "cluster": "agri_food",
        "volume_rank": 20,
        "alpha_letter": "T",
        "keywords": ["thit", "thit bo", "thit heo", "thit ga", "meat", "pork", "beef", "poultry"],
        "sample_hs": [{"hs": "0202.30", "name": "Thịt bò đông lạnh rút xương"}, {"hs": "0207.14", "name": "Đùi gà đông lạnh"}]
    },
    {
        "code": "03",
        "name_vi": "Cá và động vật giáp xác, động vật thân mềm (Thủy hải sản)",
        "name_en": "Fish and crustaceans, molluscs (Seafood)",
        "section": 1,
        "cluster": "agri_food",
        "volume_rank": 6,
        "alpha_letter": "C",
        "keywords": ["ca", "tom", "muc", "thuy san", "hai san", "ca tra", "tom su", "seafood", "fish", "shrimp"],
        "sample_hs": [{"hs": "0306.17", "name": "Tôm sú & tôm thẻ đông lạnh"}, {"hs": "0304.62", "name": "Cá tra, basa phi lê đông lạnh"}]
    },
    {
        "code": "04",
        "name_vi": "Sữa, sản phẩm từ sữa; trứng chim; mật ong tự nhiên",
        "name_en": "Dairy produce; birds' eggs; natural honey",
        "section": 1,
        "cluster": "agri_food",
        "volume_rank": 22,
        "alpha_letter": "S",
        "keywords": ["sua", "pho mai", "mat ong", "trung", "dairy", "milk", "cheese", "honey"],
        "sample_hs": [{"hs": "0402.10", "name": "Sữa bột nguyên kem"}, {"hs": "0409.00", "name": "Mật ong hoa cà phê tự nhiên"}]
    },
    {
        "code": "05",
        "name_vi": "Sản phẩm gốc động vật khác chưa được chi tiết",
        "name_en": "Products of animal origin, not elsewhere specified",
        "section": 1,
        "cluster": "agri_food",
        "volume_rank": 58,
        "alpha_letter": "S",
        "keywords": ["long vu", "ruot dong vat", "mong sung", "feathers", "guts"],
        "sample_hs": [{"hs": "0505.10", "name": "Lông vũ dùng nhồi áo phao"}, {"hs": "0504.00", "name": "Ruột động vật làm vỏ xúc xích"}]
    },

    # Nhóm Nông Sản Thực Vật (Ch. 06 - 14)
    {
        "code": "06",
        "name_vi": "Cây sống và hoa cắt cành trang trí",
        "name_en": "Live trees and other plants; cut flowers",
        "section": 2,
        "cluster": "agri_food",
        "volume_rank": 48,
        "alpha_letter": "C",
        "keywords": ["hoa", "cay canh", "hoa lan", "hoa hong", "flowers", "plants", "orchids"],
        "sample_hs": [{"hs": "0603.11", "name": "Hoa hồng tươi cắt cành"}, {"hs": "0602.90", "name": "Cây giống nuôi cấy mô"}]
    },
    {
        "code": "07",
        "name_vi": "Rau, củ, thân củ và rễ ăn được",
        "name_en": "Edible vegetables and certain roots and tubers",
        "section": 2,
        "cluster": "agri_food",
        "volume_rank": 19,
        "alpha_letter": "R",
        "keywords": ["rau", "cu", "khoai tay", "hanh toi", "nam", "vegetables", "onions", "garlic", "potatoes"],
        "sample_hs": [{"hs": "0703.20", "name": "Tỏi khô xuất khẩu"}, {"hs": "0709.60", "name": "Ớt tươi xuất khẩu"}]
    },
    {
        "code": "08",
        "name_vi": "Quả và quả hạch ăn được; hạt điều, sầu riêng, thanh long",
        "name_en": "Edible fruit and nuts; citrus fruit or melons",
        "section": 2,
        "cluster": "agri_food",
        "volume_rank": 4,
        "alpha_letter": "Q",
        "keywords": ["hat dieu", "sau rieng", "thanh long", "trai cay", "hoa qua", "chuoi", "fruit", "cashew", "durian"],
        "sample_hs": [{"hs": "0801.32", "name": "Hạt điều nhân xuất khẩu W320"}, {"hs": "0810.60", "name": "Sầu riêng tươi múi đông lạnh"}]
    },
    {
        "code": "09",
        "name_vi": "Cà phê, chè (trà), hạt tiêu, quế, hồi và gia vị",
        "name_en": "Coffee, tea, maté and spices",
        "section": 2,
        "cluster": "agri_food",
        "volume_rank": 5,
        "alpha_letter": "C",
        "keywords": ["ca phe", "tieu", "che", "tra", "que", "hoi", "gia vi", "coffee", "pepper", "tea", "cinnamon"],
        "sample_hs": [{"hs": "0901.11", "name": "Cà phê Robusta nhân thô Grade 1"}, {"hs": "0904.11", "name": "Hồ tiêu đen khô FAQ"}]
    },
    {
        "code": "10",
        "name_vi": "Ngũ cốc (Gạo thơm ST25, ngô, lúa mì, đại mạch)",
        "name_en": "Cereals (Rice, wheat, corn)",
        "section": 2,
        "cluster": "agri_food",
        "volume_rank": 7,
        "alpha_letter": "G",
        "keywords": ["gao", "gao st25", "lua mi", "ngo", "bap", "rice", "wheat", "corn", "cereals"],
        "sample_hs": [{"hs": "1006.30", "name": "Gạo thơm ST25 xuất khẩu"}, {"hs": "1005.90", "name": "Ngô hạt sấy khô thức ăn chăn nuôi"}]
    },
    {
        "code": "11",
        "name_vi": "Sản phẩm xay xát; bột mì, tinh bột sắn, mạch nha",
        "name_en": "Products of the milling industry; malt; starches",
        "section": 2,
        "cluster": "agri_food",
        "volume_rank": 16,
        "alpha_letter": "T",
        "keywords": ["tinh bot san", "bot mi", "bot gao", "mach nha", "starch", "tapioca", "flour"],
        "sample_hs": [{"hs": "1108.14", "name": "Tinh bột sắn biến tính (Tapioca starch)"}, {"hs": "1101.00", "name": "Bột mì làm bánh"}]
    },
    {
        "code": "12",
        "name_vi": "Hạt có dầu; đậu nành, hạt vừng, cây dược liệu",
        "name_en": "Oil seeds and oleaginous fruits; medicinal plants",
        "section": 2,
        "cluster": "agri_food",
        "volume_rank": 21,
        "alpha_letter": "H",
        "keywords": ["dau nanh", "vung", "me", "duoc lieu", "soybeans", "sesame", "oil seeds"],
        "sample_hs": [{"hs": "1201.90", "name": "Đậu nành hạt nhập khẩu"}, {"hs": "1207.40", "name": "Hạt vừng trắng"}]
    },
    {
        "code": "13",
        "name_vi": "Nhựa cây, chất gôm và chất chiết xuất từ thực vật",
        "name_en": "Lac; gums, resins and other vegetable saps",
        "section": 2,
        "cluster": "agri_food",
        "volume_rank": 62,
        "alpha_letter": "N",
        "keywords": ["nhua thong", "chat chiet", "agar", "resins", "gum"],
        "sample_hs": [{"hs": "1301.90", "name": "Nhựa thông đã sơ chế"}, {"hs": "1302.19", "name": "Chất chiết thảo dược"}]
    },
    {
        "code": "14",
        "name_vi": "Vật liệu thắt tết từ thực vật (Mây, tre, nứa, cói)",
        "name_en": "Vegetable plaiting materials (Bamboo, rattan)",
        "section": 2,
        "cluster": "agri_food",
        "volume_rank": 52,
        "alpha_letter": "M",
        "keywords": ["may", "tre", "nua", "coi", "luc binh", "bamboo", "rattan"],
        "sample_hs": [{"hs": "1401.10", "name": "Tre nguyên liệu chế biến"}, {"hs": "1401.20", "name": "Song mây đan lát"}]
    },

    # Nhóm Dầu Mỡ & Thực Phẩm Chế Biến (Ch. 15 - 24)
    {
        "code": "15",
        "name_vi": "Mỡ và dầu động thực vật; dầu cọ, dầu đậu nành",
        "name_en": "Animal or vegetable fats and oils",
        "section": 3,
        "cluster": "agri_food",
        "volume_rank": 17,
        "alpha_letter": "D",
        "keywords": ["dau an", "dau co", "dau dua", "dau nanh", "palm oil", "coconut oil"],
        "sample_hs": [{"hs": "1511.90", "name": "Dầu cọ tinh luyện"}, {"hs": "1513.19", "name": "Dầu dừa nguyên chất ép lạnh"}]
    },
    {
        "code": "16",
        "name_vi": "Chế phẩm từ thịt, cá, tôm đóng hộp hoặc chế biến sẵn",
        "name_en": "Preparations of meat, of fish or of crustaceans",
        "section": 4,
        "cluster": "agri_food",
        "volume_rank": 10,
        "alpha_letter": "C",
        "keywords": ["ca dong hop", "thit hop", "tom che bien", "canned tuna", "canned fish"],
        "sample_hs": [{"hs": "1604.14", "name": "Cá ngừ đóng hộp ngâm dầu"}, {"hs": "1605.21", "name": "Tôm tẩm bột đông lạnh"}]
    },
    {
        "code": "17",
        "name_vi": "Đường và các loại kẹo đường",
        "name_en": "Sugars and sugar confectionery",
        "section": 4,
        "cluster": "agri_food",
        "volume_rank": 26,
        "alpha_letter": "D",
        "keywords": ["duong", "keo", "duong mia", "sugar", "candy"],
        "sample_hs": [{"hs": "1701.99", "name": "Đường mía tinh luyện RE"}, {"hs": "1704.90", "name": "Kẹo dẻo các loại"}]
    },
    {
        "code": "18",
        "name_vi": "Ca cao và các chế phẩm từ ca cao (Sô cô la)",
        "name_en": "Cocoa and cocoa preparations (Chocolate)",
        "section": 4,
        "cluster": "agri_food",
        "volume_rank": 38,
        "alpha_letter": "C",
        "keywords": ["ca cao", "socola", "chocolate", "cocoa beans"],
        "sample_hs": [{"hs": "1801.00", "name": "Hạt ca cao lên men"}, {"hs": "1806.32", "name": "Sô cô la dạng thanh"}]
    },
    {
        "code": "19",
        "name_vi": "Chế phẩm từ bột; mì ăn liền, bánh ngọt, bún khô",
        "name_en": "Preparations of cereals, flour; bakery wares",
        "section": 4,
        "cluster": "agri_food",
        "volume_rank": 14,
        "alpha_letter": "M",
        "keywords": ["mi an lien", "banh khao", "bun kho", "banh quy", "instant noodles", "biscuits"],
        "sample_hs": [{"hs": "1902.30", "name": "Mì ăn liền xuất khẩu"}, {"hs": "1905.31", "name": "Bánh quy ngọt đóng hộp"}]
    },
    {
        "code": "20",
        "name_vi": "Chế phẩm từ rau quả; nước ép trái cây, mứt, rau muối",
        "name_en": "Preparations of vegetables, fruit, nuts",
        "section": 4,
        "cluster": "agri_food",
        "volume_rank": 18,
        "alpha_letter": "N",
        "keywords": ["nuoc ep", "dua muoi", "xoai say", "mut", "fruit juice", "dried mango"],
        "sample_hs": [{"hs": "2009.89", "name": "Nước ép chanh dây cô đặc"}, {"hs": "2008.99", "name": "Xoài sấy dẻo xuất khẩu"}]
    },
    {
        "code": "21",
        "name_vi": "Chế phẩm ăn được khác (Gia vị nêm, nước mắm, cà phê hòa tan)",
        "name_en": "Miscellaneous edible preparations (Sauces, instant coffee)",
        "section": 4,
        "cluster": "agri_food",
        "volume_rank": 15,
        "alpha_letter": "G",
        "keywords": ["nuoc mam", "ca phe hoa tan", "tuong ot", "fish sauce", "instant coffee", "sauces"],
        "sample_hs": [{"hs": "2101.11", "name": "Cà phê hòa tan 3 trong 1"}, {"hs": "2103.90", "name": "Nước mắm Phú Quốc truyền thống"}]
    },
    {
        "code": "22",
        "name_vi": "Đồ uống, rượu vang, bia, nước giải khát và giấm",
        "name_en": "Beverages, spirits and vinegar (Beer, wine)",
        "section": 4,
        "cluster": "agri_food",
        "volume_rank": 24,
        "alpha_letter": "B",
        "keywords": ["bia", "ruou", "nuoc giai khat", "beer", "wine", "spirits", "beverages"],
        "sample_hs": [{"hs": "2203.00", "name": "Bia đóng lon xuất khẩu"}, {"hs": "2202.99", "name": "Nước tăng lực đóng lon"}]
    },
    {
        "code": "23",
        "name_vi": "Phế liệu công nghiệp thực phẩm; thức ăn gia súc (Bã đậu nành)",
        "name_en": "Residues and waste from food industries; animal feed",
        "section": 4,
        "cluster": "agri_food",
        "volume_rank": 9,
        "alpha_letter": "T",
        "keywords": ["thuc an chan nuoi", "ba dau nanh", "cam gao", "animal feed", "soybean meal"],
        "sample_hs": [{"hs": "2304.00", "name": "Bã khô dầu đậu nành"}, {"hs": "2309.90", "name": "Thức ăn hỗn hợp cho tôm"}]
    },
    {
        "code": "24",
        "name_vi": "Thuốc lá và các sản phẩm thay thế lá thuốc lá",
        "name_en": "Tobacco and manufactured tobacco substitutes",
        "section": 4,
        "cluster": "agri_food",
        "volume_rank": 35,
        "alpha_letter": "T",
        "keywords": ["thuoc la", "xiga", "tobacco", "cigarettes"],
        "sample_hs": [{"hs": "2401.20", "name": "Lá thuốc lá đã sấy khô"}, {"hs": "2402.20", "name": "Thuốc lá điếu"}]
    },

    # Nhóm Khoáng Sản, Dầu Khí & Năng Lượng (Ch. 25 - 27)
    {
        "code": "25",
        "name_vi": "Muối, lưu huỳnh, đất, đá, vôi, thạch cao và xi măng",
        "name_en": "Salt; sulphur; earths and stone; plastering materials, cement",
        "section": 5,
        "cluster": "materials_chemicals",
        "volume_rank": 25,
        "alpha_letter": "X",
        "keywords": ["xi mang", "clinker", "cat", "da vo", "cement", "clinker", "limestone", "salt"],
        "sample_hs": [{"hs": "2523.10", "name": "Clinker xi măng xuất khẩu"}, {"hs": "2517.10", "name": "Đá xây dựng dăm nghiền"}]
    },
    {
        "code": "26",
        "name_vi": "Quặng, xỉ và tro khoáng sản (Quặng sắt, đồng, titan)",
        "name_en": "Ores, slag and ash (Iron ore, bauxite)",
        "section": 5,
        "cluster": "materials_chemicals",
        "volume_rank": 28,
        "alpha_letter": "Q",
        "keywords": ["quang sat", "bauxite", "titan", "iron ore", "bauxite", "minerals"],
        "sample_hs": [{"hs": "2601.11", "name": "Quặng sắt chưa nung kết"}, {"hs": "2614.00", "name": "Quặng titan và tinh quặng"}]
    },
    {
        "code": "27",
        "name_vi": "Nhiên liệu khoáng, dầu mỏ, than đá, khí đốt tự nhiên",
        "name_en": "Mineral fuels, mineral oils (Crude oil, coal, LNG)",
        "section": 5,
        "cluster": "materials_chemicals",
        "volume_rank": 8,
        "alpha_letter": "D",
        "keywords": ["dau tho", "xang dau", "than da", "khi dot", "coal", "crude oil", "petroleum", "gas"],
        "sample_hs": [{"hs": "2709.00", "name": "Dầu mỏ thô khai thác"}, {"hs": "2701.12", "name": "Than đá bitum xuất khẩu"}]
    },

    # Nhóm Hóa Chất & Phân Bón (Ch. 28 - 38)
    {
        "code": "28",
        "name_vi": "Hóa chất vô cơ; axit, kiềm, hợp chất clo, kim loại hiếm",
        "name_en": "Inorganic chemicals; compounds of precious metals",
        "section": 6,
        "cluster": "materials_chemicals",
        "volume_rank": 23,
        "alpha_letter": "H",
        "keywords": ["axit", "xut", "clo", "hoa chat vo co", "soda", "sulfuric acid", "caustic soda"],
        "sample_hs": [{"hs": "2815.11", "name": "Xút ăn da NaOH dạng rắn"}, {"hs": "2807.00", "name": "Axit sunfuric H2SO4"}]
    },
    {
        "code": "29",
        "name_vi": "Hóa chất hữu cơ; hydrocacbon, cồn, este công nghiệp",
        "name_en": "Organic chemicals",
        "section": 6,
        "cluster": "materials_chemicals",
        "volume_rank": 27,
        "alpha_letter": "H",
        "keywords": ["con", "ethanol", "methanol", "dung moi", "organic chemicals"],
        "sample_hs": [{"hs": "2905.11", "name": "Methanol công nghiệp"}, {"hs": "2902.50", "name": "Styren monomer tinh khiết"}]
    },
    {
        "code": "30",
        "name_vi": "Dược phẩm; thuốc kháng sinh, vắc xin, bông băng y tế",
        "name_en": "Pharmaceutical products",
        "section": 6,
        "cluster": "special_consumer",
        "volume_rank": 11,
        "alpha_letter": "D",
        "keywords": ["thuoc", "duoc pham", "vac xin", "khang sinh", "medicine", "pharmaceuticals", "vaccines"],
        "sample_hs": [{"hs": "3004.90", "name": "Thuốc tân dược thành phẩm đóng gói"}, {"hs": "3002.20", "name": "Vắc xin phòng bệnh người"}]
    },
    {
        "code": "31",
        "name_vi": "Phân bón (Urea, DAP, NPK, Kali, SA, lân hữu cơ)",
        "name_en": "Fertilisers (Urea, DAP, NPK)",
        "section": 6,
        "cluster": "materials_chemicals",
        "volume_rank": 12,
        "alpha_letter": "P",
        "keywords": ["phan bon", "urea", "dap", "npk", "kali", "dam", "fertilizer"],
        "sample_hs": [{"hs": "3102.10", "name": "Phân đạm Urea hạt đục / hạt trong"}, {"hs": "3105.20", "name": "Phân khoáng NPK phức hợp"}]
    },
    {
        "code": "32",
        "name_vi": "Chất chiết xuất nhuộm; sơn, vecni, mực in và bột màu",
        "name_en": "Tanning or dyeing extracts; paints, inks",
        "section": 6,
        "cluster": "materials_chemicals",
        "volume_rank": 33,
        "alpha_letter": "S",
        "keywords": ["son", "muc in", "bot mau", "chat nhuom", "paints", "inks", "dyes"],
        "sample_hs": [{"hs": "3208.90", "name": "Sơn công nghiệp hệ dung môi"}, {"hs": "3215.11", "name": "Mực in offset đen"}]
    },
    {
        "code": "33",
        "name_vi": "Tinh dầu và mỹ phẩm, chế phẩm trang điểm, nước hoa",
        "name_en": "Essential oils and resinoids; cosmetics",
        "section": 6,
        "cluster": "special_consumer",
        "volume_rank": 29,
        "alpha_letter": "M",
        "keywords": ["my pham", "tinh dau", "nuoc hoa", "son moi", "kem duong", "cosmetics", "perfumes"],
        "sample_hs": [{"hs": "3304.99", "name": "Kem dưỡng da mặt và cơ thể"}, {"hs": "3301.29", "name": "Tinh dầu sả chanh nguyên chất"}]
    },
    {
        "code": "34",
        "name_vi": "Xà phòng, chất tẩy rửa, sáp nhân tạo và chất bôi trơn",
        "name_en": "Soap, washing preparations, waxes",
        "section": 6,
        "cluster": "materials_chemicals",
        "volume_rank": 36,
        "alpha_letter": "X",
        "keywords": ["xa phong", "nuoc giat", "nuoc rua chen", "soap", "detergent"],
        "sample_hs": [{"hs": "3402.20", "name": "Nước giặt xả đóng can"}, {"hs": "3401.11", "name": "Xà bông tắm thảo dược"}]
    },
    {
        "code": "35",
        "name_vi": "Chất keo, albumin, gelatin, enzym công nghiệp",
        "name_en": "Albuminoidal substances; modified starches; glues; enzymes",
        "section": 6,
        "cluster": "materials_chemicals",
        "volume_rank": 46,
        "alpha_letter": "K",
        "keywords": ["keo", "gelatin", "enzym", "glue", "gelatin"],
        "sample_hs": [{"hs": "3506.91", "name": "Keo dán gỗ công nghiệp PVA"}, {"hs": "3503.00", "name": "Gelatin thực phẩm dạng hạt"}]
    },
    {
        "code": "36",
        "name_vi": "Chất nổ, pháo hoa, diêm, hợp kim tự cháy",
        "name_en": "Explosives; pyrotechnic products; matches",
        "section": 6,
        "cluster": "materials_chemicals",
        "volume_rank": 65,
        "alpha_letter": "C",
        "keywords": ["thuoc no", "phao hoa", "diem", "explosives", "fireworks"],
        "sample_hs": [{"hs": "3604.10", "name": "Pháo hoa lễ hội"}, {"hs": "3602.00", "name": "Thuốc nổ mỏ đá"}]
    },
    {
        "code": "37",
        "name_vi": "Vật liệu dùng cho nhiếp ảnh hoặc điện ảnh (Phim, bản kẽm)",
        "name_en": "Photographic or cinematographic goods",
        "section": 6,
        "cluster": "materials_chemicals",
        "volume_rank": 70,
        "alpha_letter": "P",
        "keywords": ["phim", "ban kem in", "film", "photographic plates"],
        "sample_hs": [{"hs": "3701.30", "name": "Bản kẽm CTP in offset"}, {"hs": "3702.39", "name": "Phim chụp X-quang y tế"}]
    },
    {
        "code": "38",
        "name_vi": "Các chế phẩm hóa chất hỗn hợp (Thuốc BVTV, phụ gia bê tông)",
        "name_en": "Miscellaneous chemical products (Pesticides, additives)",
        "section": 6,
        "cluster": "materials_chemicals",
        "volume_rank": 18,
        "alpha_letter": "T",
        "keywords": ["thuoc bao ve thuc vat", "thuoc tru sau", "phu gia", "pesticides", "additives"],
        "sample_hs": [{"hs": "3808.91", "name": "Thuốc trừ sâu sinh học"}, {"hs": "3824.40", "name": "Phụ gia đông kết bê tông"}]
    },

    # Nhóm Nhựa & Cao Su (Ch. 39 - 40)
    {
        "code": "39",
        "name_vi": "Chất dẻo (Nhựa nguyên sinh PE, PP, PVC, bao bì nhựa)",
        "name_en": "Plastics and articles thereof (PE, PP, PVC)",
        "section": 7,
        "cluster": "materials_chemicals",
        "volume_rank": 3,
        "alpha_letter": "N",
        "keywords": ["nhua", "hat nhua", "nhua pp", "nhua pe", "bao bi nhua", "plastics", "polymers"],
        "sample_hs": [{"hs": "3901.10", "name": "Hạt nhựa Polyethylene (PE) tỷ trọng thấp"}, {"hs": "3923.21", "name": "Bao bì túi màng nhựa xuất khẩu"}]
    },
    {
        "code": "40",
        "name_vi": "Cao su tự nhiên, cao su tổng hợp, lốp xe tải",
        "name_en": "Rubber and articles thereof (Natural rubber, tyres)",
        "section": 7,
        "cluster": "materials_chemicals",
        "volume_rank": 13,
        "alpha_letter": "C",
        "keywords": ["cao su", "mu cao su", "lop xe", "sam lop", "rubber", "latex", "tyres"],
        "sample_hs": [{"hs": "4001.22", "name": "Cao su tự nhiên TSR 20 khối"}, {"hs": "4011.20", "name": "Lốp xe tải Radial xuất khẩu"}]
    },

    # Nhóm Da, Gỗ, Giấy (Ch. 41 - 49)
    {
        "code": "41",
        "name_vi": "Da sống và da thuộc nguyên liệu (Da bò, da trâu)",
        "name_en": "Raw hides and skins and leather",
        "section": 8,
        "cluster": "fashion_footwear",
        "volume_rank": 34,
        "alpha_letter": "D",
        "keywords": ["da song", "da thuoc", "leather", "raw hides"],
        "sample_hs": [{"hs": "4104.11", "name": "Da bò muối ướt nguyên con"}, {"hs": "4107.12", "name": "Da thuộc làm sofa"}]
    },
    {
        "code": "42",
        "name_vi": "Sản phẩm bằng da; túi xách, va li, ví, thắt lưng da",
        "name_en": "Articles of leather; saddlery; travel goods, handbags",
        "section": 8,
        "cluster": "fashion_footwear",
        "volume_rank": 15,
        "alpha_letter": "T",
        "keywords": ["tui xach", "vali", "vi da", "balo", "handbags", "luggage", "backpacks"],
        "sample_hs": [{"hs": "4202.12", "name": "Va li kéo du lịch vỏ nhựa/da"}, {"hs": "4202.21", "name": "Túi xách nữ da bò thật"}]
    },
    {
        "code": "43",
        "name_vi": "Da lông và lông thú nhân tạo",
        "name_en": "Furskins and artificial fur",
        "section": 8,
        "cluster": "fashion_footwear",
        "volume_rank": 75,
        "alpha_letter": "L",
        "keywords": ["long thu", "fur", "furskins"],
        "sample_hs": [{"hs": "4303.10", "name": "Áo khoác da lông thú"}, {"hs": "4304.00", "name": "Vải lông nhân tạo"}]
    },
    {
        "code": "44",
        "name_vi": "Gỗ và sản phẩm bằng gỗ; dăm gỗ, viên nén mùn cưa, ván ép",
        "name_en": "Wood and articles of wood; wood charcoal, pellets, plywood",
        "section": 9,
        "cluster": "construction_furniture",
        "volume_rank": 5,
        "alpha_letter": "G",
        "keywords": ["go", "dam go", "vien nen go", "van ep", "plywood", "wood pellets", "timber", "lumber"],
        "sample_hs": [{"hs": "4401.31", "name": "Viên nén mùn cưa (Wood pellets ENplus)"}, {"hs": "4412.33", "name": "Ván ép Plywood phủ phim chịu nước"}]
    },
    {
        "code": "45",
        "name_vi": "Chất bần và các mặt hàng bằng chất bần (Nút chai)",
        "name_en": "Cork and articles of cork",
        "section": 9,
        "cluster": "construction_furniture",
        "volume_rank": 80,
        "alpha_letter": "N",
        "keywords": ["nut chai", "chat ban", "cork"],
        "sample_hs": [{"hs": "4503.10", "name": "Nút bần chai rượu vang"}, {"hs": "4504.10", "name": "Tấm bần cách âm sàn"}]
    },
    {
        "code": "46",
        "name_vi": "Sản phẩm bằng mây, rơm, cỏ bện (Hàng thủ công mỹ nghệ)",
        "name_en": "Manufactures of straw, of esparto or of other plaiting materials",
        "section": 9,
        "cluster": "construction_furniture",
        "volume_rank": 39,
        "alpha_letter": "T",
        "keywords": ["thu cong my nghe", "gio may", "chieu coi", "handicrafts", "baskets"],
        "sample_hs": [{"hs": "4602.11", "name": "Giỏ đan bằng tre xuất khẩu"}, {"hs": "4601.21", "name": "Thảm dệt từ cói tự nhiên"}]
    },
    {
        "code": "47",
        "name_vi": "Bột giấy từ gỗ hoặc sợi xenluloza tái chế",
        "name_en": "Pulp of wood or of other fibrous cellulosic material",
        "section": 10,
        "cluster": "special_consumer",
        "volume_rank": 40,
        "alpha_letter": "B",
        "keywords": ["bot giay", "pulp", "wood pulp"],
        "sample_hs": [{"hs": "4703.21", "name": "Bột giấy hóa học gỗ lá kim tẩy trắng"}, {"hs": "4707.10", "name": "Giấy phế liệu thu hồi tái chế"}]
    },
    {
        "code": "48",
        "name_vi": "Giấy và bìa các tông; thùng carton, giấy in văn phòng",
        "name_en": "Paper and paperboard; cartons, printing paper",
        "section": 10,
        "cluster": "special_consumer",
        "volume_rank": 16,
        "alpha_letter": "G",
        "keywords": ["giay", "thung carton", "giay cuon", "paper", "cardboard", "packaging"],
        "sample_hs": [{"hs": "4819.10", "name": "Thùng hộp giấy carton sóng 3-5 lớp"}, {"hs": "4802.56", "name": "Giấy A4 in văn phòng 70-80gsm"}]
    },
    {
        "code": "49",
        "name_vi": "Sách, báo, tranh ảnh và các sản phẩm của ngành in ấn",
        "name_en": "Printed books, newspapers, pictures (Printing industry)",
        "section": 10,
        "cluster": "special_consumer",
        "volume_rank": 43,
        "alpha_letter": "S",
        "keywords": ["sach", "tap chi", "tem nhan", "books", "printing", "labels"],
        "sample_hs": [{"hs": "4901.99", "name": "Sách in xuất bản phẩm"}, {"hs": "4911.99", "name": "Tem nhãn in decal thương mại"}]
    },

    # Nhóm Dệt May & Giày Dép (Ch. 50 - 67)
    {
        "code": "50",
        "name_vi": "Tơ tằm và sợi tơ tằm",
        "name_en": "Silk",
        "section": 11,
        "cluster": "fashion_footwear",
        "volume_rank": 55,
        "alpha_letter": "T",
        "keywords": ["to tam", "lua", "silk"],
        "sample_hs": [{"hs": "5002.00", "name": "Tơ tằm thô chưa xe"}, {"hs": "5007.20", "name": "Vải lụa tơ tằm tự nhiên"}]
    },
    {
        "code": "51",
        "name_vi": "Lông cừu, lông động vật và vải từ lông cừu (Len)",
        "name_en": "Wool, fine or coarse animal hair; horsehair yarn",
        "section": 11,
        "cluster": "fashion_footwear",
        "volume_rank": 50,
        "alpha_letter": "L",
        "keywords": ["len", "long cuu", "wool"],
        "sample_hs": [{"hs": "5101.11", "name": "Lông cừu chưa cạo sạch"}, {"hs": "5112.11", "name": "Vải len may veston cao cấp"}]
    },
    {
        "code": "52",
        "name_vi": "Bông (Cotton), sợi bông và vải dệt thoi từ bông",
        "name_en": "Cotton, cotton yarn and woven fabrics",
        "section": 11,
        "cluster": "fashion_footwear",
        "volume_rank": 8,
        "alpha_letter": "B",
        "keywords": ["bong", "cotton", "soi cotton", "vai cotton", "cotton yarn"],
        "sample_hs": [{"hs": "5201.00", "name": "Bông thô chưa chải kỹ nhập khẩu"}, {"hs": "5205.12", "name": "Sợi đơn từ bông combed"}]
    },
    {
        "code": "53",
        "name_vi": "Xơ sợi dệt thực vật khác; sợi lanh, sợi đay",
        "name_en": "Other vegetable textile fibres; paper yarn and fabrics",
        "section": 11,
        "cluster": "fashion_footwear",
        "volume_rank": 59,
        "alpha_letter": "S",
        "keywords": ["soi lanh", "soi day", "linen", "jute"],
        "sample_hs": [{"hs": "5309.11", "name": "Vải dệt từ sợi lanh tự nhiên"}, {"hs": "5303.10", "name": "Sợi đay thô dệt bao bố"}]
    },
    {
        "code": "54",
        "name_vi": "Sợi filament nhân tạo; sợi polyester, sợi nylon",
        "name_en": "Man-made filaments; strip and the like",
        "section": 11,
        "cluster": "fashion_footwear",
        "volume_rank": 11,
        "alpha_letter": "S",
        "keywords": ["soi polyester", "soi nylon", "filament", "polyester yarn"],
        "sample_hs": [{"hs": "5402.33", "name": "Sợi filament polyester DTY"}, {"hs": "5407.52", "name": "Vải dệt thoi từ sợi polyester nhuộm màu"}]
    },
    {
        "code": "55",
        "name_vi": "Xơ staple nhân tạo (Xơ ngắn polyester dệt thoi)",
        "name_en": "Man-made staple fibres",
        "section": 11,
        "cluster": "fashion_footwear",
        "volume_rank": 14,
        "alpha_letter": "X",
        "keywords": ["xo staple", "staple fibres", "polyester staple"],
        "sample_hs": [{"hs": "5503.20", "name": "Xơ polyester staple (PSF) tái sinh"}, {"hs": "5509.21", "name": "Sợi đơn từ xơ nhân tạo"}]
    },
    {
        "code": "56",
        "name_vi": "Bền lót, phớt dệt, vải không dệt; dây thừng dệt",
        "name_en": "Wadding, felt and nonwovens; special yarns; twine, cordage",
        "section": 11,
        "cluster": "fashion_footwear",
        "volume_rank": 31,
        "alpha_letter": "V",
        "keywords": ["vai khong det", "day thung", "non-woven", "ropes"],
        "sample_hs": [{"hs": "5603.12", "name": "Vải không dệt may khẩu trang y tế"}, {"hs": "5607.49", "name": "Dây thừng bện neo tàu biển"}]
    },
    {
        "code": "57",
        "name_vi": "Thảm và các loại hàng dệt trải sàn khác",
        "name_en": "Carpets and other textile floor coverings",
        "section": 11,
        "cluster": "construction_furniture",
        "volume_rank": 47,
        "alpha_letter": "T",
        "keywords": ["tham", "tham trai san", "carpets", "rugs"],
        "sample_hs": [{"hs": "5703.20", "name": "Thảm dệt chần sợi nylon văn phòng"}, {"hs": "5702.42", "name": "Thảm cuộn dệt hoa văn"}]
    },
    {
        "code": "58",
        "name_vi": "Vải dệt thoi đặc biệt; vải nhung, ren, thêu",
        "name_en": "Special woven fabrics; tufted textile fabrics; lace; tapestries",
        "section": 11,
        "cluster": "fashion_footwear",
        "volume_rank": 41,
        "alpha_letter": "R",
        "keywords": ["ren", "nhung", "theu", "velvet", "lace"],
        "sample_hs": [{"hs": "5804.21", "name": "Vải ren dệt may váy đầm"}, {"hs": "5801.32", "name": "Vải nhung dệt từ sợi tổng hợp"}]
    },
    {
        "code": "59",
        "name_vi": "Vải dệt tráng phủ, vải kỹ thuật công nghiệp",
        "name_en": "Impregnated, coated, covered or laminated textile fabrics",
        "section": 11,
        "cluster": "materials_chemicals",
        "volume_rank": 37,
        "alpha_letter": "V",
        "keywords": ["vai tráng nhua", "vai bat", "tarpaulin", "coated fabric"],
        "sample_hs": [{"hs": "5903.10", "name": "Vải dệt tráng nhựa PVC làm bạt xe"}, {"hs": "5902.10", "name": "Vải mành nylon làm lốp xe hơi"}]
    },
    {
        "code": "60",
        "name_vi": "Vải dệt kim hoặc móc (Knitted fabrics)",
        "name_en": "Knitted or crocheted fabrics",
        "section": 11,
        "cluster": "fashion_footwear",
        "volume_rank": 12,
        "alpha_letter": "V",
        "keywords": ["vai det kim", "vai thun", "knitted fabric", "jersey"],
        "sample_hs": [{"hs": "6006.22", "name": "Vải dệt kim từ sợi bông nhuộm màu (Vải cotton 100%)"}, {"hs": "6004.10", "name": "Vải thun dệt kim co giãn spandex"}]
    },
    {
        "code": "61",
        "name_vi": "Quần áo và hàng may mặc phụ trợ dệt kim (Áo thun, polo, đồ thể thao)",
        "name_en": "Articles of apparel and clothing accessories, knitted or crocheted",
        "section": 11,
        "cluster": "fashion_footwear",
        "volume_rank": 2,
        "alpha_letter": "A",
        "keywords": ["ao thun", "ao phong", "ao polo", "quan ao det kim", "t-shirt", "garment", "polo"],
        "sample_hs": [{"hs": "6109.10", "name": "Áo thun T-shirt dệt kim từ bông (Cotton)"}, {"hs": "6110.20", "name": "Áo len chui đầu dài tay"}]
    },
    {
        "code": "62",
        "name_vi": "Quần áo và hàng may mặc dệt thoi (Sơ mi, quần âu, veston, áo khoác)",
        "name_en": "Articles of apparel and clothing accessories, not knitted (Woven garments)",
        "section": 11,
        "cluster": "fashion_footwear",
        "volume_rank": 3,
        "alpha_letter": "S",
        "keywords": ["ao so mi", "quan jean", "quan tay", "ao khoac", "vest", "shirts", "jeans", "trousers", "jackets"],
        "sample_hs": [{"hs": "6205.20", "name": "Áo sơ mi nam dệt thoi từ sợi bông"}, {"hs": "6203.42", "name": "Quần dài quần jeans nam"}]
    },
    {
        "code": "63",
        "name_vi": "Hàng dệt may sẵn khác; chăn màn, rèm cửa, ga gối",
        "name_en": "Other made-up textile articles; sets; worn clothing",
        "section": 11,
        "cluster": "fashion_footwear",
        "volume_rank": 19,
        "alpha_letter": "C",
        "keywords": ["chan ga goi", "rem cua", "khan tam", "bedding", "towels", "curtains"],
        "sample_hs": [{"hs": "6302.60", "name": "Khăn tắm khăn mặt dệt từ bông"}, {"hs": "6304.92", "name": "Vỏ ga trải giường khách sạn"}]
    },
    {
        "code": "64",
        "name_vi": "Giày, dép xuất khẩu (Giày thể thao, giày da, dép sandal)",
        "name_en": "Footwear, gaiters and the like (Shoes, sneakers)",
        "section": 12,
        "cluster": "fashion_footwear",
        "volume_rank": 4,
        "alpha_letter": "G",
        "keywords": ["giay the thao", "giay da", "dep", "sneakers", "shoes", "footwear", "boots"],
        "sample_hs": [{"hs": "6404.11", "name": "Giày thể thao đế cao su mặt vải (Sneakers)"}, {"hs": "6403.99", "name": "Giày tây nam đế da thật"}]
    },
    {
        "code": "65",
        "name_vi": "Mũ, nón và các vật đội đầu khác",
        "name_en": "Headgear and parts thereof",
        "section": 12,
        "cluster": "fashion_footwear",
        "volume_rank": 42,
        "alpha_letter": "M",
        "keywords": ["mu", "non", "mu luoi trai", "caps", "hats"],
        "sample_hs": [{"hs": "6505.00", "name": "Mũ lưỡi trai dệt may xuất khẩu"}, {"hs": "6506.10", "name": "Mũ bảo hiểm xe máy đạt chuẩn"}]
    },
    {
        "code": "66",
        "name_vi": "Ô, dù, gậy ba toong, roi da điều khiển ngựa",
        "name_en": "Umbrellas, sun umbrellas, walking-sticks",
        "section": 12,
        "cluster": "fashion_footwear",
        "volume_rank": 66,
        "alpha_letter": "O",
        "keywords": ["o", "du", "umbrellas"],
        "sample_hs": [{"hs": "6601.99", "name": "Ô che mưa cầm tay gấp gọn"}]
    },
    {
        "code": "67",
        "name_vi": "Lông vũ đã xử lý, hoa giả, tóc giả",
        "name_en": "Prepared feathers and down; artificial flowers; articles of human hair",
        "section": 12,
        "cluster": "special_consumer",
        "volume_rank": 53,
        "alpha_letter": "H",
        "keywords": ["hoa gia", "toc gia", "artificial flowers", "wigs"],
        "sample_hs": [{"hs": "6702.10", "name": "Hoa lụa cành giả trang trí"}, {"hs": "6704.11", "name": "Tóc giả sợi tổng hợp"}]
    },

    # Nhóm Vật Liệu Xây Dựng, Gốm Sứ & Đá Quý (Ch. 68 - 71)
    {
        "code": "68",
        "name_vi": "Sản phẩm bằng đá, thạch cao, xi măng, amiăng, mica",
        "name_en": "Articles of stone, plaster, cement, asbestos, mica",
        "section": 13,
        "cluster": "construction_furniture",
        "volume_rank": 28,
        "alpha_letter": "D",
        "keywords": ["da hoa cuong", "da granite", "tam thach cao", "granite", "stone tiles"],
        "sample_hs": [{"hs": "6802.21", "name": "Đá marble cẩm thạch xẻ tấm"}, {"hs": "6809.11", "name": "Tấm trần thạch cao chống ẩm"}]
    },
    {
        "code": "69",
        "name_vi": "Đồ gốm sứ; gạch ốp lát, thiết bị vệ sinh sứ",
        "name_en": "Ceramic products; tiles, sanitary fixtures",
        "section": 13,
        "cluster": "construction_furniture",
        "volume_rank": 21,
        "alpha_letter": "G",
        "keywords": ["gach op lat", "gom su", "bon cau", "lavabo", "ceramics", "tiles", "sanitary"],
        "sample_hs": [{"hs": "6907.21", "name": "Gạch ốp lát granite tráng men"}, {"hs": "6910.10", "name": "Bồn cầu sứ vệ sinh cao cấp"}]
    },
    {
        "code": "70",
        "name_vi": "Thủy tinh và sản phẩm thủy tinh (Kính xây dựng, chai lọ)",
        "name_en": "Glass and glassware (Float glass, bottles)",
        "section": 13,
        "cluster": "construction_furniture",
        "volume_rank": 23,
        "alpha_letter": "T",
        "keywords": ["kinh xay dung", "chai thuy tinh", "ly coc", "glass", "glassware"],
        "sample_hs": [{"hs": "7005.29", "name": "Kính nổi xây dựng cường lực"}, {"hs": "7010.90", "name": "Chai thủy tinh đựng rượu"}]
    },
    {
        "code": "71",
        "name_vi": "Ngọc trai tự nhiên, đá quý, kim loại quý (Vàng, bạc, trang sức)",
        "name_en": "Natural pearls, precious stones, precious metals (Gold, jewelry)",
        "section": 14,
        "cluster": "special_consumer",
        "volume_rank": 30,
        "alpha_letter": "V",
        "keywords": ["vang", "bac", "da quy", "kim cuong", "trang suc", "gold", "silver", "diamonds", "jewelry"],
        "sample_hs": [{"hs": "7113.19", "name": "Trang sức vàng nữ trang 18k"}, {"hs": "7102.39", "name": "Kim cương đã mài giác cắt"}]
    },

    # Nhóm Kim Loại Cơ Bản & Cơ Khí (Ch. 72 - 83)
    {
        "code": "72",
        "name_vi": "Sắt và thép (Thép cuộn cán nóng HRC, phôi thép, thép thanh)",
        "name_en": "Iron and steel (HRC, rebar, steel billets)",
        "section": 15,
        "cluster": "materials_chemicals",
        "volume_rank": 3,
        "alpha_letter": "S",
        "keywords": ["thep", "sat thep", "thep cuon", "thep hrc", "phoi thep", "steel", "iron", "rebar"],
        "sample_hs": [{"hs": "7208.39", "name": "Thép cuộn cán nóng HRC không hợp kim"}, {"hs": "7214.20", "name": "Thép thanh vằn xây dựng (Rebar)"}]
    },
    {
        "code": "73",
        "name_vi": "Sản phẩm bằng sắt hoặc thép (Ống thép, kết cấu thép, bu lông)",
        "name_en": "Articles of iron or steel (Tubes, pipes, structures)",
        "section": 15,
        "cluster": "materials_chemicals",
        "volume_rank": 7,
        "alpha_letter": "O",
        "keywords": ["ong thep", "ket cau thep", "bu long", "oc vit", "steel pipes", "fasteners"],
        "sample_hs": [{"hs": "7306.30", "name": "Ống thép hàn mạ kẽm nhúng nóng"}, {"hs": "7308.90", "name": "Khung giàn kết cấu thép nhà xưởng"}]
    },
    {
        "code": "74",
        "name_vi": "Đồng và các sản phẩm bằng đồng (Đồng đỏ, dây đồng)",
        "name_en": "Copper and articles thereof (Copper cathodes, wire)",
        "section": 15,
        "cluster": "materials_chemicals",
        "volume_rank": 17,
        "alpha_letter": "D",
        "keywords": ["dong", "dong catot", "day dong", "copper", "copper wire"],
        "sample_hs": [{"hs": "7403.11", "name": "Đồng tấm Catot tinh khiết 99.99%"}, {"hs": "7408.11", "name": "Dây đồng đỏ kỹ thuật điện"}]
    },
    {
        "code": "75",
        "name_vi": "Niken và các sản phẩm bằng niken",
        "name_en": "Nickel and articles thereof",
        "section": 15,
        "cluster": "materials_chemicals",
        "volume_rank": 56,
        "alpha_letter": "N",
        "keywords": ["niken", "nickel"],
        "sample_hs": [{"hs": "7502.10", "name": "Niken chưa gia công hợp kim"}]
    },
    {
        "code": "76",
        "name_vi": "Nhôm và các sản phẩm bằng nhôm (Nhôm định hình, nhôm thỏi)",
        "name_en": "Aluminium and articles thereof (Extrusions, ingots)",
        "section": 15,
        "cluster": "materials_chemicals",
        "volume_rank": 9,
        "alpha_letter": "N",
        "keywords": ["nhom", "nhom dinh hinh", "nhom thoi", "aluminium", "aluminum profiles"],
        "sample_hs": [{"hs": "7604.21", "name": "Nhôm định hình cửa kính kiến trúc"}, {"hs": "7601.10", "name": "Nhôm thỏi nguyên chất"}]
    },
    {
        "code": "77",
        "name_vi": "(Dành riêng cho WCO sử dụng trong tương lai)",
        "name_en": "Reserved for possible future use in the HS by WCO",
        "section": 15,
        "cluster": "materials_chemicals",
        "volume_rank": 97,
        "alpha_letter": "D",
        "keywords": ["wco", "du phong", "reserved"],
        "sample_hs": []
    },
    {
        "code": "78",
        "name_vi": "Chì và các sản phẩm bằng chì",
        "name_en": "Lead and articles thereof",
        "section": 15,
        "cluster": "materials_chemicals",
        "volume_rank": 72,
        "alpha_letter": "C",
        "keywords": ["chi", "lead ingots"],
        "sample_hs": [{"hs": "7801.10", "name": "Chì tinh luyện dạng thỏi đúc"}]
    },
    {
        "code": "79",
        "name_vi": "Kẽm và các sản phẩm bằng kẽm",
        "name_en": "Zinc and articles thereof",
        "section": 15,
        "cluster": "materials_chemicals",
        "volume_rank": 54,
        "alpha_letter": "K",
        "keywords": ["kem", "kem thoi", "zinc"],
        "sample_hs": [{"hs": "7901.11", "name": "Kẽm thỏi mạ điện phân"}]
    },
    {
        "code": "80",
        "name_vi": "Thiếc và các sản phẩm bằng thiếc",
        "name_en": "Tin and articles thereof",
        "section": 15,
        "cluster": "materials_chemicals",
        "volume_rank": 68,
        "alpha_letter": "T",
        "keywords": ["thiec", "tin ingots"],
        "sample_hs": [{"hs": "8001.10", "name": "Thiếc thỏi hàn điện tử"}]
    },
    {
        "code": "81",
        "name_vi": "Các kim loại cơ bản khác; cermet và sản phẩm của chúng",
        "name_en": "Other base metals; cermets; articles thereof (Titanium, tungsten)",
        "section": 15,
        "cluster": "materials_chemicals",
        "volume_rank": 64,
        "alpha_letter": "T",
        "keywords": ["titan", "vonfram", "tungsten", "titanium"],
        "sample_hs": [{"hs": "8108.20", "name": "Titan dạng thỏi gia công cơ khí"}]
    },
    {
        "code": "82",
        "name_vi": "Dụng cụ cầm tay, lưỡi dao, đồ cắt gọt kim loại",
        "name_en": "Tools, implements, cutlery, spoons and forks",
        "section": 15,
        "cluster": "materials_chemicals",
        "volume_rank": 26,
        "alpha_letter": "D",
        "keywords": ["dung cu", "kim", "bua", "mo let", "luoi phay", "tools", "hand tools"],
        "sample_hs": [{"hs": "8207.50", "name": "Mũi khoan kim loại CNC carbide"}, {"hs": "8204.11", "name": "Cờ lê mỏ lết cầm tay"}]
    },
    {
        "code": "83",
        "name_vi": "Khóa, bản lề, khung giá kim loại tạp trị",
        "name_en": "Miscellaneous articles of base metal (Locks, hinges)",
        "section": 15,
        "cluster": "materials_chemicals",
        "volume_rank": 32,
        "alpha_letter": "K",
        "keywords": ["khoa", "ban le", "tay nam cua", "locks", "hinges", "hardware"],
        "sample_hs": [{"hs": "8301.40", "name": "Khóa cửa cơ khí thông minh"}, {"hs": "8302.10", "name": "Bản lề cửa inox 304"}]
    },

    # Nhóm Máy Móc, Điện Tử & Công Nghệ (Ch. 84 - 85 - Chiếm Tỷ Trọng Lớn Nhất VN)
    {
        "code": "84",
        "name_vi": "Nồi hơi, máy móc cơ khí, động cơ đốt trong, máy tính xách tay",
        "name_en": "Nuclear reactors, boilers, machinery and mechanical appliances; computers",
        "section": 16,
        "cluster": "tech_machinery",
        "volume_rank": 1,
        "alpha_letter": "M",
        "keywords": ["may moc", "may tinh", "may in", "dong co", "laptop", "machinery", "engines", "computers"],
        "sample_hs": [{"hs": "8471.30", "name": "Máy tính xách tay Laptop siêu mỏng"}, {"hs": "8428.39", "name": "Hệ thống băng chuyền tự động công nghiệp"}]
    },
    {
        "code": "85",
        "name_vi": "Máy móc, thiết bị điện thoại, điện tử, vi mạch bán dẫn và âm thanh",
        "name_en": "Electrical machinery and equipment; sound recorders; semiconductors, smartphones",
        "section": 16,
        "cluster": "tech_machinery",
        "volume_rank": 1,
        "alpha_letter": "D",
        "keywords": ["dien thoai", "vi mach", "chip", "dien tu", "ti vi", "smartphones", "chips", "semiconductors", "electronics"],
        "sample_hs": [{"hs": "8517.13", "name": "Điện thoại thông minh (Smartphones)"}, {"hs": "8542.31", "name": "Bộ vi xử lý tích hợp (Integrated circuits / Chip)"}]
    },

    # Nhóm Phương Tiện Vận Tải (Ch. 86 - 89)
    {
        "code": "86",
        "name_vi": "Đầu máy, toa xe lửa và các thiết bị tín hiệu đường sắt",
        "name_en": "Railway or tramway locomotives, rolling stock and parts thereof",
        "section": 17,
        "cluster": "transport_logistics",
        "volume_rank": 67,
        "alpha_letter": "D",
        "keywords": ["toa xe lua", "duong sat", "railway"],
        "sample_hs": [{"hs": "8606.91", "name": "Toa xe chở hàng đường sắt kín"}]
    },
    {
        "code": "87",
        "name_vi": "Ô tô, xe máy, xe tải, xe kéo và phụ tùng linh kiện xe cơ giới",
        "name_en": "Vehicles other than railway (Cars, trucks, motorcycles, auto parts)",
        "section": 17,
        "cluster": "transport_logistics",
        "volume_rank": 5,
        "alpha_letter": "O",
        "keywords": ["o to", "xe tai", "xe may", "phu tung o to", "cars", "trucks", "motorcycles", "auto parts"],
        "sample_hs": [{"hs": "8703.23", "name": "Xe ô tô con dung tích 1500cc - 2000cc"}, {"hs": "8708.29", "name": "Linh kiện phụ tùng thân xe hơi"}]
    },
    {
        "code": "88",
        "name_vi": "Phương tiện bay, tàu vũ trụ và các bộ phận phụ tùng",
        "name_en": "Aircraft, spacecraft, and parts thereof",
        "section": 17,
        "cluster": "transport_logistics",
        "volume_rank": 44,
        "alpha_letter": "M",
        "keywords": ["may bay", "flycam", "drone", "aircraft", "drones"],
        "sample_hs": [{"hs": "8806.22", "name": "Thiết bị bay không người lái Drone có camera"}, {"hs": "8807.30", "name": "Cánh quạt và cánh lái máy bay"}]
    },
    {
        "code": "89",
        "name_vi": "Tàu thủy, thuyền bè và các kết cấu nổi phục vụ hàng hải",
        "name_en": "Ships, boats and floating structures",
        "section": 17,
        "cluster": "transport_logistics",
        "volume_rank": 30,
        "alpha_letter": "T",
        "keywords": ["tau thuy", "xa lan", "cano", "tau cho hang", "ships", "boats", "barges"],
        "sample_hs": [{"hs": "8901.90", "name": "Tàu chở hàng rời trọng tải 20,000 DWT"}, {"hs": "8905.10", "name": "Tàu hút bùn nạo vét cảng"}]
    },

    # Nhóm Thiết Bị Đo Lường, Y Tế, Nội Thất & Đồ Chơi (Ch. 90 - 97)
    {
        "code": "90",
        "name_vi": "Dụng cụ đo lường, quang học, chụp chiếu y tế và kính mắt",
        "name_en": "Optical, photographic, medical or surgical instruments",
        "section": 18,
        "cluster": "tech_machinery",
        "volume_rank": 10,
        "alpha_letter": "T",
        "keywords": ["thiet bi y te", "may sieu am", "kinh mat", "dong ho do", "medical equipment", "optical"],
        "sample_hs": [{"hs": "9018.12", "name": "Máy siêu âm màu y tế 4D"}, {"hs": "9004.10", "name": "Kính mát thời trang chống UV"}]
    },
    {
        "code": "91",
        "name_vi": "Đồng hồ đeo tay, đồng hồ treo tường và các bộ phận",
        "name_en": "Clocks and watches and parts thereof",
        "section": 18,
        "cluster": "tech_machinery",
        "volume_rank": 49,
        "alpha_letter": "D",
        "keywords": ["dong ho", "dong ho deo tay", "watches", "clocks"],
        "sample_hs": [{"hs": "9102.11", "name": "Đồng hồ đeo tay điện tử thạch anh"}, {"hs": "9102.21", "name": "Đồng hồ đeo tay cơ khí tự động"}]
    },
    {
        "code": "92",
        "name_vi": "Nhạc cụ (Đàn piano, đàn guitar, trống, kèn)",
        "name_en": "Musical instruments; parts and accessories",
        "section": 18,
        "cluster": "special_consumer",
        "volume_rank": 69,
        "alpha_letter": "N",
        "keywords": ["nhac cu", "guitar", "piano", "musical instruments"],
        "sample_hs": [{"hs": "9202.90", "name": "Đàn guitar acoustic gỗ tự nhiên"}, {"hs": "9201.10", "name": "Đàn piano đứng Upright"}]
    },
    {
        "code": "93",
        "name_vi": "Vũ khí, đạn dược và các bộ phận phụ kiện chuyên dụng",
        "name_en": "Arms and ammunition; parts and accessories thereof",
        "section": 19,
        "cluster": "special_consumer",
        "volume_rank": 78,
        "alpha_letter": "V",
        "keywords": ["vu khi", "dan", "arms", "ammunition"],
        "sample_hs": [{"hs": "9306.30", "name": "Đạn ghém săn bắn thể thao"}]
    },
    {
        "code": "94",
        "name_vi": "Đồ nội thất, giường, nệm, ghế sofa, đèn và biển hiệu chiếu sáng",
        "name_en": "Furniture; bedding, mattresses, lamps and lighting fittings",
        "section": 20,
        "cluster": "construction_furniture",
        "volume_rank": 4,
        "alpha_letter": "D",
        "keywords": ["noi that", "ban ghe", "sofa", "giuong", "nem", "den led", "furniture", "sofas", "lighting"],
        "sample_hs": [{"hs": "9403.60", "name": "Bàn ghế đồ gỗ nội thất phòng ăn/phòng khách"}, {"hs": "9401.61", "name": "Ghế sofa bọc nệm khung gỗ"}]
    },
    {
        "code": "95",
        "name_vi": "Đồ chơi, trò chơi, dụng cụ thể thao và đồ dùng giải trí",
        "name_en": "Toys, games and sports requisites",
        "section": 20,
        "cluster": "special_consumer",
        "volume_rank": 13,
        "alpha_letter": "D",
        "keywords": ["do choi", "tro choi", "dung cu the thao", "lego", "bup be", "toys", "games", "sports equipment"],
        "sample_hs": [{"hs": "9503.00", "name": "Đồ chơi mô hình lắp ráp thông minh"}, {"hs": "9506.62", "name": "Quả bóng đá tiêu chuẩn FIFA"}]
    },
    {
        "code": "96",
        "name_vi": "Hàng tạp hóa chế tạo khác (Bút viết, bật lửa, bàn chải đánh răng)",
        "name_en": "Miscellaneous manufactured articles (Pens, buttons, lighters)",
        "section": 20,
        "cluster": "special_consumer",
        "volume_rank": 32,
        "alpha_letter": "B",
        "keywords": ["but bi", "ban chai", "khoa keo", "bat lua", "pens", "buttons", "zippers"],
        "sample_hs": [{"hs": "9608.10", "name": "Bút bi mực gel đầu bi 0.5mm"}, {"hs": "9603.21", "name": "Bàn chải đánh răng sợi tơ"}]
    },
    {
        "code": "97",
        "name_vi": "Tác phẩm nghệ thuật, đồ sưu tầm và đồ cổ trên 100 năm",
        "name_en": "Works of art, collectors' pieces and antiques",
        "section": 21,
        "cluster": "special_consumer",
        "volume_rank": 74,
        "alpha_letter": "T",
        "keywords": ["tranh ve", "do co", "art", "antiques", "paintings"],
        "sample_hs": [{"hs": "9701.21", "name": "Tranh sơn dầu vẽ tay nguyên bản"}, {"hs": "9706.00", "name": "Đồ cổ niên đại trên 100 năm"}]
    }
]

def get_catalog_by_view_mode(mode="volume"):
    """
    Trả về danh bạ phân nhóm theo đúng 4 chế độ trải nghiệm tìm kiếm:
    1. 'volume': Sắp xếp theo Top Kim Ngạch Xuất Nhập Khẩu & Tần suất Giao dịch
    2. 'clusters': Nhóm thành 6 Cụm Chuỗi Giá Trị & Mục Đích Sử Dụng
    3. 'alphabet': Sắp xếp theo Bảng Chữ Cái (A -> Z)
    4. 'wco': Thứ tự Số học Chuẩn WCO Hải Quan (Chương 01 -> 97 qua 21 Phần)
    """
    if mode == "volume":
        sorted_list = sorted(ALL_97_CHAPTERS, key=lambda x: (x["volume_rank"], int(x["code"])))
        return {
            "mode": "volume",
            "title": "Top Ngành Hàng Kim Ngạch Lớn & Giao Dịch Phổ Biến Nhất",
            "description": "Ưu tiên các nhóm ngành có quy mô xuất nhập khẩu hàng đầu (Điện thoại/Điện tử, Nông sản, Dệt may, Da giày, Gỗ, Sắt thép, Nhựa...)",
            "data": sorted_list
        }
    
    elif mode == "clusters":
        clusters_data = []
        for c_id, c_meta in END_USE_CLUSTERS.items():
            ch_list = [ch for ch in ALL_97_CHAPTERS if ch["code"] in c_meta["chapters"]]
            # Sắp xếp nội bộ cụm theo kim ngạch
            ch_list.sort(key=lambda x: (x["volume_rank"], int(x["code"])))
            clusters_data.append({
                "cluster_id": c_id,
                "name_vi": c_meta["name_vi"],
                "icon": c_meta["icon"],
                "badge_color": c_meta["badge_color"],
                "description": c_meta["description"],
                "chapter_count": len(ch_list),
                "chapters": ch_list
            })
        return {
            "mode": "clusters",
            "title": "6 Cụm Chuỗi Giá Trị & Mục Đích Sử Dụng",
            "description": "Gom 97 chương HS thành các nhóm ứng dụng thực tế trực quan để người dùng tìm nhanh theo nhóm công nghiệp",
            "data": clusters_data
        }

    elif mode == "alphabet":
        groups = {}
        for ch in ALL_97_CHAPTERS:
            let = ch["alpha_letter"].upper()
            if let not in groups:
                groups[let] = []
            groups[let].append(ch)
        
        alphabet_list = []
        for let in sorted(groups.keys()):
            alphabet_list.append({
                "letter": let,
                "count": len(groups[let]),
                "chapters": sorted(groups[let], key=lambda x: x["name_vi"])
            })
        return {
            "mode": "alphabet",
            "title": "Tra Cứu Theo Bảng Chữ Cái (A ➔ Z)",
            "description": "Dành cho người dùng tìm kiếm theo tên chữ quen thuộc (A: Áo quần, C: Cà phê/Cá, G: Gạo/Gỗ/Giày, S: Sắt thép...)",
            "data": alphabet_list
        }

    elif mode == "wco":
        # Gom theo 21 Phần WCO
        sections_data = []
        for sec in WCO_SECTIONS:
            sec_num = sec["section"]
            sec_chapters = [ch for ch in ALL_97_CHAPTERS if ch["section"] == sec_num]
            sec_chapters.sort(key=lambda x: int(x["code"]))
            sections_data.append({
                "section_num": sec_num,
                "roman": sec["roman"],
                "name_vi": sec["name_vi"],
                "chapter_range": sec["chapters"],
                "chapter_count": len(sec_chapters),
                "chapters": sec_chapters
            })
        return {
            "mode": "wco",
            "title": "Hệ Thống Hải Quan Chuẩn WCO (Chương 01 ➔ 97)",
            "description": "Chuẩn hóa theo 21 Phần (Sections) và 97 Chương (Chapters) của Tổ chức Hải quan Thế giới",
            "data": sections_data
        }

    return get_catalog_by_view_mode("volume")

def search_hs_omni(query, limit=15):
    """
    Tìm kiếm thông minh tức thì theo từ khóa tiếng Việt (có dấu/không dấu) hoặc mã HS
    """
    q = (query or "").strip().lower()
    if not q:
        return ALL_97_CHAPTERS[:limit]
    
    matches = []
    for ch in ALL_97_CHAPTERS:
        score = 0
        code = ch["code"]
        name_vi = ch["name_vi"].lower()
        name_en = ch["name_en"].lower()
        keywords = [k.lower() for k in ch.get("keywords", [])]

        if q == code:
            score += 100
        elif code.startswith(q):
            score += 70
        
        if q in name_vi:
            score += 50
        if q in name_en:
            score += 40
        if any(q in kw for kw in keywords):
            score += 60

        for s_hs in ch.get("sample_hs", []):
            if q in s_hs["hs"].replace(".", "") or q in s_hs["hs"]:
                score += 80
            if q in s_hs["name"].lower():
                score += 45

        if score > 0:
            item_copy = dict(ch)
            item_copy["search_relevance"] = score
            matches.append(item_copy)

    matches.sort(key=lambda x: x["search_relevance"], reverse=True)
    return matches[:limit]
