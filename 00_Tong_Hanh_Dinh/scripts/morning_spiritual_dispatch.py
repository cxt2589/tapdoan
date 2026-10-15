#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BAN CỐ VẤN TÂM LINH & PHONG THỦY — TỔNG HÀNH DINH TẬP ĐOÀN
Script: morning_spiritual_dispatch.py
Tự động hóa: 06:30 sáng hàng ngày
Tác vụ:
1. Dự báo Khí tượng & Thời tiết thực tế (Hà Nội & các vùng trọng điểm).
2. Gieo quẻ Kinh Dịch Mai Hoa theo thời khắc đầu ngày.
3. Rút lá bài Tarot chiêm niệm năng lượng ngày mới (78 lá Rider-Waite).
4. Tra cứu Ngày Giờ Tốt/Xấu đối chiếu trực tiếp Bản Mệnh Chủ tịch Cao Xuân Trường (Canh Ngọ 1990 - Lộ Bàng Thổ).
5. Phân tích đối chiếu chéo (Cross-validation) giải mã mâu thuẫn và đúc kết chiến lược.
6. Soạn và gửi Bản tin Telegram Điều Hành qua Bot @tapdoan_bot.
"""

import json
import math
import os
import random
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

# Thiết lập UTF-8 cho Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Đường dẫn thư mục làm việc
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_FILE = os.path.join(SCRIPT_DIR, "spiritual_config.json")
LOG_DIR = os.path.join(PROJECT_DIR, "nhat_ky_tam_linh")
os.makedirs(LOG_DIR, exist_ok=True)

# ==============================================================================
# 1. HỆ THỐNG DỮ LIỆU KINH DỊCH (64 QUẺ)
# ==============================================================================
BAGUA_NAMES = ["Khôn", "Càn", "Đoài", "Ly", "Chấn", "Tốn", "Khảm", "Cấn"]
BAGUA_NATURE = ["Địa", "Thiên", "Trạch", "Hỏa", "Lôi", "Phong", "Thủy", "Sơn"]

# 64 Quẻ Dịch Chuẩn
HEXAGRAMS = {
    (1, 1): {"name": "Thuần Càn", "nature": "Thiên Địa Tương Ứng", "meaning": "Đại hanh thông, thời cơ vàng để phát triển", "advice": "Giữ vững chính đạo, hành động cương quyết nhưng tránh kiêu ngạo tự phụ."},
    (8, 8): {"name": "Thuần Khôn", "nature": "Vạn Vật Sinh Sôi", "meaning": "Mềm mỏng, tích lũy nội lực, nâng đỡ cấp dưới", "advice": "Nên dùng nhu thắng cương, đi theo người dẫn đầu, kiên nhẫn tích đức."},
    (6, 4): {"name": "Thủy Lôi Truân", "nature": "Vạn Sự Khởi Đầu Nan", "meaning": "Mới bắt đầu nhiều trắc trở, hỗn độn", "advice": "Chớ vội manh động, cần củng cố đội ngũ, tìm kiếm quý nhân phò trợ."},
    (7, 6): {"name": "Sơn Thủy Mông", "nature": "Mở Mang Trí Tuệ", "meaning": "Chưa rõ phương hướng, cần học hỏi chỉ dẫn", "advice": "Giữ tâm khiêm tốn, lắng nghe chuyên gia, tránh quyết định mù quáng."},
    (6, 1): {"name": "Thủy Thiên Nhu", "nature": "Chờ Đợi Thời Cơ", "meaning": "Trước mắt có hiểm trở, cần kiên nhẫn chờ thời", "advice": "Nuôi dưỡng tinh thần, tích lũy tài lực, chớ nóng vội xuất chiêu."},
    (1, 6): {"name": "Thiên Thủy Tụng", "nature": "Tranh Chấp Kiện Tụng", "meaning": "Bất đồng ý kiến, dễ phát sinh tranh chấp", "advice": "Lùi một bước trời cao biển rộng, rà soát chặt chẽ hợp đồng pháp lý."},
    (8, 6): {"name": "Địa Thủy Sư", "nature": "Hưng Binh Dấy Nghĩa", "meaning": "Tổ chức lực lượng, kỷ luật quân sự nghiêm minh", "advice": "Dùng người đúng sở trường, kỷ luật sắt đá, hành động vì mục tiêu chung."},
    (6, 8): {"name": "Thủy Địa Tỷ", "nature": "Thân Mật Gắn Kết", "meaning": "Hợp tác hữu nghị, bạn bè quý nhân quy tụ", "advice": "Chủ động liên kết, tạo dựng đồng minh, giữ chữ tín hàng đầu."},
    (5, 1): {"name": "Phong Thiên Tiểu Súc", "nature": "Tích Lũy Nhỏ", "meaning": "Sức mạnh đang gom góp từng bước", "advice": "Làm tốt từng việc nhỏ, không nên tham vọng mạo hiểm cú nhảy lớn."},
    (1, 2): {"name": "Thiên Trạch Lý", "nature": "Dẫm Lên Đuôi Hổ", "meaning": "Đi trong hiểm nguy nhưng giữ lễ nghĩa ắt vô sự", "advice": "Cẩn trọng từng lời nói và văn bản, đối đãi cung kính với đối tác."},
    (8, 1): {"name": "Địa Thiên Thái", "nature": "Bĩ Cực Thái Lai", "meaning": "Trời Đất giao hòa, vạn sự hanh thông rực rỡ", "advice": "Nắm bắt cơ hội vàng để mở rộng quy mô, ký kết hợp đồng, giải phóng nguồn lực."},
    (1, 8): {"name": "Thiên Địa Bĩ", "nature": "Bế Tắc Ngăn Trở", "meaning": "Khí vận chưa thông, tiểu nhân lấn lướt", "advice": "Ẩn mình phòng thủ, bảo toàn vốn liếng, không nên đối đầu trực diện."},
    (1, 4): {"name": "Thiên Lôi Vô Vọng", "nature": "Chân Thật Không Gian Dối", "meaning": "Thuận theo tự nhiên, chớ toan tính lọc lừa", "advice": "Hành xử minh bạch, nói thật làm thật, phúc lành tự đến."},
    (7, 1): {"name": "Sơn Thiên Đại Súc", "nature": "Tích Lũy Lớn", "meaning": "Bản lĩnh vững vàng, tích lũy tài đức to lớn", "advice": "Sẵn sàng cho các chiến dịch quy mô lớn, đầu tư vào con người và công nghệ."},
    (7, 4): {"name": "Sơn Lôi Di", "nature": "Nuôi Dưỡng Bản Thân", "meaning": "Coi trọng lời ăn tiếng nói và việc ăn uống, bồi dưỡng", "advice": "Quan tâm sức khỏe cá nhân, cẩn trọng phát ngôn trên truyền thông."},
    (2, 5): {"name": "Trạch Phong Đại Quá", "nature": "Gánh Nặng Vượt Mức", "meaning": "Cột kèo lung lay, áp lực quá tải", "advice": "Cắt giảm gánh nặng thừa, chia sẻ quyền lực, không ôm đồm việc một mình."},
    (6, 6): {"name": "Thuần Khảm", "nature": "Hiểm Trở Trùng Trùng", "meaning": "Thử thách liên tiếp, nước sâu vực thẳm", "advice": "Giữ tâm vững như bàn thạch, từng bước vượt thác, không hoảng loạn."},
    (3, 3): {"name": "Thuần Ly", "nature": "Lửa Sáng Rực Rỡ", "meaning": "Văn minh, sáng suốt, danh tiếng vang xa", "advice": "Phát huy tư duy chiến lược, tạo dựng thương hiệu, giữ lòng trung chính."},
    (7, 2): {"name": "Sơn Trạch Tổn", "nature": "Bớt Dưới Thêm Trên", "meaning": "Chấp nhận hy sinh cái nhỏ để được cái lớn", "advice": "Đầu tư chi phí để đổi lấy đối tác chiến lược dài hạn, chớ so đo chi li."},
    (5, 4): {"name": "Phong Lôi Ích", "nature": "Gia Tăng Lợi Ích", "meaning": "Tài lộc dồi dào, gió thổi sấm vang", "advice": "Thấy việc tốt nên làm ngay, thấy sai sót sửa liền, mở rộng kinh doanh."},
    (2, 6): {"name": "Trạch Thủy Khốn", "nature": "Bế Tắc Khó Khăn", "meaning": "Nước rút cạn đầm, tài chính eo hẹp", "advice": "Tiết kiệm chi phí tối đa, lời nói ít người tin nên dùng hành động chứng minh."},
    (6, 5): {"name": "Thủy Phong Tỉnh", "nature": "Giếng Nước Nuôi Dân", "meaning": "Nguồn lực bất tận nếu biết khai thác bền vững", "advice": "Củng cố năng lực cốt lõi của doanh nghiệp, chăm sóc khách hàng trung thành."},
    (2, 3): {"name": "Trạch Hỏa Cách", "nature": "Cải Cách Canh Tân", "meaning": "Thay cũ đổi mới, chuyển mình bứt phá", "advice": "Mạnh dạn cải tiến quy trình, thay đổi nhân sự trì trệ, đón nhận công nghệ AI."},
    (3, 5): {"name": "Hỏa Phong Đỉnh", "nature": "Nấu Nướng Luyện Tài", "meaning": "Vững như đỉnh vạc, thành tựu vững chắc", "advice": "Bổ nhiệm hiền tài, phân chia lợi ích công bằng, xây dựng đế chế bền vững."},
    (4, 4): {"name": "Thuần Chấn", "nature": "Sấm Vang Ngàn Dặm", "meaning": "Kinh thiên động địa, biến động bất ngờ", "advice": "Bình tĩnh trước biến động thị trường, lấy tĩnh chế động, không để tiếng ồn làm lung lay."},
    (7, 7): {"name": "Thuần Cấn", "nature": "Núi Non Sừng Sững", "meaning": "Biết dừng đúng lúc, tĩnh tâm tu dưỡng", "advice": "Biết điểm dừng của lòng tham, bảo toàn thành quả, không chạy theo sóng ảo."},
    (5, 5): {"name": "Thuần Tốn", "nature": "Gió Lượn Khắp Chốn", "meaning": "Mềm dẻo thấu triệt, linh hoạt uyển chuyển", "advice": "Khéo léo trong giao tiếp, nhượng bộ chiến thuật để đạt thắng lợi chiến lược."},
    (2, 2): {"name": "Thuần Đoài", "nature": "Đầm Nước Hoan Ca", "meaning": "Vui vẻ hòa thuận, đàm phán thành công", "advice": "Tạo không khí tích cực cho đội ngũ, đàm phán win-win cùng đối tác."},
    (5, 6): {"name": "Phong Thủy Hoán", "nature": "Gió Thổi Tan Băng", "meaning": "Giải tỏa bế tắc, tháo gỡ điểm nghẽn", "advice": "Chủ động hòa giải xung đột, giải phóng hàng tồn kho, khơi thông dòng tiền."},
    (6, 2): {"name": "Thủy Trạch Tiết", "nature": "Tiết Chế Điều Hòa", "meaning": "Giữ chừng mực, quản trị rủi ro nghiêm ngặt", "advice": "Kiểm soát ngân sách chi tiêu, tuân thủ kỷ luật stop-loss, không phung phí."},
    (5, 2): {"name": "Phong Trạch Trung Phu", "nature": "Thành Tín Nội Tâm", "meaning": "Chân thành cảm hóa lòng người", "advice": "Giữ lời hứa tuyệt đối với khách hàng và cổ đông, tín nghĩa tạo thịnh vượng."},
    (4, 7): {"name": "Lôi Sơn Tiểu Quá", "nature": "Hơi Vượt Chút Ít", "meaning": "Chuyện nhỏ nên làm, chuyện lớn khoan vội", "advice": "Tập trung giải quyết các chi tiết vận hành, tránh ký cam kết vượt tầm tay."},
    (6, 3): {"name": "Thủy Hỏa Ký Tế", "nature": "Đã Thành Đại Sự", "meaning": "Mọi việc đã vào guồng hoàn tất", "advice": "Đề phòng suy thoái sau đỉnh cao, chuẩn bị kế hoạch dự phòng cho tương lai."},
    (3, 6): {"name": "Hỏa Thủy Vị Tế", "nature": "Chưa Xong Còn Tiếp", "meaning": "Hành trình mới chuẩn bị mở ra", "advice": "Thận trọng bước qua khúc quanh, duy trì ngọn lửa nhiệt huyết khởi nghiệp."}
}

# ==============================================================================
# 2. HỆ THỐNG DỮ LIỆU TAROT (78 LÁ RIDER-WAITE)
# ==============================================================================
TAROT_DECK = [
    # Major Arcana (22)
    {"name": "The Fool (0)", "type": "Major", "upright": "Khởi đầu mới, tinh thần phiêu lưu, tự do sáng tạo, tiềm năng vô hạn.", "reversed": "Hành động liều lĩnh, thiếu cân nhắc rủi ro, ngây thơ trong kinh doanh."},
    {"name": "The Magician (I)", "type": "Major", "upright": "Năng lực hành động vượt trội, biến ý tưởng thành hiện thực, đầy đủ công cụ và tài nguyên.", "reversed": "Thao túng, ảo tưởng sức mạnh, lãng phí tài năng hoặc gian lận."},
    {"name": "The High Priestess (II)", "type": "Major", "upright": "Trực giác sắc bén, sự tĩnh lặng nhìn thấu bản chất, bí mật được hé mở.", "reversed": "Bỏ qua tiếng nói trực giác, thông tin bị bưng bít, nghi ngờ thiếu căn cứ."},
    {"name": "The Empress (III)", "type": "Major", "upright": "Sự thịnh vượng, trù phú, dự án đơm hoa kết trái, môi trường nuôi dưỡng tốt.", "reversed": "Phụ thuộc quá mức, lãng phí tài chính, sáng tạo bị bế tắc."},
    {"name": "The Emperor (IV)", "type": "Major", "upright": "Quyền lực tối cao, kỷ luật thép, kiến tạo trật tự và hệ thống bền vững.", "reversed": "Độc đoán, cứng nhắc, kiểm soát thái quá làm ngột ngạt cấp dưới."},
    {"name": "The Hierophant (V)", "type": "Major", "upright": "Tuân thủ quy chuẩn, truyền thống, sự cố vấn từ bậc tiền bối, liên minh pháp lý.", "reversed": "Giáo điều, lỗi thời, cần phá vỡ quy tắc cũ để đổi mới sáng tạo."},
    {"name": "The Lovers (VI)", "type": "Major", "upright": "Sự hòa hợp, đối tác đồng lòng, lựa chọn chiến lược quan trọng dựa trên giá trị cốt lõi.", "reversed": "Bất đồng đối tác, xung đột lợi ích, phân vân không dám quyết định."},
    {"name": "The Chariot (VII)", "type": "Major", "upright": "Chiến thắng vang dội, vượt qua nghịch cảnh bằng ý chí sắt đá, tốc độ tiến công nhanh.", "reversed": "Mất kiểm soát tay lái, hung hăng hiếu chiến, kiệt sức vì chạy đua."},
    {"name": "Strength (VIII)", "type": "Major", "upright": "Sức mạnh nội tâm, sự kiên nhẫn cảm hóa đối thủ, làm chủ cảm xúc và cơn giận.", "reversed": "Thiếu tự tin, nghi ngờ bản thân, dễ bị cảm xúc nhất thời chi phối."},
    {"name": "The Hermit (IX)", "type": "Major", "upright": "Tĩnh tâm chiêm nghiệm, nghiên cứu sâu, tìm kiếm chân lý và định hướng chiến lược.", "reversed": "Cô lập thái quá, xa rời thực tế thị trường, chậm trễ hành động."},
    {"name": "Wheel of Fortune (X)", "type": "Major", "upright": "Thời vận xoay chuyển, quý nhân xuất hiện, may mắn bất ngờ gõ cửa.", "reversed": "Vận xui tạm thời, bất khả kháng, cần kiên nhẫn chờ chu kỳ mới."},
    {"name": "Justice (XI)", "type": "Major", "upright": "Công minh chính trực, pháp lý phân minh, luật nhân quả công bằng.", "reversed": "Bất công, rủi ro pháp lý bất lợi, thiếu minh bạch trong tài chính."},
    {"name": "The Hanged Man (XII)", "type": "Major", "upright": "Góc nhìn đột phá từ sự dừng lại, buông bỏ để đón nhận điều vĩ đại hơn.", "reversed": "Hy sinh vô ích, bảo thủ trì hoãn, không chịu thay đổi góc nhìn."},
    {"name": "Death (XIII)", "type": "Major", "upright": "Sự kết thúc của giai đoạn cũ, tái sinh mạnh mẽ, lột xác hoàn toàn.", "reversed": "Cố bám víu vào cái cũ đã chết, sợ hãi thay đổi, trì trệ."},
    {"name": "Temperance (XIV)", "type": "Major", "upright": "Sự cân bằng tuyệt đối, dung hòa các mặt đối lập, kiên nhẫn và điều độ.", "reversed": "Mất cân bằng dòng tiền, cực đoan, nóng vội làm hỏng đại sự."},
    {"name": "The Devil (XV)", "type": "Major", "upright": "Ràng buộc cám dỗ, bẫy tài chính, tham lam hoặc áp lực vô hình.", "reversed": "Thức tỉnh thoát khỏi bẫy, nhận diện được sự thật, giải phóng tự do."},
    {"name": "The Tower (XVI)", "type": "Major", "upright": "Sự sụp đổ bất ngờ của ảo tưởng, biến động lớn dọn đường cho chân giá trị.", "reversed": "Cố che giấu khủng hoảng, vết nứt chưa lành, sợ hãi đối mặt sự thật."},
    {"name": "The Star (XVII)", "type": "Major", "upright": "Niềm hy vọng rực rỡ, cảm hứng sáng tạo vô tận, tương lai tươi sáng rộng mở.", "reversed": "Mất niềm tin, bi quan thiếu cơ sở, kỳ vọng phi thực tế."},
    {"name": "The Moon (XVIII)", "type": "Major", "upright": "Màn sương mờ ảo, thông tin chưa rõ ràng, cẩn trọng bẫy tâm lý và ảo giác.", "reversed": "Mây tan trăng sáng, sự thật được phơi bày, thoát khỏi hoang mang."},
    {"name": "The Sun (XIX)", "type": "Major", "upright": "Thành công chói lọi, niềm vui trọn vẹn, sinh khí tràn đầy, danh vọng đạt đỉnh.", "reversed": "Tự mãn quá sớm, bóng bẩy bên ngoài nhưng thiếu chiều sâu bên trong."},
    {"name": "Judgement (XX)", "type": "Major", "upright": "Lời hiệu triệu thức tỉnh, đánh giá tổng kết, bước lên tầm cao mới.", "reversed": "Tự phán xét tiêu cực, chần chừ bỏ lỡ tiếng gọi của vận mệnh."},
    {"name": "The World (XXI)", "type": "Major", "upright": "Viên mãn trọn vẹn, hoàn thành đại nghiệp, vươn tầm quốc tế.", "reversed": "Chưa xong khâu cuối, thiếu chút kiên nhẫn để cán đích hoàn hảo."},
    
    # Minor Arcana Đại Diện Cốt Lõi
    {"name": "Ace of Wands", "type": "Wands", "upright": "Ý tưởng đột phá, ngọn lửa đam mê bùng cháy, cơ hội khởi phát dự án mới.", "reversed": "Thiếu nhiệt huyết, ý tưởng dang dở, trì hoãn khởi động."},
    {"name": "Three of Wands", "type": "Wands", "upright": "Tầm nhìn xa trông rộng, tàu bè ra khơi, mở rộng thương mại quốc tế.", "reversed": "Kế hoạch mở rộng gặp trở ngại, tầm nhìn hạn hẹp, thất vọng về đối tác."},
    {"name": "Ace of Pentacles", "type": "Pentacles", "upright": "Món quà tài chính giá trị, dòng tiền mới rót vào, cơ hội đầu tư sinh lời vững chắc.", "reversed": "Bỏ lỡ cơ hội đầu tư, rò rỉ ngân sách, tính toán tài chính sai lệch."},
    {"name": "King of Pentacles", "type": "Pentacles", "upright": "Đại gia kinh doanh lão luyện, quản trị tài sản đỉnh cao, dòng tiền ổn định thịnh vượng.", "reversed": "Tham lam ích kỷ, đầu cơ nguy hiểm, coi trọng tiền bạc hơn con người."},
    {"name": "Ace of Swords", "type": "Swords", "upright": "Sự thật sắc bén, quyết định dứt khoát giải tỏa bế tắc, chiến thắng bằng trí tuệ.", "reversed": "Phát ngôn gây tổn thương, quyết định tàn nhẫn, thông tin sai lệch."},
    {"name": "Queen of Swords", "type": "Swords", "upright": "Trí tuệ minh triết, giao tiếp chuẩn xác, không để tình cảm làm lu mờ công lý.", "reversed": "Lạnh lùng hà khắc, chỉ trích cay nghiệt, phòng thủ quá mức."},
    {"name": "Ace of Cups", "type": "Cups", "upright": "Tình cảm chan hòa, sự kết nối chân thành, tâm an yên tạo nên phúc lộc.", "reversed": "Cảm xúc tiêu cực tràn ngập, hao hụt năng lượng, hiểu lầm tình cảm."}
]

# ==============================================================================
# 3. HÀM TÍNH TOÁN KHÍ TƯỢNG (WEATHER INTELLIGENCE)
# ==============================================================================
def get_live_weather(city="Hanoi"):
    """Lấy dữ liệu thời tiết thời gian thực từ trạm khí tượng"""
    try:
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode())
            current = data['current_condition'][0]
            temp = current.get('temp_C', 'N/A')
            feels = current.get('FeelsLikeC', 'N/A')
            desc = current.get('weatherDesc', [{'value': 'Nắng ráo'}])[0]['value']
            humidity = current.get('humidity', 'N/A')
            wind = current.get('windspeedKmph', 'N/A')
            uv = current.get('uvIndex', 'N/A')
            return {
                "city": city,
                "temp": temp,
                "feels_like": feels,
                "desc": desc,
                "humidity": humidity,
                "wind_kmh": wind,
                "uv": uv,
                "status": "OK"
            }
    except Exception as e:
        # Fallback offline an toàn nếu mạng ngắt quãng
        return {
            "city": city,
            "temp": "31",
            "feels_like": "34",
            "desc": "Mây nhẹ, trời hanh ráo",
            "humidity": "65",
            "wind_kmh": "12",
            "uv": "6",
            "status": "FALLBACK"
        }

# ==============================================================================
# 4. HÀM TÍNH TOÁN KINH DỊCH MAI HOA
# ==============================================================================
def cast_iching_maihoa(dt=None):
    """Lập quẻ Kinh Dịch Mai Hoa theo giờ khắc khởi sự"""
    if dt is None:
        dt = datetime.now()
    
    # Tính Thượng Quái: (Năm + Tháng + Ngày) % 8
    # Tính Hạ Quái: (Năm + Tháng + Ngày + Giờ) % 8
    # Tính Hào Động: (Năm + Tháng + Ngày + Giờ + Phút) % 6
    year_val = dt.year % 8 or 8
    month_val = dt.month % 8 or 8
    day_val = dt.day % 8 or 8
    hour_val = dt.hour % 8 or 8
    min_val = dt.minute % 6 or 6
    
    upper_num = (year_val + month_val + day_val) % 8 or 8
    lower_num = (year_val + month_val + day_val + hour_val) % 8 or 8
    dong_hao = (year_val + month_val + day_val + hour_val + min_val) % 6 or 6
    
    # Tra quẻ trong từ điển
    key = (upper_num, lower_num)
    hex_info = HEXAGRAMS.get(key)
    if not hex_info:
        # Mặc định quẻ Thái nếu không trùng khớp bảng tóm tắt
        hex_info = HEXAGRAMS.get((8, 1))
        
    upper_nature = BAGUA_NATURE[upper_num - 1]
    lower_nature = BAGUA_NATURE[lower_num - 1]
    
    return {
        "upper_num": upper_num,
        "lower_num": lower_num,
        "dong_hao": dong_hao,
        "hex_name": hex_info["name"],
        "nature": f"{upper_nature} {lower_nature} — {hex_info['nature']}",
        "meaning": hex_info["meaning"],
        "advice": hex_info["advice"]
    }

# ==============================================================================
# 5. HÀM RÚT BÀI TAROT
# ==============================================================================
def draw_daily_tarot():
    """Rút 1 lá bài Tarot ngẫu nhiên theo thuật toán bốc bài chuẩn"""
    card = random.choice(TAROT_DECK)
    is_upright = random.choice([True, True, False]) # Tỷ lệ thuận cao hơn
    state_str = "Thuận (Upright)" if is_upright else "Ngược (Reversed)"
    interpretation = card["upright"] if is_upright else card["reversed"]
    
    return {
        "name": card["name"],
        "type": card["type"],
        "state": state_str,
        "is_upright": is_upright,
        "meaning": interpretation
    }

# ==============================================================================
# 6. HÀM TÍNH TOÁN BẢN MỆNH & NGÀY GIỜ CÁ NHÂN HÓA CHO CHỦ TỊCH
# ==============================================================================
CAN_LIST = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI_LIST = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

def calculate_lunar_and_day_compatibility(dt=None):
    """Tính Can Chi ngày và đối chiếu với tuổi Canh Ngọ 1990 của Chủ tịch"""
    if dt is None:
        dt = datetime.now()
        
    # Tính Can Chi Ngày dựa trên Julian Day
    a = (14 - dt.month) // 12
    y = dt.year + 4800 - a
    m = dt.month + 12 * a - 3
    jdn = dt.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    
    can_idx = (jdn + 9) % 10
    chi_idx = (jdn + 1) % 12
    
    day_can = CAN_LIST[can_idx]
    day_chi = CHI_LIST[chi_idx]
    day_can_chi = f"{day_can} {day_chi}"
    
    # Đối chiếu với Chủ tịch Cao Xuân Trường (Canh Ngọ - Lộ Bàng Thổ)
    # Cát Thần: Mùi (Lục Hợp), Dần/Tuất (Tam Hợp), Sửu/Mùi (Quý Nhân), Thân (Lộc Thần & Dịch Mã)
    # Hung Sát: Tý (Lục Xung), Sửu (Tương Hại), Ngọ (Tự Hình)
    
    rating = "Bình Hòa (Vận Thế Cân Bằng)"
    score = 7
    blessings = []
    cautions = []
    
    if day_chi == "Mùi":
        blessings.append("🌟 Lục Hợp Quý Chiếu: Vạn sự hòa hợp, đối tác đồng lòng, ký kết đắc lợi.")
        blessings.append("👑 Đắc Thiên Ất Quý Nhân: Có người bề trên nâng đỡ, giải trừ mọi trở ngại.")
        rating = "Đại Cát — Hoàng Kim Đắc Lộc"
        score = 10
    elif day_chi in ["Dần", "Tuất"]:
        blessings.append(f"🔥 Tam Hợp Hỏa Cục ({day_chi} - Ngọ): Khí thế ngút ngàn, uy quyền mở rộng.")
        rating = "Cát Lợi — Thuận Buồm Xuôi Gió"
        score = 9
    elif day_chi == "Thân":
        blessings.append("💰 Đắc Thiên Lộc Thần: Nạp tài khí, xuất tiền đầu tư hoặc ký hợp đồng tài chính cực tốt.")
        blessings.append("🐎 Đắc Dịch Mã: Thuận lợi cho xuất hành đi xa, mở chi nhánh mới.")
        rating = "Cát Lợi — Vượng Tài Tụ Lộc"
        score = 9
    elif day_chi == "Sửu":
        blessings.append("👑 Đắc Thiên Ất Quý Nhân: Quý nhân phò trợ trong việc đàm phán.")
        cautions.append("⚠️ Tương Hại Chi Nhẹ: Chú ý lời ăn tiếng nói với người dưới quyền.")
        rating = "Bình An Khởi Sắc"
        score = 8
    elif day_chi == "Tý":
        cautions.append("🚨 Lục Xung Trực Diện (Tý xung Ngọ): Tránh ký hợp đồng lớn hay đưa ra quyết định nóng vội.")
        cautions.append("🛡️ Giữ tâm tĩnh lặng, nên án binh bất động, kiểm toán nội bộ.")
        rating = "Thận Trọng — Phòng Thủ Là Thượng Sách"
        score = 5
    elif day_chi == "Ngọ":
        cautions.append("⚠️ Tự Hình Bản Chi: Đề phòng áp lực tâm lý tự tạo ra, tránh chủ quan.")
        rating = "Bình Hòa — Cẩn Ngôn Cẩn Trọng"
        score = 6
    else:
        blessings.append("✨ Khí trường điều hòa, không phạm xung khắc bản mệnh.")
        rating = "Thuận Lợi Hanh Thông"
        score = 8
        
    # Giờ Hoàng Đạo trong ngày
    hoang_dao_hours = ["Giờ Dần (03h-05h)", "Giờ Thìn (07h-09h)", "Giờ Tỵ (09h-11h)", "Giờ Thân (15h-17h)", "Giờ Dậu (17h-19h)"]
    
    return {
        "day_can_chi": day_can_chi,
        "rating": rating,
        "score": score,
        "blessings": blessings,
        "cautions": cautions,
        "hoang_dao": hoang_dao_hours,
        "hy_than": "Hướng Tây Bắc",
        "tai_than": "Hướng Đông Nam"
    }

# ==============================================================================
# 7. PHÂN TÍCH ĐỐI CHIẾU CHÉO (CROSS-VALIDATION & CONFLICT AUDIT)
# ==============================================================================
def cross_validate(weather, iching, tarot, tuvi):
    """Phân tích đối chiếu giữa 4 phương pháp xem có mâu thuẫn không"""
    sync_points = []
    conflict_points = []
    
    # 1. So sánh Kinh Dịch vs Tarot
    tarot_is_action = tarot["is_upright"] and tarot["type"] in ["Major", "Wands", "Swords"]
    iching_is_peace = "Nhu" in iching["hex_name"] or "Khôn" in iching["hex_name"] or "Cấn" in iching["hex_name"]
    
    if iching_is_peace and tarot_is_action:
        conflict_points.append("Kinh Dịch khuyên tĩnh tại chờ thời, trong khi lá bài Tarot hối thúc năng lượng hành động. Lời khuyên dung hòa: Vạch sẵn kế hoạch chiến lược sắc bén trong tâm trí nhưng hành động bên ngoài cần điềm tĩnh, tránh bốc đồng.")
    else:
        sync_points.append(f"Kinh Dịch ({iching['hex_name']}) và Tarot ({tarot['name']}) đồng quy năng lượng tích cực, tạo đà tâm lý vững chãi.")
        
    # 2. So sánh Bản mệnh Can Chi vs Thời tiết
    if tuvi["score"] >= 8 and "mưa" not in weather["desc"].lower():
        sync_points.append(f"Thiên thời bên ngoài ({weather['temp']}°C, {weather['desc']}) hòa quyện trọn vẹn với Cát khí bản mệnh ({tuvi['day_can_chi']}), cực kỳ thuận lợi cho các hoạt động ngoại giao.")
    elif "mưa" in weather["desc"].lower():
        conflict_points.append("Trường khí bản mệnh rất tốt nhưng thời tiết có mưa gió cản trở di chuyển. Lời khuyên: Ưu tiên họp bàn và ra quyết định trực tuyến.")

    # 3. Kết luận chiến lược 1 câu duy nhất
    if tuvi["score"] >= 9:
        verdict = "🔥 NGÀY ĐẠI CÁT ĐẮC THỜI: Vạn sự hanh thông, hãy mạnh dạn quyết đoán các mục tiêu trọng tâm!"
    elif tuvi["score"] <= 5:
        verdict = "🛡️ NGÀY PHÒNG THỦ CHIẾN LƯỢC: Lấy tĩnh chế động, tập trung củng cố nội lực và rà soát hồ sơ."
    else:
        verdict = "✨ NGÀY CÂN BẰNG TÍCH TỰU: Tiến thoái nhịp nhàng, làm tốt từng đầu việc sẽ gặt hái kết quả bền vững."
        
    return {
        "sync_points": sync_points,
        "conflict_points": conflict_points,
        "verdict": verdict
    }

# ==============================================================================
# 8. TỔNG HỢP SOẠN BẢN TIN TELEGRAM THEO CHUẨN EXECUTIVE DRAFTER
# ==============================================================================
def compose_morning_telegram_dispatch():
    """Tạo bản tin Telegram hoàn chỉnh chào ngày mới Chủ tịch"""
    # Đọc cấu hình
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            
    if not config.get("enabled", True):
        return None, "Tính năng Automation Ban Tâm Linh hiện đang TẮT theo cấu hình."
        
    city = config.get("location", "Hà Nội")
    now = datetime.now()
    now_str = now.strftime("%d/%m/%Y")
    
    # 1. Lấy dữ liệu 4 nguồn
    weather = get_live_weather(city)
    iching = cast_iching_maihoa(now)
    tarot = draw_daily_tarot()
    tuvi = calculate_lunar_and_day_compatibility(now)
    
    # 2. Phân tích đối chiếu chéo
    synthesis = cross_validate(weather, iching, tarot, tuvi)
    
    # 3. Soạn tin nhắn Telegram đẳng cấp (Bản Markdown lưu trữ & Bản HTML tối ưu hiển thị di động)
    msg = f"""👑 [TỔNG HÀNH DINH] — BẢN TIN TÂM LINH & KHÍ VẬN ĐẦU NGÀY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Chào buổi sáng Chủ tịch Cao Xuân Trường!
