#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Từ Điển Tra Cứu Quy Chuẩn Thẻ Tag Ngoại Thương (Trade Criteria Tag Dictionary)
Định nghĩa chi tiết phân loại, ý nghĩa thực tế và khuyến nghị nghiệp vụ khi thương thảo
"""

TRADE_TAG_CATALOG = {
    # 1. Specs (Quy cách kỹ thuật)
    "#Moist_Max12.5%": {
        "name": "Độ ẩm tối đa 12.5% (Moisture Max 12.5%)",
        "category": "Quy Cách Kỹ Thuật (Specs)",
        "desc": "Quy chuẩn độ ẩm an toàn cao nhất cho phép đối với nông sản khô (cà phê nhân, hạt tiêu, ngũ cốc). Đảm bảo hàng hóa không bị nấm mốc hoặc lên men sinh nhiệt trong hành trình vận chuyển biển dài ngày.",
        "advice": "Yêu cầu cấp Chứng thư Giám định độ ẩm độc lập (SGS / Vinacontrol / Cafecontrol) trước khi niêm phong chì container."
    },
    "#Screen_S18": {
        "name": "Kích thước hạt Sàng 18 (Screen 18 - 7.1mm)",
        "category": "Quy Cách Kỹ Thuật (Specs)",
        "desc": "Quy chuẩn phân loại cỡ hạt nông sản (cà phê, hạt điều) có đường kính lỗ sàng 7.1mm. Đây là phẩm cấp hạt loại 1 cao cấp (Grade 1), giá trị thương phẩm cao nhất trên sàn giao dịch quốc tế.",
        "advice": "Tỷ lệ hạt trên sàng 18 phải đạt tối thiểu 90% khối lượng mẫu thử nghiệm theo tiêu chuẩn hợp đồng."
    },
    "#Screen_S16": {
        "name": "Kích thước hạt Sàng 16 (Screen 16 - 6.3mm)",
        "category": "Quy Cách Kỹ Thuật (Specs)",
        "desc": "Quy chuẩn cỡ hạt nông sản qua sàng 16 (đường kính lỗ sàng 6.3mm), là phẩm cấp hạt tiêu chuẩn thương mại phổ thông (Grade 2) dùng cho rang xay và chế biến công nghiệp.",
        "advice": "Thích hợp làm hàng phối trộn công nghiệp; giá thành cạnh tranh hơn so với Sàng 18."
    },
    "#Urea_N46%": {
        "name": "Hàm lượng Đạm Nitơ tối thiểu 46.0% (Urea N46%)",
        "category": "Quy Cách Kỹ Thuật (Specs)",
        "desc": "Tiêu chuẩn quốc tế cao nhất cho phân đạm Urê tinh khiết. Hàm lượng Nitơ đạt từ 46% trở lên, đảm bảo hiệu suất dinh dưỡng tối đa cho cây trồng.",
        "advice": "Yêu cầu giấy phân tích chất lượng COA kiểm tra thêm hàm lượng Biuret (phải dưới 1.0%) để tránh làm cháy lá cây trồng."
    },
    "#Granular": {
        "name": "Dạng hạt to đúc nén (Granular 2.0 - 4.75mm)",
        "category": "Quy Cách Kỹ Thuật (Specs)",
        "desc": "Quy chuẩn phân bón/hóa chất dạng hạt to tròn ép nén. Có độ cứng cao, chống vỡ vụn, ít hút ẩm, tan chậm và hạn chế vón cục khi vận chuyển biển dài ngày.",
        "advice": "Rất phù hợp cho máy bón phân cơ giới và vận chuyển hàng rời (bulk) bằng tàu hàng khô chuyên dụng."
    },
    "#Prilled": {
        "name": "Dạng hạt tháp mịn (Prilled 1.0 - 2.8mm)",
        "category": "Quy Cách Kỹ Thuật (Specs)",
        "desc": "Dạng hạt phân bón tròn nhỏ mịn tạo từ tháp làm lạnh. Độ đồng đều cao, tốc độ hòa tan trong nước cực nhanh, thích hợp cho hệ thống tưới tự động hoặc phun hòa tan.",
        "advice": "Cần đóng bao màng PE kép chống ẩm cẩn thận trong kho bảo quản để chống chảy nước."
    },
    "#WhiteMeat": {
        "name": "Phi lê thịt trắng cao cấp (White Meat Spec)",
        "category": "Quy Cách Kỹ Thuật (Specs)",
        "desc": "Quy chuẩn phi lê thủy sản (cá tra, cá basa, cá tuyết) yêu cầu thịt trắng tinh khiết, lọc sạch hoàn toàn mỡ, da, xương và không bị vệt đỏ/màu vàng.",
        "advice": "Thị trường Mỹ và Châu Âu định giá thịt trắng cao hơn 15 - 25% so với thịt hồng hoặc vàng nhạt."
    },
    "#Glazing_10-20%": {
        "name": "Tỷ lệ mạ băng bảo quản lạnh 10% - 20% (Glazing)",
        "category": "Quy Cách Kỹ Thuật (Specs)",
        "desc": "Lớp nước tinh khiết mạ băng bao bọc bên ngoài sản phẩm đông lạnh để bảo vệ bề mặt thịt cá khỏi hiện tượng cháy lạnh (freezer burn) và oxy hóa trong quá trình lưu trữ.",
        "advice": "Hợp đồng ngoại thương phải ghi rõ 'Net Weight without Glazing' (Trọng lượng tịnh thực không tính nước mạ băng) để tránh tranh chấp hải quan."
    },
    "#DeepFrozen_-20C": {
        "name": "Cấp đông sâu âm 20 độ C (Deep Frozen -20°C)",
        "category": "Quy Cách Kỹ Thuật (Specs)",
        "desc": "Tiêu chuẩn bảo quản lạnh nhiệt độ tâm sản phẩm đạt từ -18°C đến -20°C xuyên suốt chuỗi logistics bằng container lạnh Reefer và kho lạnh chuyên dụng.",
        "advice": "Bắt buộc đặt thiết bị theo dõi nhiệt độ điện tử (Temperature Data Logger) trong từng container để đối chiếu bảo hiểm hàng hải khi hàng đến cảng."
    },
    "#ASTM_A500": {
        "name": "Tiêu chuẩn Thép kết cấu nguội ASTM A500",
        "category": "Quy Cách Kỹ Thuật (Specs)",
        "desc": "Tiêu chuẩn kỹ thuật Hoa Kỳ quy định cho thép hộp, ống thép hàn kết cấu dạng tròn, vuông và chữ nhật. Đáp ứng khả năng chịu lực, uốn dẻo và tính hàn trong xây dựng.",
        "advice": "Yêu cầu Mill Test Certificate (MTC) từ nhà máy ghi rõ giới hạn chảy (Yield Strength) và độ bền kéo (Tensile Strength)."
    },
    "#Zinc_Z275": {
        "name": "Độ dày lớp mạ kẽm tối thiểu 275 g/m² (Zinc Coating Z275)",
        "category": "Quy Cách Kỹ Thuật (Specs)",
        "desc": "Quy chuẩn mạ kẽm nhúng nóng hai mặt đạt tổng khối lượng kẽm 275 g/m². Cung cấp khả năng kháng ăn mòn muối biển vượt trội và tuổi thọ trên 25 năm ngoài trời.",
        "advice": "Tiêu chuẩn bắt buộc cho công trình ven biển, giàn khung điện mặt trời và nhà xưởng công nghiệp."
    },
    "#WoodPellet_6-8mm": {
        "name": "Viên nén gỗ sinh khối đường kính 6 - 8mm",
        "category": "Quy Cách Kỹ Thuật (Specs)",
        "desc": "Kích thước tiêu chuẩn công nghiệp của viên nén nhiên liệu sinh khối (Wood Pellets) phục vụ lò hơi nhà máy nhiệt điện than Nhật Bản và Hàn Quốc.",
        "advice": "Đảm bảo độ nén chặt, độ bền cơ học cao để hạn chế tỷ lệ mùn vụn phát sinh khi rót hàng lên tàu rời."
    },
    "#Caloric_Min4200kcal": {
        "name": "Nhiệt lượng sinh nhiệt tối thiểu 4,200 kcal/kg",
        "category": "Quy Cách Kỹ Thuật (Specs)",
        "desc": "Mức nhiệt năng cháy tiêu chuẩn của viên nén gỗ loại 1, hàm lượng tro dưới 1.5%, không phối trộn phụ gia hóa chất hay vỏ cây độc hại.",
        "advice": "Yêu cầu giấy chứng nhận kiểm nghiệm nhiệt lượng từ cơ quan kiểm định độc lập SGS hoặc Intertek."
    },
    "#Clean_FAQ": {
        "name": "Phẩm cấp thương mại sạch chuẩn FAQ (Fair Average Quality)",
        "category": "Quy Cách Kỹ Thuật (Specs)",
        "desc": "Tiêu chuẩn chất lượng trung bình khá phổ biến trong thương mại nông sản thế giới, sàng sạch tạp chất lớn, tỷ lệ hạt hỏng và hạt lép dưới ngưỡng quy định.",
        "advice": "Phù hợp làm nguyên liệu thô đầu vào cho các nhà máy tinh chế công nghiệp."
    },

    # 2. Certifications (Tiêu chuẩn & Chứng chỉ chất lượng)
    "#HACCP": {
        "name": "Phân tích Mối nguy & Điểm Kiểm soát Tới hạn HACCP",
        "category": "Chứng Chỉ Chất Lượng (Cert)",
        "desc": "Hệ thống quản lý an toàn thực phẩm được quốc tế công nhận, kiểm soát nguy cơ vật lý, hóa học và sinh học tại các công đoạn chế biến trọng yếu.",
        "advice": "Điều kiện tiên quyết để được cấp phép xuất khẩu nông - thủy sản chế biến vào hầu hết các quốc gia."
    },
    "#ISO22000": {
        "name": "Hệ thống Quản lý An Toàn Thực Phẩm ISO 22000",
        "category": "Chứng Chỉ Chất Lượng (Cert)",
        "desc": "Tiêu chuẩn an toàn thực phẩm tích hợp giữa hệ thống HACCP và quy trình quản trị doanh nghiệp ISO, bao phủ toàn bộ chuỗi cung ứng từ nông trại đến bàn ăn.",
        "advice": "Giúp đối tác nhập khẩu tin tưởng tuyệt đối vào quy trình truy xuất nguồn gốc và kiểm soát rủi ro của nhà máy."
    },
    "#ISO9001": {
        "name": "Hệ thống Quản lý Chất lượng Tiêu chuẩn Quốc tế ISO 9001",
        "category": "Chứng Chỉ Chất Lượng (Cert)",
        "desc": "Chứng nhận doanh nghiệp sở hữu quy trình vận hành và kiểm soát chất lượng sản xuất đồng bộ, ổn định và tuân thủ nghiêm ngặt các quy định tiêu chuẩn.",
        "advice": "Là thước đo cơ bản để các tập đoàn đa quốc gia phê duyệt nhà cung cấp vào danh sách Vendor đủ điều kiện."
    },
    "#Rainforest_Alliance": {
        "name": "Chứng nhận Nông nghiệp Bền vững Rainforest Alliance",
        "category": "Chứng Chỉ Bền Vững (ESG)",
        "desc": "Chứng chỉ quốc tế chứng minh sản phẩm nông sản (cà phê, cacao, chè) được canh tác bảo vệ rừng tự nhiên, không hủy hoại sinh thái, bảo vệ đất và đảm bảo phúc lợi xã hội người lao động.",
        "advice": "Thị trường Châu Âu và Bắc Mỹ ưu tiên thu mua và sẵn sàng trả mức giá chênh lệch thưởng (Premium) $50 - $120/tấn cho hàng có chứng chỉ này."
    },
    "#FDA_US": {
        "name": "Đăng ký Cơ sở Thực phẩm Cục Quản lý FDA Hoa Kỳ",
        "category": "Chứng Nhận Pháp Lý Mỹ",
        "desc": "Nhà máy sản xuất đã được cấp mã số đăng ký FFRN (Food Facility Registration Number) với FDA và chỉ định đại lý pháp lý tại Mỹ (U.S. Agent), đủ điều kiện thông quan vào Hoa Kỳ.",
        "advice": "Phải nộp Thông Báo Trước Khi Nhập Khẩu (Prior Notice) trước khi tàu cập cảng Mỹ để tránh bị giữ hàng tại cảng."
    },
    "#CE_Europe": {
        "name": "Dấu Hợp Chuẩn Châu Âu CE Marking (Conformité Européenne)",
        "category": "Dấu Hợp Chuẩn EU",
        "desc": "Tuyên bố của nhà sản xuất rằng sản phẩm (thép, vật liệu xây dựng, thiết bị điện máy) tuân thủ đầy đủ các chỉ thị an toàn, sức khỏe và bảo vệ môi trường của Liên minh Châu Âu.",
        "advice": "Hàng hóa không có dấu CE hợp pháp sẽ bị từ chối thông quan và cấm lưu hành trên toàn bộ 27 quốc gia EU."
    },
    "#REACH_EU": {
        "name": "Quy định Đăng ký & Đánh giá Hóa chất Châu Âu (REACH)",
        "category": "Tuân Thủ Môi Trường EU",
        "desc": "Quy định khắt khe của EU kiểm soát việc sử dụng hóa chất và các chất có nguy cơ rất cao (SVHC) trong sản phẩm dệt may, da giày, phân bón và hàng tiêu dùng.",
        "advice": "Cần cung cấp bảng kiểm định hàm lượng kim loại nặng và hóa chất cấm từ các phòng thử nghiệm được EU ủy quyền."
    },
    "#Halal_JAKIM": {
        "name": "Chứng nhận Tiêu chuẩn Hồi giáo Halal (JAKIM / BPJPH / GCC)",
        "category": "Chứng Chỉ Halal Quốc Tế",
        "desc": "Xác nhận toàn bộ nguyên liệu, phụ gia và dây chuyền chế biến hoàn toàn hợp pháp theo luật Sharia của người Hồi giáo; tuyệt đối không nhiễm cấm (Haram) hoặc nhiễm bẩn (Najis).",
        "advice": "Tấm vé vàng mở toang cánh cửa xuất khẩu sang thị trường 2 tỷ dân tại Indonesia, Malaysia và các nước vùng Vịnh GCC."
    },
    "#GlobalGAP": {
        "name": "Thực hành Nông nghiệp Tốt Toàn cầu GlobalGAP",
        "category": "Tiêu Chuẩn Nông Nghiệp",
        "desc": "Bộ tiêu chuẩn trang trại toàn cầu kiểm soát an toàn thực phẩm từ khâu làm đất, hạt giống, nguồn nước tưới, thuốc bảo vệ thực vật đến khâu thu hoạch và đóng gói ban đầu.",
        "advice": "Điều kiện bắt buộc nếu muốn đưa trái cây tươi và rau củ Việt Nam lên kệ các chuỗi siêu thị hàng đầu thế giới."
    },
    "#FSC_100%": {
        "name": "Chứng chỉ Quản lý Rừng Bền vững Quốc tế FSC 100%",
        "category": "Chứng Nhận Lâm Sản Bền Vững",
        "desc": "Chứng nhận gỗ và các sản phẩm từ gỗ (viên nén, ván ép, đồ gỗ nội thất) có nguồn gốc 100% từ rừng trồng được quy hoạch và quản lý bền vững, có trách nhiệm xã hội.",
        "advice": "Yếu tố sống còn để vượt qua rào cản Đạo luật Chống phá rừng Châu Âu (EUDR) và Đạo luật Lacey của Hoa Kỳ."
    },

    # 3. Incoterms (Điều kiện giao hàng)
    "#Inco_FOB": {
        "name": "Giao hàng lên tàu (Free On Board - FOB)",
        "category": "Điều Kiện Incoterms",
        "desc": "Người bán hoàn thành nghĩa vụ khi hàng đã được xếp lên tàu tại cảng bốc quy định. Chi phí cước tàu biển quốc tế và bảo hiểm hàng hải do Người mua chịu trách nhiệm chi trả.",
        "advice": "Thuận tiện cho người bán Việt Nam vì không phải chịu biến động cước tàu biển quốc tế (Ocean Freight Volatility)."
    },
    "#Inco_FOB_CatLai": {
        "name": "FOB Cảng Tân Cảng Cát Lái, TP. Hồ Chí Minh",
        "category": "Điều Kiện Incoterms",
        "desc": "Hàng hóa được làm thủ tục thông quan xuất khẩu và xếp lên tàu tại Cảng Tân Cảng Cát Lái - trung tâm xuất khẩu hàng container lớn nhất miền Nam Việt Nam.",
        "advice": "Lưu ý hạn chế tắc nghẽn giao thông quanh nút giao An Phú trong mùa cao điểm xuất khẩu cuối năm."
    },
    "#Inco_FOB_CaiMep": {
        "name": "FOB Cụm Cảng Nước Sâu Cái Mép - Thị Vải",
        "category": "Điều Kiện Incoterms",
        "desc": "Xếp hàng lên các tàu mẹ (Mother Vessels) siêu trọng tải đi thẳng sang Bờ Tây nước Mỹ và Châu Âu, không phải trung chuyển qua Singapore hay Hong Kong.",
        "advice": "Rút ngắn thời gian vận chuyển (transit time) từ 5 đến 7 ngày so với đi tàu gom feeders từ cảng sông."
    },
    "#Inco_CIF": {
        "name": "Tiền hàng, Bảo hiểm & Cước phí (CIF)",
        "category": "Điều Kiện Incoterms",
        "desc": "Người bán chịu trách nhiệm thuê tàu, trả cước vận chuyển đường biển và mua bảo hiểm hàng hải cho lô hàng đến tận cảng dỡ hàng quy định của người mua.",
        "advice": "Người bán cần chọn đơn vị bảo hiểm uy tín với điều kiện bảo hiểm loại A (All Risks) theo Viện Bảo hiểm London (ICC)."
    },
    "#Inco_CIF_Hamburg": {
        "name": "CIF Cảng Hamburg, CHLB Đức",
        "category": "Điều Kiện Incoterms",
        "desc": "Giao hàng cập cảng biển quốc tế Hamburg - cửa ngõ logistics chiến lược của nước Đức và toàn khu vực Trung Âu.",
        "advice": "Theo dõi lịch thông quan kiểm dịch thực vật tại trạm kiểm soát biên giới cảng Hamburg."
    },
    "#Inco_CIF_Rotterdam": {
        "name": "CIF Cảng Rotterdam, Hà Lan",
        "category": "Điều Kiện Incoterms",
        "desc": "Giao hàng đến Cảng Rotterdam - cảng biển lớn nhất Châu Âu, đầu mối trung chuyển và phân phối hàng hóa đi khắp các nước EU.",
        "advice": "Thời gian dỡ hàng và quay vòng container tại Rotterdam rất nhanh, tối ưu chi phí lưu kho bãi."
    },
    "#Inco_CIF_StPetersburg": {
        "name": "CIF Cảng St. Petersburg, Liên Bang Nga",
        "category": "Điều Kiện Incoterms",
        "desc": "Giao hàng đến cảng biển lớn nhất của Nga tại Vịnh Phần Lan, phục vụ cung ứng hàng hóa cho thị trường Moscow và toàn bộ Tây Bắc nước Nga.",
        "advice": "Cần điều phối hãng tàu có tuyến vận tải trực tiếp sang Nga và cơ chế thanh toán không bị cản trở bởi lệnh trừng phạt phương Tây."
    },
    "#Inco_CFR": {
        "name": "Tiền hàng & Cước phí đường biển (CFR - Cost and Freight)",
        "category": "Điều Kiện Incoterms",
        "desc": "Người bán trả cước tàu đường biển đến cảng đích; tuy nhiên người mua tự chịu chi phí và thủ tục mua bảo hiểm hàng hải cho lô hàng của mình.",
        "advice": "Người bán phải lập tức gửi Thông Báo Gửi Hàng (Shipping Advice) kèm bản scan vận đơn ngay khi tàu rời cảng để người mua kịp mua bảo hiểm."
    },

    # 4. Payment terms (Thanh toán quốc tế)
    "#LC_AtSight": {
        "name": "Tín dụng thư không hủy ngang trả ngay (L/C At Sight)",
        "category": "Thanh Toán Quốc Tế",
        "desc": "Phương thức thanh toán an toàn nhất trong ngoại thương. Ngân hàng mở L/C cam kết thanh toán 100% tiền hàng ngay khi người bán xuất trình bộ chứng từ xuất khẩu hoàn hảo hợp lệ.",
        "advice": "Người bán phải kiểm tra kỹ từng câu chữ trong thông báo mở L/C để phát hiện và tu chỉnh sớm các điều khoản bẫy (soft clauses)."
    },
    "#Usance_LC": {
        "name": "Tín dụng thư trả chậm (Usance L/C 30/60/90 Ngày)",
        "category": "Thanh Toán Quốc Tế",
        "desc": "Người mua được hoãn thanh toán trong một thời hạn nhất định (30, 60 hoặc 90 ngày) sau ngày phát hành vận đơn B/L hoặc ngày chấp nhận hối phiếu.",
        "advice": "Người bán nên tính toán chi phí tài trợ thương mại và lãi suất vay vốn vào giá chào hàng để bù đắp chi phí thời gian chờ tiền về."
    },
    "#TT_Deposit_30_70": {
        "name": "Chuyển tiền điện T/T (Cọc 30% - Thanh toán 70% khi có B/L scan)",
        "category": "Thanh Toán Quốc Tế",
        "desc": "Người mua chuyển cọc 30% giá trị hợp đồng để nhà sản xuất mua nguyên liệu; 70% còn lại thanh toán ngay khi người bán gửi bản scan bộ chứng từ và vận đơn B/L gốc đường biển.",
        "advice": "Chỉ giải phóng bản gốc vận đơn Surrendered / Telex Release khi tiền 70% đã báo có (Credited) vào tài khoản ngân hàng."
    },
    "#CAD_Payment": {
        "name": "Giao chứng từ trả tiền (Cash Against Documents - CAD)",
        "category": "Thanh Toán Quốc Tế",
        "desc": "Người bán chuyển bộ chứng từ qua ngân hàng chỉ định tại nước người mua. Người mua phải nộp đủ 100% tiền vào ngân hàng thì mới được nhận chứng từ để ra cảng nhận hàng.",
        "advice": "Chi phí dịch vụ rẻ hơn L/C nhưng vẫn bảo đảm quyền kiểm soát hàng hóa thông qua quyền giữ bộ chứng từ gốc của ngân hàng."
    }
}

def get_trade_tag_info(tag: str) -> dict:
    if not tag:
        return {}
    clean_tag = tag.strip()
    if clean_tag in TRADE_TAG_CATALOG:
        data = dict(TRADE_TAG_CATALOG[clean_tag])
        data["tag"] = clean_tag
        return data

    # Phân tích theo tiền tố quy chuẩn
    if clean_tag.startswith("#HS_"):
        code = clean_tag.replace("#HS_", "")
        return {
            "tag": clean_tag,
            "name": f"Mã Ngành Hàng HS {code}",
            "category": "Mã Ngành Hàng WCO",
            "desc": f"Mã phân loại hàng hóa xuất nhập khẩu 4 số theo chuẩn của Tổ chức Hải quan Thế giới (WCO). Xác định danh mục thuế quan và thủ tục hải quan áp dụng.",
            "advice": "Đối soát tính chính xác của 6 số hoặc 8 số trên tờ khai hải quan thực tế giữa nước xuất khẩu và nước nhập khẩu."
        }

    if clean_tag.startswith("#Inco_"):
        term = clean_tag.replace("#Inco_", "").replace("_", " ")
        return {
            "tag": clean_tag,
            "name": f"Điều Kiện Giao Nhận Incoterms {term}",
            "category": "Điều Kiện Incoterms",
            "desc": "Quy tắc thương mại quốc tế của Phòng Thương mại Quốc tế (ICC) xác định rõ điểm phân chia chi phí, rủi ro và trách nhiệm xếp dỡ vận tải biển.",
            "advice": "Kiểm tra địa điểm giao nhận cụ thể và người chịu trách nhiệm mua bảo hiểm hàng hải cho lô hàng."
        }

    if clean_tag.startswith("#LC_") or clean_tag.startswith("#TT_") or clean_tag.startswith("#CAD_"):
        return {
            "tag": clean_tag,
            "name": "Phương Thức Thanh Toán Quốc Tế",
            "category": "Thanh Toán Quốc Tế",
            "desc": "Điều kiện và phương thức thanh toán tiền hàng qua hệ thống ngân hàng thương mại quốc tế (SWIFT).",
            "advice": "Đảm bảo chứng từ hoàn hảo theo quy tắc thực hành thống nhất tín dụng chứng từ UCP 600."
        }

    return {
        "tag": clean_tag,
        "name": clean_tag.replace("#", "").replace("_", " "),
        "category": "Quy Chuẩn Ngoại Thương",
        "desc": "Tiêu chuẩn kỹ thuật, chứng chỉ chất lượng hoặc điều kiện thương mại thỏa thuận giữa hai bên trong giao dịch xuất nhập khẩu.",
        "advice": "Làm rõ chi tiết tiêu chuẩn kỹ thuật cụ thể trong phụ lục hợp đồng mua bán ngoại thương."
    }