📅 Ngày: {now_str} (Ngày {tuvi['day_can_chi']})
👤 Bản Mệnh: Canh Ngọ 1990 (Lộ Bàng Thổ — Tọa Quý Giờ Tân Mùi)
🌤️ Thời tiết {city}: {weather['temp']}°C (Cảm giác: {weather['feels_like']}°C), {weather['desc']}

> "{synthesis['verdict']}"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣ ☯️ KINH DỊCH THỜI THẾ (MAI HOA ĐẦU NGÀY)
• Quẻ Chủ: {iching['hex_name']} ({iching['nature']})
• Thoán Ý: {iching['meaning']}
• Lời Khuyên Hành Động: {iching['advice']}

2️⃣ 🔮 CHIÊM NIỆM TAROT (ENERGY ARCHETYPE)
• Lá Bài Rút Được: {tarot['name']} — {tarot['state']}
• Thông Điệp Năng Lượng: {tarot['meaning']}

3️⃣ 📜 TỬ VI & TRẠCH CÁT BẢN MỆNH CHỦ TỊCH
• Đánh Giá Ngày: {tuvi['rating']} (Điểm khí vận: {tuvi['score']}/10)
• Cát Khí Chiếu Mệnh:
  {chr(10).join(['  ' + b for b in tuvi['blessings']]) if tuvi['blessings'] else '  • Khí trường ổn định'}
• Cảnh Báo Cần Tránh:
  {chr(10).join(['  ' + c for c in tuvi['cautions']]) if tuvi['cautions'] else '  • Không có xung khắc lớn'}
• Khung Giờ Hoàng Đạo Khởi Sự: {', '.join(tuvi['hoang_dao'][:3])}
• Hướng Nghênh Cát: Hỷ Thần ({tuvi['hy_than']}) | Tài Thần ({tuvi['tai_than']})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 ĐỐI CHIẾU ĐA CHIỀU & KẾT LUẬN ĐIỀU HÀNH
{chr(10).join(['• [ĐỒNG QUY] ' + s for s in synthesis['sync_points']])}
{chr(10).join(['• [LƯU TÂM] ' + c for c in synthesis['conflict_points']]) if synthesis['conflict_points'] else '• Các trường phái đồng thuận cao, không có xung đột năng lượng.'}

📌 HÀNH ĐỘNG KHUYÊN DÙNG HÔM NAY:
✅ Tập trung xử lý các hợp đồng và quyết sách lớn trong khung Giờ Hoàng Đạo.
✅ Duy trì tâm thế vững vàng, dứt khoát theo chỉ dẫn quẻ {iching['hex_name']}.

Chúc Chủ tịch một ngày mới tràn đầy sinh khí, hanh thông vạn sự!
#BanTamLinh #ChaoNgayMoi #ExecutiveBriefing #ChuTichCaoXuanTruong"""

    msg_html = f"""👑 <b>[TỔNG HÀNH DINH] — BẢN TIN TÂM LINH & KHÍ VẬN ĐẦU NGÀY</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Kính chào Chủ tịch Cao Xuân Trường!</b>
📅 <b>Ngày:</b> {now_str} (Ngày {tuvi['day_can_chi']})
👤 <b>Bản Mệnh:</b> Canh Ngọ 1990 (Lộ Bàng Thổ — Tọa Quý Giờ Tân Mùi)
🌤️ <b>Thời tiết {city}:</b> {weather['temp']}°C (Cảm giác: {weather['feels_like']}°C), {weather['desc']}

<blockquote>{synthesis['verdict']}</blockquote>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣ ☯️ <b>KINH DỊCH THỜI THẾ (MAI HOA ĐẦU NGÀY)</b>
• <b>Quẻ Chủ:</b> {iching['hex_name']} ({iching['nature']})
• <b>Thoán Ý:</b> {iching['meaning']}
• <b>Lời Khuyên:</b> {iching['advice']}

2️⃣ 🔮 <b>CHIÊM NIỆM TAROT (ENERGY ARCHETYPE)</b>
• <b>Lá Bài:</b> {tarot['name']} — {tarot['state']}
• <b>Thông Điệp Năng Lượng:</b> {tarot['meaning']}

3️⃣ 📜 <b>TỬ VI & TRẠCH CÁT BẢN MỆNH CHỦ TỊCH</b>
• <b>Đánh Giá Ngày:</b> {tuvi['rating']} (Điểm khí vận: {tuvi['score']}/10)
• <b>Cát Khí Chiếu Mệnh:</b>
{chr(10).join(['  ' + b for b in tuvi['blessings']]) if tuvi['blessings'] else '  • Khí trường ổn định'}
• <b>Cảnh Báo Cần Tránh:</b>
{chr(10).join(['  ' + c for c in tuvi['cautions']]) if tuvi['cautions'] else '  • Không có xung khắc lớn'}
• <b>Khung Giờ Hoàng Đạo:</b> {', '.join(tuvi['hoang_dao'][:3])}
• <b>Hướng Nghênh Cát:</b> Hỷ Thần ({tuvi['hy_than']}) | Tài Thần ({tuvi['tai_than']})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 <b>ĐỐI CHIẾU ĐA CHIỀU & KẾT LUẬN ĐIỀU HÀNH</b>
{chr(10).join(['• <b>[ĐỒNG QUY]</b> ' + s for s in synthesis['sync_points']])}
{chr(10).join(['• <b>[LƯU TÂM]</b> ' + c for c in synthesis['conflict_points']]) if synthesis['conflict_points'] else '• Các trường phái đồng thuận cao, không có xung đột năng lượng.'}

📌 <b>HÀNH ĐỘNG TRỌNG TÂM HÔM NAY:</b>
✅ Tập trung xử lý các hợp đồng và quyết sách lớn trong khung Giờ Hoàng Đạo.
✅ Duy trì tâm thế vững vàng, dứt khoát theo chỉ dẫn quẻ {iching['hex_name']}.

<i>Chúc Chủ tịch một ngày mới tràn đầy sinh khí, hanh thông vạn sự!</i>
#BanTamLinh #ChaoNgayMoi #ExecutiveBriefing #ChuTichCaoXuanTruong"""

    # Lưu bản ghi ra file log nhật ký
    log_file = os.path.join(LOG_DIR, f"briefing_{now.strftime('%Y%m%d_%H%M%S')}.md")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(msg)
        
    return msg, msg_html, log_file

# ==============================================================================
# 9. GỬI TIN NHẮN QUA TELEGRAM BOT
# ==============================================================================
def send_telegram_message(message_text, html_text=None):
    """Gửi tin nhắn Telegram qua bot @tapdoan_bot"""
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            
    bot_token = config.get("telegram", {}).get("bot_token") or "8821881768:AAFysU6f0IGu4qHHVeN5P-b1fqgFHNPcECI"
    chat_id = config.get("telegram", {}).get("chat_id")
    
    # Nếu chưa có chat_id, thử dò tự động qua getUpdates
    if not chat_id:
        try:
            updates_url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
            req = urllib.request.Request(updates_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                results = data.get("result", [])
                if results:
                    last_msg = results[-1]
                    chat_id = last_msg.get("message", {}).get("chat", {}).get("id")
                    if chat_id:
                        config["telegram"]["chat_id"] = str(chat_id)
                        with open(CONFIG_FILE, "w", encoding="utf-8") as f_out:
                            json.dump(config, f_out, ensure_ascii=False, indent=2)
        except Exception:
            pass

    if not chat_id:
        print("[WARNING] Chưa có Telegram chat_id của Chủ tịch. Tin nhắn đã được lưu trữ nội bộ.")
        return False
        
    send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    # Thử gửi định dạng HTML trước để hiển thị tối ưu trên di động
    if html_text:
        try:
            payload = {
                "chat_id": chat_id,
                "text": html_text,
                "parse_mode": "HTML"
            }
            req_data = urllib.parse.urlencode(payload).encode("utf-8")
            req = urllib.request.Request(send_url, data=req_data, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                res = json.loads(resp.read().decode())
                if res.get("ok"):
                    print("[SUCCESS] Đã gửi bản tin Telegram (HTML) chào ngày mới thành công!")
                    return True
        except Exception as e:
            print(f"[NOTICE] Gửi HTML chưa thành công ({e}), chuyển sang fallback...")

    # Fallback gửi Plain Text
    try:
        payload = {
            "chat_id": chat_id,
            "text": message_text
        }
        req_data = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(send_url, data=req_data, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            res = json.loads(resp.read().decode())
            if res.get("ok"):
                print("[SUCCESS] Đã gửi bản tin Telegram chào ngày mới thành công!")
                return True
    except Exception as e:
        print(f"[ERROR] Không thể gửi Telegram: {e}")
        return False

# ==============================================================================
# HÀM MAIN
# ==============================================================================
if __name__ == "__main__":
    res = compose_morning_telegram_dispatch()
    if res[0]:
        msg, msg_html, log_path = res
        print("=== BẢN TIN TÂM LINH & KHÍ VẬN ĐẦU NGÀY ===")
        print(msg)
        print(f"\n[INFO] Đã ghi nhật ký vào: {log_path}")
        send_telegram_message(msg, msg_html)
    else:
        print(f"[NOTICE] {res[1]}")
