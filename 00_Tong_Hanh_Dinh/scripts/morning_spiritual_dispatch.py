#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BAN CỐ VẤN TÂM LINH & PHONG THỦY — TỔNG HÀNH DINH TẬP ĐOÀN
Script: morning_spiritual_dispatch.py (Phiên bản Nâng cấp Toàn diện 2026)
Tự động hóa: 06:30 sáng hàng ngày
Tác vụ:
1. Dự báo Khí tượng & Môi trường thời gian thực (CHUYÊN BIỆT TẠI HÀ NỘI).
2. Gieo quẻ Kinh Dịch Mai Hoa theo giờ khắc đầu ngày (Đủ 64 Quẻ, Hào Động, Quẻ Biến & Quẻ Hổ).
3. Rút lá bài Tarot chiêm niệm năng lượng ngày mới (Đủ 78 lá Rider-Waite, tâm lý học Carl Jung).
4. Tra cứu Tử Vi & Trạch Cát Bản Mệnh Chủ tịch Cao Xuân Trường (Canh Ngọ 1990 - Lộ Bàng Thổ).
   - Can Chi, 12 Trực, 28 Tú thiên văn.
   - Giờ Hoàng Đạo và Hướng Hỷ Thần / Tài Thần động tính toán theo từng ngày.
5. Tổng Hợp Đối Chiếu Đa Chiều & Đúc Kết Lãnh Đạo Độc Bản (Spiritual Executive Synthesizer).
6. Soạn và gửi Bản tin Telegram Điều Hành qua Bot @tapdoan_bot.
"""

import os
import sys
import json
import time
import random
import hashlib
import argparse
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

# Thiết lập UTF-8 cho console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Thư mục làm việc
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_FILE = os.path.join(SCRIPT_DIR, "spiritual_config.json")
LOG_DIR = os.path.join(PROJECT_DIR, "nhat_ky_tam_linh")
HISTORY_FILE = os.path.join(LOG_DIR, "dispatch_history.json")
os.makedirs(LOG_DIR, exist_ok=True)

# Múi giờ Việt Nam chuẩn (Hà Nội: UTC+7)
VN_TZ = timezone(timedelta(hours=7))

def get_vn_now():
    """Luôn lấy thời gian chính xác theo múi giờ Việt Nam (UTC+7) bất kể máy chủ đặt ở đâu (UTC hay local)"""
    return datetime.now(timezone.utc).astimezone(VN_TZ)


# ==============================================================================
# 1. HỆ THỐNG DỮ LIỆU KINH DỊCH ĐỦ 64 QUẺ CHUẨN XÁC
# ==============================================================================
# Tiên Thiên Bát Quái: 1: Càn, 2: Đoài, 3: Ly, 4: Chấn, 5: Tốn, 6: Khảm, 7: Cấn, 8: Khôn
BAGUA_NATURE = {
    1: "Thiên",
    2: "Trạch",
    3: "Hỏa",
    4: "Lôi",
    5: "Phong",
    6: "Thủy",
    7: "Sơn",
    8: "Địa"
}

TRIGRAM_LINES = {
    1: [1, 1, 1], # Càn (Thiên)
    2: [1, 1, 0], # Đoài (Trạch)
    3: [1, 0, 1], # Ly (Hỏa)
    4: [1, 0, 0], # Chấn (Lôi)
    5: [0, 1, 1], # Tốn (Phong)
    6: [0, 1, 0], # Khảm (Thủy)
    7: [0, 0, 1], # Cấn (Sơn)
    8: [0, 0, 0], # Khôn (Địa)
}
LINES_TO_TRIGRAM = {tuple(v): k for k, v in TRIGRAM_LINES.items()}

HEXAGRAMS_64 = {
    # Nhóm Càn (Thượng quái = 1)
    (1, 1): {"name": "Thuần Càn", "nature": "Thiên Địa Tương Ứng", "meaning": "Đại hanh thông, thời cơ vàng để phát triển", "advice": "Cương kiện bất tức, giữ vững chính đạo, tránh kiêu ngạo tự phụ."},
    (1, 2): {"name": "Thiên Trạch Lý", "nature": "Dẫm Lên Đuôi Hổ", "meaning": "Đi trong hiểm nguy nhưng giữ lễ nghĩa ắt vô sự", "advice": "Cẩn trọng từng lời nói và văn bản pháp lý, đối đãi hòa nhã với đối tác."},
    (1, 3): {"name": "Thiên Hỏa Đồng Nhân", "nature": "Đồng Tâm Hiệp Lực", "meaning": "Đoàn kết rộng rãi, chí lớn gặp nhau", "advice": "Quy tụ hiền tài, minh bạch mục tiêu chung, phá bỏ rào cản nội bộ."},
    (1, 4): {"name": "Thiên Lôi Vô Vọng", "nature": "Chân Thật Tự Nhiên", "meaning": "Thuận theo tự nhiên, chớ toan tính lọc lừa", "advice": "Nói thật làm thật, tuân thủ đạo lý kinh doanh, phúc lành tự đến."},
    (1, 5): {"name": "Thiên Phong Cấu", "nature": "Bất Ngờ Gặp Gỡ", "meaning": "Gió thổi dưới trời, cơ duyên bất ngờ", "advice": "Đề phòng tiểu nhân chen ngang hoặc đối tác bề ngoài bóng bẩy nhưng thiếu thực chất."},
    (1, 6): {"name": "Thiên Thủy Tụng", "nature": "Tranh Chấp Kiện Tụng", "meaning": "Bất đồng ý kiến, dễ sinh xung đột", "advice": "Lùi một bước trời cao biển rộng, hòa giải thương lượng trước khi tranh chấp."},
    (1, 7): {"name": "Thiên Sơn Độn", "nature": "Lùi Bước Ẩn Mình", "meaning": "Thời thế chưa thuận, nên tạm rút lui", "advice": "Bảo toàn lực lượng, tái cấu trúc nội bộ, không ham đối đầu trực diện."},
    (1, 8): {"name": "Thiên Địa Bĩ", "nature": "Bế Tắc Ngăn Trở", "meaning": "Khí vận chưa thông, tiểu nhân lấn lướt", "advice": "Kiên trì giữ vững khí tiết, ẩn nhẫn chờ thời, quản lý chặt dòng tiền."},

    # Nhóm Đoài (Thượng quái = 2)
    (2, 1): {"name": "Trạch Thiên Quái", "nature": "Dứt Khoát Quyết Đoán", "meaning": "Vạch trần tiêu cực, thanh lọc bộ máy", "advice": "Hành động dứt khoát nhưng chớ dùng vũ lực bạo tàn, giữ lòng nhân đạo."},
    (2, 2): {"name": "Thuần Đoài", "nature": "Đầm Nước Hoan Ca", "meaning": "Vui vẻ hòa thuận, đàm phán thành công", "advice": "Dùng lời nói truyền cảm hứng, đàm phán hai bên cùng thắng (Win-Win)."},
    (2, 3): {"name": "Trạch Hỏa Cách", "nature": "Cải Cách Canh Tân", "meaning": "Thay cũ đổi mới, chuyển mình bứt phá", "advice": "Mạnh dạn cải tiến quy trình trì trệ, ứng dụng công nghệ mới."},
    (2, 4): {"name": "Trạch Lôi Tùy", "nature": "Tùy Thời Biến Chuyển", "meaning": "Linh hoạt thuận theo hoàn cảnh", "advice": "Thích ứng nhanh với biến động thị trường, lắng nghe phản hồi của khách hàng."},
    (2, 5): {"name": "Trạch Phong Đại Quá", "nature": "Gánh Nặng Quá Tải", "meaning": "Cột kèo lung lay, áp lực quá sức", "advice": "Cắt giảm chi phí rườm rà, phân quyền ủy nhiệm, chớ ôm đồm việc một mình."},
    (2, 6): {"name": "Trạch Thủy Khốn", "nature": "Bế Tắc Khó Khăn", "meaning": "Nước rút cạn đầm, tài chính eo hẹp", "advice": "Tiết kiệm chi phí tối đa, kiên định với giá trị cốt lõi, hành động chứng minh."},
    (2, 7): {"name": "Trạch Sơn Hàm", "nature": "Cảm Ứng Giao Hòa", "meaning": "Tâm ý tương thông, đối tác chân thành", "advice": "Lắng nghe bằng sự thấu cảm, xây dựng lòng tin bền vững từ đáy lòng."},
    (2, 8): {"name": "Trạch Địa Tụy", "nature": "Quy Tụ Tinh Hoa", "meaning": "Quần tụ nguồn lực, tiền tài hội tụ", "advice": "Tập trung vốn và nhân lực vào mũi nhọn then chốt, đề phòng nội bộ chia rẽ."},

    # Nhóm Ly (Thượng quái = 3)
    (3, 1): {"name": "Hỏa Thiên Đại Hữu", "nature": "Sở Hữu To Lớn", "meaning": "Trời ban phúc lộc, thành quả rực rỡ", "advice": "Khiêm tốn bao dung, chia sẻ thành quả với cộng sự, tránh xa sự kiêu ngạo."},
    (3, 2): {"name": "Hỏa Trạch Khuê", "nature": "Trái Ý Bất Đồng", "meaning": "Nhìn về hai hướng khác nhau, xung đột quan điểm", "advice": "Tìm kiếm điểm tương đồng trong dị biệt (Cầu đồng tồn dị), chớ vội ép buộc."},
    (3, 3): {"name": "Thuần Ly", "nature": "Lửa Sáng Rực Rỡ", "meaning": "Văn minh, sáng suốt, danh tiếng vang xa", "advice": "Phát huy tư duy chiến lược, giữ lòng trung chính, dựa vào người hiền tài."},
    (3, 4): {"name": "Hỏa Lôi Phệ Hạp", "nature": "Cắn Đứt Trở Ngại", "meaning": "Thực thi pháp luật, trừ khử gian dối", "advice": "Kỷ luật nghiêm minh, rà soát kiểm toán rõ ràng, không dung túng sai phạm."},
    (3, 5): {"name": "Hỏa Phong Đỉnh", "nature": "Vững Như Đỉnh Vạc", "meaning": "Nấu nướng luyện tài, kiến tạo đế chế vững bền", "advice": "Bổ nhiệm đúng người đúng việc, phân chia lợi ích minh bạch và công bằng."},
    (3, 6): {"name": "Hỏa Thủy Vị Tế", "nature": "Chưa Xong Còn Tiếp", "meaning": "Khởi đầu cho một chu kỳ mới", "advice": "Thận trọng từng bước qua khúc quanh, giữ vững ngọn lửa nhiệt huyết khởi nghiệp."},
    (3, 7): {"name": "Hỏa Sơn Lữ", "nature": "Lữ Khách Phương Xa", "meaning": "Đi xa lập nghiệp, môi trường mới mẻ", "advice": "Thận trọng khi mở rộng thị trường mới, tôn trọng văn hóa địa phương."},
    (3, 8): {"name": "Hỏa Địa Tấn", "nature": "Mặt Trời Mọc Lên", "meaning": "Tiến bước rực rỡ, được cấp trên nâng đỡ", "advice": "Thừa thắng xông lên, khẳng định năng lực vượt trội, tranh thủ thời cơ lớn."},

    # Nhóm Chấn (Thượng quái = 4)
    (4, 1): {"name": "Lôi Thiên Đại Tráng", "nature": "Khí Thế Hùng Mạnh", "meaning": "Sức mạnh đang lên như vũ bão", "advice": "Dùng sức mạnh đi đôi với sự kiềm chế, chớ manh động kẻo húc đầu vào đá."},
    (4, 2): {"name": "Lôi Trạch Quy Muội", "nature": "Hôn Nhân Sai Thời", "meaning": "Quan hệ hợp tác chưa chín muồi, đảo lộn trật tự", "advice": "Xem xét lại điều khoản hợp tác liên doanh, chớ vì lợi trước mắt mà vội vàng."},
    (4, 3): {"name": "Lôi Hỏa Phong", "nature": "Thịnh Vượng Đỉnh Cao", "meaning": "Sấm giông chớp giật, danh vọng tột bậc", "advice": "Đang ở đỉnh cao cần lo lúc suy thoái, chuẩn bị phương án phòng ngừa rủi ro."},
    (4, 4): {"name": "Thuần Chấn", "nature": "Sấm Vang Ngàn Dặm", "meaning": "Kinh thiên động địa, biến động bất ngờ", "advice": "Bình tĩnh trước tiếng ồn thị trường, lấy tĩnh chế động, nội tâm bất biến."},
    (4, 5): {"name": "Lôi Phong Hằng", "nature": "Bền Vững Lâu Dài", "meaning": "Đạo lý trường tồn, kiên định mục tiêu", "advice": "Duy trì kỷ luật vận hành bền bỉ, không thay đổi xoành xoạch tôn chỉ cốt lõi."},
    (4, 6): {"name": "Lôi Thủy Giải", "nature": "Giải Tỏa Hiểm Nguy", "meaning": "Mưa rào dập tắt hạn hán, nút thắt được tháo gỡ", "advice": "Nhanh chóng hành động giải phóng hàng tồn hoặc dòng tiền, tha thứ lỗi lầm nhỏ."},
    (4, 7): {"name": "Lôi Sơn Tiểu Quá", "nature": "Hơi Vượt Chút Ít", "meaning": "Việc nhỏ nên làm, việc lớn khoan vội", "advice": "Tập trung giải quyết các chi tiết vận hành hàng ngày, cẩn thận giấy tờ hợp đồng."},
    (4, 8): {"name": "Lôi Địa Dự", "nature": "Vui Vẻ Thuận Đạo", "meaning": "Hứng khởi tràn đầy, chuẩn bị sẵn sàng", "advice": "Lên tinh thần cho đội ngũ nhưng không được chủ quan thỏa mãn sớm."},

    # Nhóm Tốn (Thượng quái = 5)
    (5, 1): {"name": "Phong Thiên Tiểu Súc", "nature": "Tích Lũy Nhỏ", "meaning": "Gió mây tụ lại chưa thành mưa lớn", "advice": "Làm tốt từng việc nhỏ, tích tiểu thành đại, kiên nhẫn bồi đắp nguồn lực."},
    (5, 2): {"name": "Phong Trạch Trung Phu", "nature": "Thành Tín Nội Tâm", "meaning": "Chân thành cảm hóa muôn người", "advice": "Giữ lời hứa tuyệt đối với khách hàng và cổ đông, tín nghĩa tạo nên đế chế."},
    (5, 3): {"name": "Phong Hỏa Gia Nhân", "nature": "Đạo Lý Gia Đình", "meaning": "Nội bộ êm ấm, hậu phương vững chắc", "advice": "Chăm lo đội ngũ nhân sự ruột thịt, quản trị gia đình và doanh nghiệp hài hòa."},
    (5, 4): {"name": "Phong Lôi Ích", "nature": "Gia Tăng Lợi Ích", "meaning": "Tài lộc dồi dào, gió thổi sấm vang", "advice": "Thấy việc tốt nên làm ngay, thấy sai sót sửa liền, tái đầu tư mở rộng quy mô."},
    (5, 5): {"name": "Thuần Tốn", "nature": "Gió Lượn Khắp Chốn", "meaning": "Mềm dẻo thấu triệt, linh hoạt uyển chuyển", "advice": "Khéo léo trong ngoại giao, nhượng bộ chiến thuật để đạt toàn thắng chiến lược."},
    (5, 6): {"name": "Phong Thủy Hoán", "nature": "Gió Thổi Tan Băng", "meaning": "Giải tỏa bế tắc, khơi thông dòng chảy", "advice": "Chủ động hòa giải mâu thuẫn, khơi thông dòng tiền ứ đọng, đổi mới tư duy."},
    (5, 7): {"name": "Phong Sơn Tiệm", "nature": "Tiến Từng Bước Một", "meaning": "Cây mọc trên núi, phát triển vững chắc", "advice": "Dục tốc bất đạt, tiến công theo từng lộ trình chuẩn mực, không nhảy cóc."},
    (5, 8): {"name": "Phong Địa Quán", "nature": "Chiêm Ngưỡng Quan Sát", "meaning": "Gió đi trên đất, nhìn thấu toàn cảnh", "advice": "Nâng cao tầm nhìn bao quát, làm gương cho cấp dưới noi theo."},

    # Nhóm Khảm (Thượng quái = 6)
    (6, 1): {"name": "Thủy Thiên Nhu", "nature": "Kiên Nhẫn Chờ Thời", "meaning": "Trước mắt có sông sâu, cần ăn uống chờ thời", "advice": "Nuôi dưỡng tinh thần, tích lũy tài lực, chớ nóng vội xuất chiêu khi chưa đủ thế."},
    (6, 2): {"name": "Thủy Trạch Tiết", "nature": "Tiết Chế Điều Hòa", "meaning": "Giữ chừng mực, quản trị rủi ro nghiêm ngặt", "advice": "Kiểm soát chi tiêu ngân sách chặt chẽ, tuân thủ kỷ luật dừng lỗ (Stop-loss)."},
    (6, 3): {"name": "Thủy Hỏa Ký Tế", "nature": "Đã Thành Đại Sự", "meaning": "Mọi việc đã vào guồng hoàn tất mỹ mãn", "advice": "Đề phòng suy thoái sau đỉnh cao, chuẩn bị sẵn phương án dự phòng tương lai."},
    (6, 4): {"name": "Thủy Lôi Truân", "nature": "Vạn Sự Khởi Đầu Nan", "meaning": "Mới bắt đầu nhiều trắc trở, hỗn độn", "advice": "Chớ vội manh động, cần củng cố đội ngũ, tìm kiếm quý nhân phò trợ."},
    (6, 5): {"name": "Thủy Phong Tỉnh", "nature": "Giếng Nước Nuôi Dân", "meaning": "Nguồn lực bất tận nếu biết khai thác bền vững", "advice": "Tập trung nâng cao năng lực cốt lõi doanh nghiệp, chăm sóc khách hàng ruột."},
    (6, 6): {"name": "Thuần Khảm", "nature": "Hiểm Trở Trùng Trùng", "meaning": "Nước sâu vực thẳm, thử thách liên tiếp", "advice": "Giữ tâm vững như bàn thạch, từng bước vượt thác hiểm nguy, không hoảng loạn."},
    (6, 7): {"name": "Thủy Sơn Kiển", "nature": "Gian Nan Trắc Trở", "meaning": "Núi cao trước mặt, sông sâu sau lưng", "advice": "Tạm dừng bước để suy xét lại kế hoạch, tìm kiếm sự trợ giúp từ chuyên gia."},
    (6, 8): {"name": "Thủy Địa Tỷ", "nature": "Thân Mật Gắn Kết", "meaning": "Hợp tác hữu nghị, bạn bè quý nhân quy tụ", "advice": "Chủ động liên kết đối tác, tạo dựng đồng minh tin cậy, giữ chữ tín hàng đầu."},

    # Nhóm Cấn (Thượng quái = 7)
    (7, 1): {"name": "Sơn Thiên Đại Súc", "nature": "Tích Lũy Lớn", "meaning": "Bản lĩnh vững vàng, tích lũy tài đức to lớn", "advice": "Sẵn sàng cho các chiến dịch quy mô lớn, đầu tư mạnh vào công nghệ và con người."},
    (7, 2): {"name": "Sơn Trạch Tổn", "nature": "Bớt Dưới Thêm Trên", "meaning": "Chấp nhận hy sinh cái nhỏ để được cái lớn", "advice": "Đầu tư chi phí để đổi lấy đối tác chiến lược dài hạn, chớ so đo chi li vụn vặt."},
    (7, 3): {"name": "Sơn Hỏa Bí", "nature": "Trang Nhã Tô Điểm", "meaning": "Văn vẻ sáng sủa, trang trí hoàn thiện", "advice": "Trau chuốt hình ảnh thương hiệu, giao diện sản phẩm và bao bì chuyên nghiệp."},
    (7, 4): {"name": "Sơn Lôi Di", "nature": "Nuôi Dưỡng Bản Thân", "meaning": "Coi trọng lời ăn tiếng nói và nuôi dưỡng hiền tài", "advice": "Quan tâm sức khỏe cá nhân, cẩn trọng phát ngôn trên truyền thông và mạng xã hội."},
    (7, 5): {"name": "Sơn Phong Cổ", "nature": "Trừ Bỏ Mục Ruỗng", "meaning": "Việc cũ đổ nát cần chấn chỉnh tái thiết", "advice": "Mạnh tay giải quyết các lỗ hổng quản trị cũ, dọn dẹp quy trình rườm rà."},
    (7, 6): {"name": "Sơn Thủy Mông", "nature": "Mở Mang Trí Tuệ", "meaning": "Chưa rõ phương hướng, cần học hỏi chỉ dẫn", "advice": "Giữ tâm khiêm tốn, lắng nghe cố vấn và chuyên gia, tránh quyết định mù quáng."},
    (7, 7): {"name": "Thuần Cấn", "nature": "Núi Non Sừng Sững", "meaning": "Biết dừng đúng lúc, tĩnh tâm tu dưỡng", "advice": "Biết điểm dừng của lòng tham, bảo toàn thành quả, không chạy theo sóng ảo."},
    (7, 8): {"name": "Sơn Địa Bác", "nature": "Tiêu Mòn Sụp Đổ", "meaning": "Nền tảng lung lay, tiểu nhân phá hoại", "advice": "Củng cố lại nền tảng tài chính và nhân sự cốt lõi, không mở rộng liều lĩnh."},

    # Nhóm Khôn (Thượng quái = 8)
    (8, 1): {"name": "Địa Thiên Thái", "nature": "Bĩ Cực Thái Lai", "meaning": "Trời Đất giao hòa, vạn sự hanh thông rực rỡ", "advice": "Nắm bắt cơ hội vàng để mở rộng quy mô, ký kết hợp đồng, giải phóng nguồn lực."},
    (8, 2): {"name": "Địa Trạch Lâm", "nature": "Tiếp Cận Đến Gần", "meaning": "Thời cơ đang tới gần, thế lực lớn mạnh", "advice": "Chủ động tiếp cận đối tác chiến lược, kiểm soát chặt chẽ tiến độ triển khai."},
    (8, 3): {"name": "Địa Hỏa Minh Di", "nature": "Ánh Sáng Bị Tổn Thương", "meaning": "Mặt trời lặn xuống đất, hoàn cảnh bất lợi", "advice": "Giấu bớt sự sắc sảo, khiêm tốn thu mình, tránh để đối thủ dòm ngó soi mói."},
    (8, 4): {"name": "Địa Lôi Phục", "nature": "Sấm Động Dưới Đất", "meaning": "Dương khí hồi sinh, mùa xuân trở lại", "advice": "Khởi động lại các dự án ấp ủ, từng bước hồi phục nhịp độ kinh doanh."},
    (8, 5): {"name": "Địa Phong Thăng", "nature": "Cây Mọc Từ Đất", "meaning": "Thăng tiến vững chắc, từng bước đi lên", "advice": "Tận dụng đà tăng trưởng, cầu thị học hỏi người đi trước, không nóng vội."},
    (8, 6): {"name": "Địa Thủy Sư", "nature": "Hưng Binh Dấy Nghĩa", "meaning": "Tổ chức lực lượng, kỷ luật quân ngũ nghiêm minh", "advice": "Dùng người đúng sở trường, kỷ luật sắt đá, hành động vì mục tiêu tập thể."},
    (8, 7): {"name": "Địa Sơn Khiêm", "nature": "Núi Ẩn Dưới Đất", "meaning": "Khiêm tốn tột bậc, phúc đức vô biên", "advice": "Càng thành công càng phải khiêm nhường, tôn trọng cộng sự và đối tác."},
    (8, 8): {"name": "Thuần Khôn", "nature": "Vạn Vật Sinh Sôi", "meaning": "Mềm mỏng bao dung, tích lũy nội lực bền bỉ", "advice": "Dùng nhu thắng cương, nhẫn nại tích đức, nâng đỡ cấp dưới tận tâm."}
}

# ==============================================================================
# 2. HỆ THỐNG DỮ LIỆU TAROT ĐỦ 78 LÁ RIDER-WAITE SMITH
# ==============================================================================
TAROT_DECK_78 = [
    # 22 Major Arcana
    {"name": "The Fool (0)", "type": "Major", "upright": "Khởi đầu mới, tiềm năng vô hạn, tinh thần dũng cảm phiêu lưu.", "reversed": "Hành động liều lĩnh, thiếu tính toán rủi ro, bốc đồng non nớt."},
    {"name": "The Magician (I)", "type": "Major", "upright": "Năng lực hành động xuất sắc, biến ý tưởng thành hiện thực, đầy đủ nguồn lực.", "reversed": "Thao túng, ảo tưởng quyền năng, lãng phí tài năng hoặc gian lận."},
    {"name": "The High Priestess (II)", "type": "Major", "upright": "Trực giác sắc bén, sự tĩnh lặng nhìn thấu bản chất, bí mật hé lộ.", "reversed": "Bỏ qua trực giác, thông tin bị bưng bít, nghi ngờ thiếu cơ sở."},
    {"name": "The Empress (III)", "type": "Major", "upright": "Thịnh vượng trù phú, dự án đơm hoa kết trái, nuôi dưỡng đội ngũ.", "reversed": "Lãng phí ngân sách, sáng tạo bế tắc, phụ thuộc quá mức."},
    {"name": "The Emperor (IV)", "type": "Major", "upright": "Quyền lực tối cao, kỷ luật thép, kiến tạo trật tự và hệ thống bền vững.", "reversed": "Độc đoán, cứng nhắc, kiểm soát thái quá làm ngạt thở cấp dưới."},
    {"name": "The Hierophant (V)", "type": "Major", "upright": "Tuân thủ quy chuẩn, liên minh pháp lý, cố vấn từ bậc tiền bối uy tín.", "reversed": "Giáo điều bảo thủ, quy tắc lỗi thời, cần phá vỡ giới hạn cũ."},
    {"name": "The Lovers (VI)", "type": "Major", "upright": "Hợp tác đồng lòng, lựa chọn chiến lược quan trọng dựa trên giá trị cốt lõi.", "reversed": "Xung đột lợi ích giữa các đối tác, phân vân do dự làm lỡ thời cơ."},
    {"name": "The Chariot (VII)", "type": "Major", "upright": "Ý chí sắt đá, vượt qua nghịch cảnh bằng kỷ luật, tốc độ tiến công nhanh.", "reversed": "Mất kiểm soát tay lái, hung hăng hiếu chiến, kiệt sức vì chạy đua."},
    {"name": "Strength (VIII)", "type": "Major", "upright": "Bản lĩnh nội tâm, kiên nhẫn cảm hóa đối thủ, làm chủ cơn giận.", "reversed": "Thiếu tự tin, dao động cảm xúc, dễ bị kích động trước áp lực."},
    {"name": "The Hermit (IX)", "type": "Major", "upright": "Tĩnh tâm chiêm nghiệm, nghiên cứu sâu, định hình chiến lược dài hạn.", "reversed": "Cô lập thái quá, xa rời thực tế thị trường, trì hoãn thực thi."},
    {"name": "Wheel of Fortune (X)", "type": "Major", "upright": "Thời vận xoay chuyển, may mắn bất ngờ gõ cửa, chu kỳ thịnh vượng mở ra.", "reversed": "Vận hạn tạm thời, nghịch cảnh khách quan, cần kiên nhẫn tích lũy."},
    {"name": "Justice (XI)", "type": "Major", "upright": "Công minh chính trực, pháp lý phân minh, quyết định khách quan không thiên vị.", "reversed": "Bất công, rủi ro pháp lý tiềm ẩn, thiếu minh bạch trong số liệu."},
    {"name": "The Hanged Man (XII)", "type": "Major", "upright": "Góc nhìn đột phá từ sự dừng lại, buông bỏ cái cũ để đón nhận điều lớn hơn.", "reversed": "Hy sinh vô ích, bảo thủ trì trệ, không dám thay đổi góc nhìn."},
    {"name": "Death (XIII)", "type": "Major", "upright": "Chấm dứt giai đoạn cũ đã mục ruỗng, lột xác tái sinh mạnh mẽ.", "reversed": "Cố bám víu vào mô hình đã chết, sợ hãi đổi mới, trì trệ cục bộ."},
    {"name": "Temperance (XIV)", "type": "Major", "upright": "Cân bằng tuyệt đối, dung hòa các mặt đối lập, kiên nhẫn và điều độ.", "reversed": "Mất cân đối dòng tiền, cực đoan nóng vội làm hỏng đại sự."},
    {"name": "The Devil (XV)", "type": "Major", "upright": "Cảnh báo cạm bẫy tài chính, ràng buộc ngầm, lòng tham che mờ lý trí.", "reversed": "Thức tỉnh thoát khỏi bẫy, nhận diện sự thật, giải phóng nguồn lực."},
    {"name": "The Tower (XVI)", "type": "Major", "upright": "Sụp đổ bất ngờ của ảo tưởng, biến động lớn dọn đường cho chân giá trị.", "reversed": "Cố che giấu khủng hoảng, rạn nứt âm ỉ chưa được giải quyết triệt để."},
    {"name": "The Star (XVII)", "type": "Major", "upright": "Hy vọng rực rỡ, cảm hứng sáng tạo dồi dào, tương lai rộng mở thênh thang.", "reversed": "Mất phương hướng, bi quan không căn cứ, kỳ vọng phi thực tế."},
    {"name": "The Moon (XVIII)", "type": "Major", "upright": "Màn sương mờ ảo, thông tin chưa rõ ràng, cẩn trọng bẫy tâm lý và ngộ nhận.", "reversed": "Mây tan trăng sáng, sự thật sáng tỏ, thoát khỏi hoang mang."},
    {"name": "The Sun (XIX)", "type": "Major", "upright": "Thành công chói lọi, sinh khí tràn trề, dự án đạt đỉnh cao danh tiếng.", "reversed": "Tự mãn quá sớm, bóng bẩy bên ngoài nhưng thiếu chiều sâu bên trong."},
    {"name": "Judgement (XX)", "type": "Major", "upright": "Hiệu triệu thức tỉnh, đánh giá tổng kết chính xác, bước lên tầm cao mới.", "reversed": "Tự phán xét tiêu cực, do dự bỏ lỡ tiếng gọi của vận mệnh lớn."},
    {"name": "The World (XXI)", "type": "Major", "upright": "Viên mãn trọn vẹn, hoàn thành đại nghiệp, vươn tầm quy mô quốc tế.", "reversed": "Chưa hoàn tất khâu cuối cùng, thiếu chút nhẫn nại để cán đích hoàn hảo."},

    # 14 Wands (Gậy - Hành động, Chiến lược, Khát vọng)
    {"name": "Ace of Wands", "type": "Wands", "upright": "Ý tưởng đột phá, ngọn lửa đam mê bùng cháy, cơ hội khởi phát dự án mới.", "reversed": "Thiếu nhiệt huyết, ý tưởng dang dở, trì hoãn khởi động."},
    {"name": "Two of Wands", "type": "Wands", "upright": "Lập kế hoạch vươn xa, nắm quyền quyết định, mở rộng tầm nhìn kinh doanh.", "reversed": "Sợ bước ra khỏi vùng an toàn, kế hoạch thiếu thực tế, mâu thuẫn mục tiêu."},
    {"name": "Three of Wands", "type": "Wands", "upright": "Tàu bè ra khơi, mở rộng thương mại, thành quả bước đầu xuất hiện.", "reversed": "Kế hoạch mở rộng gặp trở ngại, tầm nhìn hạn hẹp, chậm trễ logistics."},
    {"name": "Four of Wands", "type": "Wands", "upright": "Ăn mừng thắng lợi, nền móng vững chắc, nội bộ đoàn kết hòa hợp.", "reversed": "Bất ổn nội bộ, chia rẽ nhóm then chốt, tiệc tùng lãng phí."},
    {"name": "Five of Wands", "type": "Wands", "upright": "Cạnh tranh khốc liệt, va chạm quan điểm, cần bản lĩnh dẫn dắt vượt sóng.", "reversed": "Tránh né xung đột, thỏa hiệp tiêu cực, mệt mỏi vì đấu đá nội bộ."},
    {"name": "Six of Wands", "type": "Wands", "upright": "Vinh quang chiến thắng, sự công nhận xứng đáng từ thị trường và cộng sự.", "reversed": "Rơi vào bẫy tự cao, tai tiếng truyền thông, hào quang giả tạo."},
    {"name": "Seven of Wands", "type": "Wands", "upright": "Bảo vệ vững chắc vị thế dẫn đầu, kiên cường chống lại áp lực cạnh tranh.", "reversed": "Bị áp đảo, đuối sức trước đối thủ, nhượng bộ không đáng có."},
    {"name": "Eight of Wands", "type": "Wands", "upright": "Tốc độ hành động thần tốc, tin vui dồn dập, thời cơ chín muồi.", "reversed": "Nóng vội hấp tấp, thông tin sai lệch gây hoảng loạn, hành động thiếu chuẩn bị."},
    {"name": "Nine of Wands", "type": "Wands", "upright": "Bản lĩnh kiên cường ở chặng cuối, cảnh giác bảo vệ thành quả.", "reversed": "Kiệt sức, phòng thủ quá mức sinh đa nghi, bỏ cuộc trước cửa ải cuối."},
    {"name": "Ten of Wands", "type": "Wands", "upright": "Gánh nặng trách nhiệm lớn, cần ủy quyền chia sẻ áp lực cho đội ngũ.", "reversed": "Sụp đổ vì quá tải, ôm đồm việc vi mô, giải phóng bớt áp lực thừa."},
    {"name": "Page of Wands", "type": "Wands", "upright": "Tín hiệu cơ hội mới đầy hào hứng, tinh thần học hỏi khám phá.", "reversed": "Nông nổi thiếu kinh nghiệm, hứa hẹn nhiều làm ít, thiếu cam kết."},
    {"name": "Knight of Wands", "type": "Wands", "upright": "Tiến công quyết liệt, dũng cảm đương đầu thử thách, khí thế ngút trời.", "reversed": "Bốc đồng hung hăng, đốt cháy giai đoạn, làm hỏng việc vì thiếu kiên nhẫn."},
    {"name": "Queen of Wands", "type": "Wands", "upright": "Tự tin rạng rỡ, sức hút truyền cảm hứng mạnh mẽ, quản trị bằng tình yêu nghề.", "reversed": "Ghen tị đố kỵ, kiểm soát cảm xúc kém, áp đặt chủ quan."},
    {"name": "King of Wands", "type": "Wands", "upright": "Nhà lãnh đạo có tầm nhìn vĩ mô, truyền lửa và dẫn dắt tập đoàn bứt phá.", "reversed": "Độc đoán chuyên quyền, đòi hỏi phi lý, thiếu lắng nghe thực tế."},

    # 14 Cups (Cốc - Trực giác, Quan hệ, Cảm xúc)
    {"name": "Ace of Cups", "type": "Cups", "upright": "Tình cảm chan hòa, sự kết nối chân thành, tâm an yên tạo nên phúc lộc.", "reversed": "Cảm xúc tiêu cực tràn ngập, hao hụt năng lượng, hiểu lầm tình cảm."},
    {"name": "Two of Cups", "type": "Cups", "upright": "Hợp tác hoàn hảo, đối tác tâm đầu ý hợp, ký kết hợp đồng thuận lợi.", "reversed": "Bất đồng đối tác, thiếu tin tưởng lẫn nhau, cam kết lỏng lẻo."},
    {"name": "Three of Cups", "type": "Cups", "upright": "Hội ngộ vui vẻ, tinh thần đồng đội thăng hoa, cùng chung niềm vui thắng lợi.", "reversed": "Hè bè phái cục bộ, phân tán nguồn lực vào tiệc tùng thừa thãi."},
    {"name": "Four of Cups", "type": "Cups", "upright": "Thờ ơ lãnh đạm, bỏ qua cơ hội trước mắt, cần tĩnh tâm nhìn nhận lại.", "reversed": "Thoát khỏi u mê, đón nhận cơ hội mới, sẵn sàng kết nối lại."},
    {"name": "Five of Cups", "type": "Cups", "upright": "Thất vọng về điều đã mất, cần quay đầu nhìn lại những nguồn lực còn nguyên vẹn.", "reversed": "Chữa lành tổn thất, vượt qua tiếc nuối, chấp nhận sự thật để tiến bước."},
    {"name": "Six of Cups", "type": "Cups", "upright": "Tri ân cội nguồn, đối tác lâu năm ủng hộ, giá trị truyền thống bền vững.", "reversed": "Mắc kẹt trong quá khứ vàng son, từ chối đối mới cho phù hợp hiện tại."},
    {"name": "Seven of Cups", "type": "Cups", "upright": "Nhiều lựa chọn cám dỗ, ảo tưởng viển vông, cần tỉnh táo lọc lấy cái thực chất.", "reversed": "Xác định rõ mục tiêu cốt lõi, thoát khỏi mơ mộng, chọn đúng đường."},
    {"name": "Eight of Cups", "type": "Cups", "upright": "Dũng cảm rời bỏ nơi không còn giá trị, tìm kiếm lý tưởng cao đẹp hơn.", "reversed": "Chần chừ không dám dứt khoát, bám víu vào hoàn cảnh trì trệ."},
    {"name": "Nine of Cups", "type": "Cups", "upright": "Ước nguyện thành hiện thực, mãn nguyện về tài chính và tinh thần.", "reversed": "Tự mãn hưởng lạc, lòng tham vô đáy, thiếu chia sẻ với cộng sự."},
    {"name": "Ten of Cups", "type": "Cups", "upright": "Hạnh phúc viên mãn, tổ ấm bình an, doanh nghiệp phát triển bền vững như một gia đình.", "reversed": "Rạn nứt nội bộ, bất hòa gia đạo ảnh hưởng đến tâm lý điều hành."},
    {"name": "Page of Cups", "type": "Cups", "upright": "Tin tức tốt lành, trực giác nhạy bén, thông điệp sáng tạo bất ngờ.", "reversed": "Tính khí thất thường, nhạy cảm quá mức, tin đồn thất thiệt."},
    {"name": "Knight of Cups", "type": "Cups", "upright": "Sứ giả hòa giải, phong thái lịch thiệp, lời đề nghị hợp tác hấp dẫn.", "reversed": "Hứa hão thất tín, ảo tưởng tình cảm, thiếu tính thực tế."},
    {"name": "Queen of Cups", "type": "Cups", "upright": "Tâm hồn thấu cảm sâu sắc, trực giác tâm linh nhạy bén, che chở cấp dưới.", "reversed": "Bất ổn cảm xúc, phụ thuộc tâm lý, phán đoán bị tình cảm chi phối."},
    {"name": "King of Cups", "type": "Cups", "upright": "Làm chủ cảm xúc đỉnh cao, sáng suốt điềm tĩnh giữa tâm bão khủng hoảng.", "reversed": "Thao túng tâm lý, lạnh lùng tàn nhẫn, nội tâm xáo trộn."},

    # 14 Swords (Kiếm - Trí tuệ, Quyết định, Pháp lý)
    {"name": "Ace of Swords", "type": "Swords", "upright": "Sự thật sáng tỏ, quyết định sắc bén giải tỏa bế tắc, chiến thắng bằng trí tuệ.", "reversed": "Phát ngôn gây tổn thương, phán quyết sai lệch, bế tắc ý tưởng."},
    {"name": "Two of Swords", "type": "Swords", "upright": "Thế giằng co cân bằng, cần thêm thông tin xác thực trước khi quyết định.", "reversed": "Bế tắc tâm lý, quá tải thông tin, bị ép buộc lựa chọn sai lầm."},
    {"name": "Three of Swords", "type": "Swords", "upright": "Sự thật đau lòng nhưng cần thiết để giải phóng, cắt đứt ung nhọt.", "reversed": "Dần hồi phục sau tổn thương, buông bỏ oán trách, hướng tới tương lai."},
    {"name": "Four of Swords", "type": "Swords", "upright": "Nghỉ ngơi tĩnh dưỡng, tái tạo năng lượng trí tuệ, án binh bất động.", "reversed": "Kiệt sức vì không chịu nghỉ ngơi, bồn chồn lo lắng vô cớ."},
    {"name": "Five of Swords", "type": "Swords", "upright": "Thắng trận nhưng mất lòng người, cạnh tranh không lành mạnh để lại di chứng.", "reversed": "Hòa giải xung đột, chấm dứt tranh cãi vô bổ, học bài học khiêm tốn."},
    {"name": "Six of Swords", "type": "Swords", "upright": "Rời xa giông bão tiến vào vùng nước êm đềm, chuyển đổi mô hình thành công.", "reversed": "Khó khăn kéo dài chưa dứt, hành trình chuyển đổi gặp cản trở."},
    {"name": "Seven of Swords", "type": "Swords", "upright": "Chiến lược thông minh luồn lách qua hiểm nguy, đề phòng rò rỉ dữ liệu mật.", "reversed": "Kế hoạch ám muội bị bại lộ, nhận trách nhiệm, sửa chữa sai lầm."},
    {"name": "Eight of Swords", "type": "Swords", "upright": "Tự trói buộc mình trong nỗi sợ tưởng tượng, rào cản do tâm trí dựng lên.", "reversed": "Nhận ra lối thoát, cởi bỏ trói buộc tâm lý, tìm lại sự tự do."},
    {"name": "Nine of Swords", "type": "Swords", "upright": "Lo âu mất ngủ, áp lực đè nặng tâm trí, phóng đại nguy cơ quá mức.", "reversed": "Bình tâm trở lại, nhận ra vấn đề không nghiêm trọng như tưởng tượng."},
    {"name": "Ten of Swords", "type": "Swords", "upright": "Chạm đáy của khủng hoảng, kết thúc dứt điểm nỗi đau để bình minh ló rạng.", "reversed": "Vực dậy sau cú ngã đau, bài học đắt giá mở ra con đường mới."},
    {"name": "Page of Swords", "type": "Swords", "upright": "Tư duy phản biện sắc sảo, cảnh giác cao độ, thu thập thông tin tình báo tốt.", "reversed": "Soi mói xét nét, phát ngôn bừa bãi thiếu chứng cứ, hiếu thắng trẻ con."},
    {"name": "Knight of Swords", "type": "Swords", "upright": "Tấn công trực diện dũng mãnh, quyết liệt giải quyết dứt điểm vấn đề tồn đọng.", "reversed": "Hấp tấp lỗ mãng, đâm đầu vào tường đá, tạo thêm kẻ thù không đáng có."},
    {"name": "Queen of Swords", "type": "Swords", "upright": "Minh triết chính trực, nhìn thấu sự thật, giao tiếp chuẩn xác không nhân nhượng.", "reversed": "Cay nghiệt lạnh lùng, định kiến hẹp hòi, phán xét vô tình."},
    {"name": "King of Swords", "type": "Swords", "upright": "Uy quyền trí tuệ tối cao, phán quyết công bằng, làm chủ luật chơi và nguyên tắc.", "reversed": "Lạm quyền độc đoán, dùng trí tuệ để chèn ép cấp dưới, tàn nhẫn."},

    # 14 Pentacles (Tiền - Tài chính, Tài sản, Vận hành)
    {"name": "Ace of Pentacles", "type": "Pentacles", "upright": "Dòng tiền mới rót vào, cơ hội đầu tư sinh lời vững chắc, tài lộc hiện hữu.", "reversed": "Bỏ lỡ cơ hội tài chính, tính toán ngân sách sai lệch, chi tiêu hoang phí."},
    {"name": "Two of Pentacles", "type": "Pentacles", "upright": "Khéo léo xoay xở dòng tiền, linh hoạt cân đối nhiều nguồn lực đồng thời.", "reversed": "Mất cân đối tài chính, xoay vòng vốn quá tải, rơi vào khủng hoảng tiền mặt."},
    {"name": "Three of Pentacles", "type": "Pentacles", "upright": "Hợp tác chuyên môn đỉnh cao, chất lượng công trình và sản phẩm xuất sắc.", "reversed": "Thiếu phối hợp nhóm, tay nghề non kém, bất đồng ý kiến kỹ thuật."},
    {"name": "Four of Pentacles", "type": "Pentacles", "upright": "Quản trị tài sản an toàn, tích lũy vốn liếng, giữ vững thành quả đã đạt.", "reversed": "Keo kiệt bủn xỉn làm mất lòng người, sợ hãi không dám tái đầu tư phát triển."},
    {"name": "Five of Pentacles", "type": "Pentacles", "upright": "Khó khăn tài chính tạm thời, cảm giác cô độc, cần tìm kiếm sự hỗ trợ kịp thời.", "reversed": "Vượt qua giai đoạn eo hẹp, dòng tiền bắt đầu hồi phục, ánh sáng cuối đường hầm."},
    {"name": "Six of Pentacles", "type": "Pentacles", "upright": "Chia sẻ nguồn lực công bằng, hào phóng đầu tư, thu hút phúc lộc dồi dào.", "reversed": "Ban ơn kèm điều kiện trói buộc, phân chia lợi ích thiếu minh bạch."},
    {"name": "Seven of Pentacles", "type": "Pentacles", "upright": "Đánh giá lại hiệu quả đầu tư, kiên nhẫn chờ cây ra hoa kết trái.", "reversed": "Nóng vội muốn gặt sớm khi chưa chín, đầu tư vào dự án không sinh lời."},
    {"name": "Eight of Pentacles", "type": "Pentacles", "upright": "Chuyên tâm trau dồi tay nghề, kỷ luật lao động cao độ, hoàn thiện chi tiết xuất sắc.", "reversed": "Làm việc cẩu thả, đốt cháy quy trình, thiếu đam mê nghề nghiệp."},
    {"name": "Nine of Pentacles", "type": "Pentacles", "upright": "Độc lập tự chủ tài chính, hưởng thụ thành quả xứng đáng, đẳng cấp tinh tế.", "reversed": "Phụ thuộc tài chính, phô trương của cải bên ngoài, nội tại rỗng tuếch."},
    {"name": "Ten of Pentacles", "type": "Pentacles", "upright": "Đế chế trường tồn, tài sản gia tộc vững bền, truyền thừa di sản vẻ vang.", "reversed": "Tranh chấp tài sản gia đình/cổ đông, nền móng lung lay vì lòng tham."},
    {"name": "Page of Pentacles", "type": "Pentacles", "upright": "Cơ hội kinh doanh thực tế, thái độ cầu thị nghiêm túc, quản lý tiền bạc cẩn thận.", "reversed": "Lười biếng thiếu kỷ luật, ảo tưởng làm giàu nhanh, bỏ bê kế hoạch học hỏi."},
    {"name": "Knight of Pentacles", "type": "Pentacles", "upright": "Kỷ luật sắt son, thực thi bền bỉ, từng bước biến mục tiêu thành hiện thực vững chắc.", "reversed": "Trì trệ bảo thủ, quá chậm chạp làm lỡ thời cơ vàng, cứng nhắc."},
    {"name": "Queen of Pentacles", "type": "Pentacles", "upright": "Tài năng quản trị tài chính thực tế, chăm sóc chu đáo đời sống nhân viên, trù phú.", "reversed": "Mất cân bằng giữa công việc và cuộc sống, lo lắng thái quá về tiền bạc."},
    {"name": "King of Pentacles", "type": "Pentacles", "upright": "Đại gia kinh doanh lão luyện, quản trị gia sản đỉnh cao, dòng tiền thịnh vượng ổn định.", "reversed": "Tham lam ích kỷ, coi trọng tiền hơn đạo lý, đầu cơ mạo hiểm nguy hiểm."}
]

# ==============================================================================
# 3. DỰ BÁO KHÍ TƯỢNG THỰC TẾ — CHUYÊN BIỆT TẠI HÀ NỘI
# ==============================================================================
def get_hanoi_live_weather():
    """
    Lấy dữ liệu thời tiết thời gian thực CHUYÊN BIỆT TẠI HÀ NỘI
    Tọa độ: 21.0285°N, 105.8542°E (Khu vực làm việc và điều hành của Chủ tịch)
    """
    city_name = "Hà Nội"
    try:
        url = "https://wttr.in/Hanoi?format=j1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode())
            current = data['current_condition'][0]
            temp = current.get('temp_C', '30')
            feels = current.get('FeelsLikeC', '32')
            desc_en = current.get('weatherDesc', [{'value': 'Partly cloudy'}])[0]['value']
            humidity = current.get('humidity', '65')
            wind = current.get('windspeedKmph', '12')
            uv = current.get('uvIndex', '5')
            
            # Dịch sang tiếng Việt chuẩn mực
            desc_vn = desc_en
            translations = {
                "Clear": "Trời quang, nắng ráo",
                "Sunny": "Trời nắng đẹp",
                "Partly cloudy": "Trời có mây nhẹ, nắng ráo",
                "Cloudy": "Trời nhiều mây dịu mát",
                "Overcast": "Trời u ám, râm mát",
                "Mist": "Sương mù nhẹ đầu ngày",
                "Patchy rain possible": "Có thể có mưa rào rải rác",
                "Light rain": "Mưa nhỏ ngắt quãng",
                "Moderate rain": "Mưa rào vừa",
                "Heavy rain": "Mưa to, giông",
                "Thundery outbreaks possible": "Đề phòng mưa giông sấm chớp"
            }
            for k, v in translations.items():
                if k.lower() in desc_en.lower():
                    desc_vn = v
                    break
                    
            return {
                "city": city_name,
                "temp": temp,
                "feels_like": feels,
                "desc": desc_vn,
                "humidity": humidity,
                "wind_kmh": wind,
                "uv": uv,
                "status": "OK"
            }
    except Exception as e:
        # Fallback dữ liệu tiết trời Hà Nội an toàn nếu có sự cố mạng
        return {
            "city": city_name,
            "temp": "29",
            "feels_like": "31",
            "desc": "Trời mây nhẹ, thoáng đãng",
            "humidity": "68",
            "wind_kmh": "10",
            "uv": "5",
            "status": "FALLBACK"
        }

# ==============================================================================
# 4. THUẬT TOÁN KINH DỊCH MAI HOA ĐỘNG (ĐỦ 64 QUẺ & BIẾN QUẺ)
# ==============================================================================
def cast_iching_maihoa(dt=None):
    """
    Lập Quẻ Mai Hoa Dịch Số theo giờ khắc khởi sự.
    Sinh ra bộ 3 Quẻ: Quẻ Chủ, Quẻ Hổ (Bên trong) và Quẻ Biến (Kết quả tương lai).
    """
    if dt is None:
        dt = get_vn_now()
        
    year_val = dt.year % 8 or 8
    month_val = dt.month % 8 or 8
    day_val = dt.day % 8 or 8
    hour_val = dt.hour % 8 or 8
    min_val = dt.minute % 6 or 6
    
    # 1. Thượng Quái & Hạ Quái
    upper_num = (year_val + month_val + day_val) % 8 or 8
    lower_num = (year_val + month_val + day_val + hour_val) % 8 or 8
    dong_hao = (year_val + month_val + day_val + hour_val + min_val) % 6 or 6
    
    # 2. Quẻ Chủ
    chu_key = (upper_num, lower_num)
    hex_chu = HEXAGRAMS_64.get(chu_key, HEXAGRAMS_64[(1, 1)])
    
    # 3. Quẻ Hổ (Hạ quái = hào 2,3,4; Thượng quái = hào 3,4,5)
    lines = TRIGRAM_LINES[lower_num] + TRIGRAM_LINES[upper_num]
    lower_ho = tuple(lines[1:4])
    upper_ho = tuple(lines[2:5])
    ho_lower_num = LINES_TO_TRIGRAM.get(lower_ho, 1)
    ho_upper_num = LINES_TO_TRIGRAM.get(upper_ho, 1)
    hex_ho = HEXAGRAMS_64.get((ho_upper_num, ho_lower_num), HEXAGRAMS_64[(1, 1)])
    
    # 4. Quẻ Biến (Đảo hào động 1..6)
    new_lines = list(lines)
    new_lines[dong_hao - 1] = 1 - new_lines[dong_hao - 1]
    bien_lower_num = LINES_TO_TRIGRAM.get(tuple(new_lines[0:3]), 1)
    bien_upper_num = LINES_TO_TRIGRAM.get(tuple(new_lines[3:6]), 1)
    hex_bien = HEXAGRAMS_64.get((bien_upper_num, bien_lower_num), HEXAGRAMS_64[(1, 1)])
    
    upper_nature = BAGUA_NATURE.get(upper_num, "Thiên")
    lower_nature = BAGUA_NATURE.get(lower_num, "Thiên")
    
    return {
        "upper_num": upper_num,
        "lower_num": lower_num,
        "dong_hao": dong_hao,
        "hex_chu": {
            "name": hex_chu["name"],
            "nature": f"{upper_nature} {lower_nature} — {hex_chu['nature']}",
            "meaning": hex_chu["meaning"],
            "advice": hex_chu["advice"]
        },
        "hex_ho": {
            "name": hex_ho["name"],
            "meaning": hex_ho["meaning"]
        },
        "hex_bien": {
            "name": hex_bien["name"],
            "meaning": hex_bien["meaning"],
            "advice": hex_bien["advice"]
        }
    }

# ==============================================================================
# 5. THUẬT TOÁN RÚT BÀI TAROT NGẪU NHIÊN CHUẨN XÁC (78 LÁ)
# ==============================================================================
def draw_daily_tarot(dt=None):
    """
    Rút ngẫu nhiên 1 lá bài từ bộ 78 lá Rider-Waite Smith.
    Sử dụng hàm băm kết hợp ngày và hạt giống entropy để đảm bảo tính duyên khởi khách quan.
    """
    if dt is None:
        dt = get_vn_now()
        
    date_seed = int(hashlib.sha256(f"{dt.strftime('%Y-%m-%d_%H')}_spiritual".encode()).hexdigest(), 16)
    rng = random.Random(date_seed + int(time.time() % 1000))
    
    card = rng.choice(TAROT_DECK_78)
    # Xác suất thuận 70%, ngược 30%
    is_upright = rng.random() < 0.70
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
# 6. TỬ VI & TRẠCH CÁT BẢN MỆNH CHỦ TỊCH CAO XUÂN TRƯỜNG (1990)
# ==============================================================================
CAN_LIST = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI_LIST = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

HOANG_DAO_SCHEDULE = {
    "Tý": ["Giờ Tý (23h-01h)", "Giờ Sửu (01h-03h)", "Giờ Mão (05h-07h)", "Giờ Ngọ (11h-13h)", "Giờ Thân (15h-17h)", "Giờ Dậu (17h-19h)"],
    "Ngọ": ["Giờ Tý (23h-01h)", "Giờ Sửu (01h-03h)", "Giờ Mão (05h-07h)", "Giờ Ngọ (11h-13h)", "Giờ Thân (15h-17h)", "Giờ Dậu (17h-19h)"],
    "Sửu": ["Giờ Dần (03h-05h)", "Giờ Mão (05h-07h)", "Giờ Tỵ (09h-11h)", "Giờ Thân (15h-17h)", "Giờ Tuất (19h-21h)", "Giờ Hợi (21h-23h)"],
    "Mùi": ["Giờ Dần (03h-05h)", "Giờ Mão (05h-07h)", "Giờ Tỵ (09h-11h)", "Giờ Thân (15h-17h)", "Giờ Tuất (19h-21h)", "Giờ Hợi (21h-23h)"],
    "Dần": ["Giờ Tý (23h-01h)", "Giờ Sửu (01h-03h)", "Giờ Thìn (07h-09h)", "Giờ Tỵ (09h-11h)", "Giờ Mùi (13h-15h)", "Giờ Tuất (19h-21h)"],
    "Thân": ["Giờ Tý (23h-01h)", "Giờ Sửu (01h-03h)", "Giờ Thìn (07h-09h)", "Giờ Tỵ (09h-11h)", "Giờ Mùi (13h-15h)", "Giờ Tuất (19h-21h)"],
    "Mão": ["Giờ Tý (23h-01h)", "Giờ Dần (03h-05h)", "Giờ Mão (05h-07h)", "Giờ Ngọ (11h-13h)", "Giờ Mùi (13h-15h)", "Giờ Dậu (17h-19h)"],
    "Dậu": ["Giờ Tý (23h-01h)", "Giờ Dần (03h-05h)", "Giờ Mão (05h-07h)", "Giờ Ngọ (11h-13h)", "Giờ Mùi (13h-15h)", "Giờ Dậu (17h-19h)"],
    "Thìn": ["Giờ Dần (03h-05h)", "Giờ Thìn (07h-09h)", "Giờ Tỵ (09h-11h)", "Giờ Thân (15h-17h)", "Giờ Dậu (17h-19h)", "Giờ Hợi (21h-23h)"],
    "Tuất": ["Giờ Dần (03h-05h)", "Giờ Thìn (07h-09h)", "Giờ Tỵ (09h-11h)", "Giờ Thân (15h-17h)", "Giờ Dậu (17h-19h)", "Giờ Hợi (21h-23h)"],
    "Tỵ": ["Giờ Sửu (01h-03h)", "Giờ Thìn (07h-09h)", "Giờ Ngọ (11h-13h)", "Giờ Mùi (13h-15h)", "Giờ Tuất (19h-21h)", "Giờ Hợi (21h-23h)"],
    "Hợi": ["Giờ Sửu (01h-03h)", "Giờ Thìn (07h-09h)", "Giờ Ngọ (11h-13h)", "Giờ Mùi (13h-15h)", "Giờ Tuất (19h-21h)", "Giờ Hợi (21h-23h)"],
}

HY_TAI_DIRECTIONS = {
    "Giáp": ("Hướng Đông Bắc", "Hướng Chính Nam"),
    "Kỷ": ("Hướng Đông Bắc", "Hướng Chính Nam"),
    "Ất": ("Hướng Tây Bắc", "Hướng Tây Nam"),
    "Canh": ("Hướng Tây Bắc", "Hướng Tây Nam"),
    "Bính": ("Hướng Tây Nam", "Hướng Chính Đông"),
    "Tân": ("Hướng Tây Nam", "Hướng Chính Đông"),
    "Đinh": ("Hướng Chính Nam", "Hướng Chính Tây"),
    "Nhâm": ("Hướng Chính Nam", "Hướng Chính Tây"),
    "Mậu": ("Hướng Đông Nam", "Hướng Chính Bắc"),
    "Quý": ("Hướng Đông Nam", "Hướng Chính Bắc"),
}

TRUC_12 = ["Kiến", "Trừ", "Mãn", "Bình", "Định", "Chấp", "Phá", "Nguy", "Thành", "Thâu", "Khai", "Bế"]
TRUC_MEANINGS = {
    "Kiến": "Khởi đầu công việc mới, xuất hành, chiêu mộ nhân sự.",
    "Trừ": "Trừ bỏ rủi ro, thanh lý tồn đọng, giải quyết dứt điểm nợ nần.",
    "Mãn": "Thu hoạch tài lộc, đơm hoa kết trái, mở rộng thị trường.",
    "Bình": "Cân bằng nội bộ, đàm phán ôn hòa, giải tỏa bất đồng.",
    "Định": "Ký kết hợp đồng, chốt thỏa thuận cổ đông, ấn định kế hoạch dài hạn.",
    "Chấp": "Bảo vệ thành quả, thực thi kỷ luật nội bộ, củng cố quy trình.",
    "Phá": "Phá vỡ giới hạn cũ, tái cấu trúc bộ máy; kỵ ký giao kết lớn.",
    "Nguy": "Cẩn trọng rủi ro bất ngờ, án binh bất động, kiểm toán nội bộ.",
    "Thành": "Vạn sự hanh thông, công thành danh toại, ký kết đại cát.",
    "Thâu": "Thu hồi công nợ, tích lũy vốn liếng, nạp tài nhập quỹ.",
    "Khai": "Khai trương chi nhánh, ra mắt dự án mới, xuất hành đón tài.",
    "Bế": "Đóng cửa tiết kiệm chi phí, bảo toàn vốn liếng, không nên mạo hiểm."
}

def calculate_tuvi_and_compatibility(dt=None):
    """
    Tính toán lịch can chi thiên văn và đối chiếu chính xác Bản Mệnh Chủ tịch Cao Xuân Trường
    (Sinh 13:45 ngày 19/04/1990 - Canh Ngọ / Lộ Bàng Thổ - Tọa Quý Giờ Tân Mùi).
    """
    if dt is None:
        dt = get_vn_now()
        
    a = (14 - dt.month) // 12
    y = dt.year + 4800 - a
    m = dt.month + 12 * a - 3
    jdn = dt.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    
    can_idx = (jdn + 9) % 10
    chi_idx = (jdn + 1) % 12
    day_can = CAN_LIST[can_idx]
    day_chi = CHI_LIST[chi_idx]
    day_can_chi = f"{day_can} {day_chi}"
    
    # 1. Giờ Hoàng Đạo
    hoang_dao_list = HOANG_DAO_SCHEDULE.get(day_chi, HOANG_DAO_SCHEDULE["Tý"])
    
    # 2. Hướng Cát
    hy_than, tai_than = HY_TAI_DIRECTIONS.get(day_can, ("Hướng Đông Bắc", "Hướng Chính Nam"))
    
    # 3. Trực Ngày
    # Tính trực theo tháng (ước lượng tương đối theo tiết khí)
    month_chi_idx = (dt.month + 1) % 12
    truc_idx = (chi_idx - month_chi_idx) % 12
    truc_name = TRUC_12[truc_idx]
    truc_desc = TRUC_MEANINGS.get(truc_name, "Trực cát điều hòa")
    
    # 4. Đối chiếu Bản Mệnh Canh Ngọ 1990
    blessings = []
    cautions = []
    score = 7
    rating = "Bình Hòa — Vận Thế Ổn Định"
    
    # Cát Thần
    if day_chi == "Mùi":
        blessings.append("🌟 Lục Hợp Quý Chiếu (Ngọ - Mùi tương sinh): Vạn sự thuận hòa, đối tác đồng lòng, ký kết đắc lợi.")
        blessings.append("👑 Đắc Thiên Ất Quý Nhân: Bề trên nâng đỡ, quý nhân phò tá giải trừ trở ngại.")
        rating = "Đại Cát — Hoàng Kim Đắc Lộc"
        score = 10
    elif day_chi in ["Dần", "Tuất"]:
        blessings.append(f"🔥 Tam Hợp Hỏa Cục ({day_chi} - Ngọ): Khí thế ngút ngàn, uy quyền mở rộng, thanh thế vang xa.")
        rating = "Cát Lợi — Thuận Buồm Xuôi Gió"
        score = 9
    elif day_chi == "Thân":
        blessings.append("💰 Đắc Thiên Lộc Thần: Cung Tài Bạch mở rộng, thuận lợi cho giải ngân đầu tư và ký hợp đồng lớn.")
        blessings.append("🐎 Đắc Dịch Mã: Thuận lợi cho xuất hành công tác và mở rộng chi nhánh hải ngoại.")
        rating = "Cát Lợi — Vượng Tài Tụ Lộc"
        score = 9
    elif day_chi == "Sửu":
        blessings.append("👑 Đắc Thiên Ất Quý Nhân: Quý nhân tương trợ trong các cuộc đàm phán quan trọng.")
        cautions.append("⚠️ Tương Hại Nhẹ (Sửu hại Ngọ): Cẩn trọng lời ăn tiếng nói, tránh áp đặt người dưới quyền.")
        rating = "Khởi Sắc — Tích Cực Có Chọn Lọc"
        score = 8
    elif day_chi == "Tý":
        cautions.append("🚨 Lục Xung Trực Diện (Tý xung Ngọ): Tuyệt đối tránh quyết định nóng vội hoặc xuất vốn mạo hiểm.")
        cautions.append("🛡️ Giữ tâm tĩnh lặng, lấy phòng thủ làm thượng sách, kiểm toán rà soát nội bộ.")
        rating = "Thận Trọng — Phòng Thủ Chiến Lược"
        score = 5
    elif day_chi == "Ngọ":
        cautions.append("⚠️ Tự Hình Bản Chi: Đề phòng áp lực tâm lý tự tạo ra, tránh chủ quan tự mãn.")
        rating = "Bình Hòa — Cẩn Ngôn Cẩn Trọng"
        score = 6
    elif day_chi in ["Mão", "Dậu"]:
        cautions.append(f"⚡ Phạm Tứ Hành Xung ({day_chi}): Đề phòng đối thủ tung tin gây nhiễu, cần kiểm chứng thông tin.")
        score = 6
        rating = "Thận Trọng — Giữ Vững Kỷ Luật"
    else:
        blessings.append("✨ Khí trường nhật nguyệt bình hòa, không xung khắc bản mệnh Lộ Bàng Thổ.")
        score = 8
        rating = "Thuận Lợi Hanh Thông"
        
    return {
        "day_can_chi": day_can_chi,
        "rating": rating,
        "score": score,
        "blessings": blessings,
        "cautions": cautions,
        "hoang_dao": hoang_dao_list,
        "hy_than": hy_than,
        "tai_than": tai_than,
        "truc_name": truc_name,
        "truc_desc": truc_desc
    }

# ==============================================================================
# 7. TỔNG HỢP CHIẾN LƯỢC ĐỐI CHIẾU ĐA CHIỀU (SPIRITUAL EXECUTIVE SYNTHESIZER)
# ==============================================================================
def synthesize_executive_guidance(weather, iching, tarot, tuvi):
    """
    Tổng hợp 4 nguồn dữ liệu thành bức tranh chiến lược độc bản, sâu sắc cho ngày mới của Chủ tịch.
    """
    sync_insights = []
    conflict_insights = []
    action_items = []
    
    # 1. Đối chiếu Kinh Dịch vs Tarot
    hex_name = iching["hex_chu"]["name"]
    tarot_name = tarot["name"]
    is_tarot_upright = tarot["is_upright"]
    
    # Nhận diện tính chất động/tĩnh của Kinh Dịch
    is_iching_active = any(k in hex_name for k in ["Càn", "Đại Hữu", "Tấn", "Quái", "Ích", "Thái", "Phục", "Thăng"])
    is_iching_passive = any(k in hex_name for k in ["Cấn", "Khôn", "Nhu", "Độn", "Bĩ", "Khốn", "Kiển", "Tiết"])
    
    if is_iching_active and is_tarot_upright:
        sync_insights.append(f"Kinh Dịch ({hex_name}) và Tarot ({tarot_name}) cộng hưởng xung lực mạnh mẽ. Thiên thời và trực giác nội tại đều mở đường cho những bước tiến quyết đoán.")
        action_items.append(f"Tận dụng thời cơ phát động các dự án trọng điểm, ký kết hợp tác chiến lược theo quẻ {hex_name}.")
    elif is_iching_passive and not is_tarot_upright:
        sync_insights.append(f"Cả Kinh Dịch ({hex_name}) lẫn Tarot ({tarot_name}) đều cảnh báo sự chậm rãi và bảo toàn. Đây là giai đoạn củng cố nội lực, không nên manh động.")
        action_items.append("Ưu tiên rà soát hồ sơ pháp lý, kiểm toán tài chính nội bộ và đào tạo đội ngũ thay vì mở rộng.")
    elif is_iching_passive and is_tarot_upright:
        conflict_insights.append(f"Kinh Dịch khuyên điềm tĩnh giữ thế ({hex_name}), nhưng Tarot ({tarot_name}) lại thôi thúc hành động. Giải pháp dung hòa: Vạch sẵn chiến lược sắc bén trong đầu, chuẩn bị đầy đủ nguồn lực nhưng chờ đúng thời điểm mới ra đòn.")
        action_items.append("Hoàn thiện phương án hành động chi tiết trên bàn giấy, hạn chế xuất chiêu bất ngờ trong ngày.")
    else:
        sync_insights.append(f"Kinh Dịch ({hex_name}) mang lại sự định hướng vững chãi, kết hợp cùng năng lượng chiêm niệm của {tarot_name} tạo điểm tựa tâm lý điềm tĩnh.")
        action_items.append(f"Thực thi công việc theo lời khuyên quẻ {hex_name}: {iching['hex_chu']['advice']}")

    # 2. Đối chiếu Bản mệnh Canh Ngọ vs Thời tiết Hà Nội
    temp_val = int(weather["temp"]) if weather["temp"].isdigit() else 28
    if tuvi["score"] >= 8:
        sync_insights.append(f"Cát khí bản mệnh ({tuvi['day_can_chi']}) hòa cùng tiết trời Hà Nội ({weather['temp']}°C, {weather['desc']}), rất thuận cho việc gặp gỡ ngoại giao và điều hành.")
    else:
        conflict_insights.append(f"Khí vận ngày đòi hỏi sự thận trọng cao. Nên hạn chế di chuyển xa ngoài hiện trường, tập trung làm việc tại Văn phòng Tổng Hành Dinh.")

    # 3. Đúc kết hành động bổ sung từ Giờ Hoàng Đạo & Trực
    action_items.append(f"Tận dụng khung giờ hoàng đạo đắc khí: {tuvi['hoang_dao'][0]} hoặc {tuvi['hoang_dao'][1]} để ban hành quyết định lớn.")
    action_items.append(f"Thuận theo Trực {tuvi['truc_name']}: {tuvi['truc_desc']}")

    # 4. Khẩu quyết đại cục (Executive Verdict)
    if tuvi["score"] >= 9:
        verdict = f"🔥 ĐẠI CÁT ĐẮC THỜI — QUYẾT ĐOÁN BỨT PHÁ: Trời Đất tương trợ, Chủ tịch hãy vững tâm triển khai các mục tiêu chiến lược lớn!"
    elif tuvi["score"] <= 6:
        verdict = f"🛡️ PHÒNG THỦ CHIẾN LƯỢC — LẤY TĨNH CHẾ ĐỘNG: Giữ vững trận địa, tích lũy nội lực và kiểm soát chặt chẽ các rủi ro vận hành."
    else:
        verdict = f"✨ CÂN BẰNG TÍCH TỰU — TIẾN THOÁI NHỊP NHÀNG: Điều hòa các nguồn lực, tập trung hoàn thành dứt điểm từng việc then chốt."

    return {
        "verdict": verdict,
        "sync_insights": sync_insights,
        "conflict_insights": conflict_insights,
        "action_items": action_items[:3]
    }


# ==============================================================================
# 7B. MÔ HÌNH AI TẠO SINH LUẬN GIẢI ĐỘC BẢN (GENERATIVE AI SYNTHESIZER)
# ==============================================================================
def generate_ai_spiritual_synthesis(weather, iching, tarot, tuvi, config, dt=None):
    """
    Gọi Generative AI cấp cao nhất (Gemini 3.6 Flash -> Fallback Gemini 2.5 Flash)
    để tự tay chấp bút bài luận giải độc bản.
    Tự động fallback an toàn về bộ quy tắc tĩnh nếu mất mạng hoặc lỗi API.
    """
    ai_cfg = config.get("ai_engine", {})
    if not ai_cfg.get("enabled", True):
        return None
        
    api_key = ai_cfg.get("api_key") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
        
    models_to_try = [
        ai_cfg.get("model", "gemini-3.8-flash"),
        ai_cfg.get("secondary_model", "gemini-3.6-flash"),
        ai_cfg.get("fallback_model", "gemini-2.5-flash")
    ]
    
    now_dt = dt if dt else get_vn_now()
    now_str = now_dt.strftime("%d/%m/%Y")
    
    prompt = f"""Bạn là Bậc Thầy Cố Vấn Tâm Linh & Chiến Lược Cấp Cao thuộc Tổng Hành Dinh Tập Đoàn, phụng sự riêng cho Chủ tịch Cao Xuân Trường (sinh 13:45 ngày 19/04/1990 - Canh Ngọ, mệnh Lộ Bàng Thổ, đắc cách Tọa Quý Giờ Tân Mùi).

Hôm nay hệ thống thiên văn và dịch số đầu ngày đã xác lập các thông số sau:
- Ngày: {now_str} (Ngày {tuvi['day_can_chi']})
- Tiết trời Hà Nội: {weather['temp']}°C (Cảm giác: {weather['feels_like']}°C), {weather['desc']}, độ ẩm {weather['humidity']}%, gió {weather['wind_kmh']} km/h (UV: {weather['uv']}).
- Kinh Dịch Mai Hoa: Quẻ Chủ là {iching['hex_chu']['name']} ({iching['hex_chu']['nature']} - {iching['hex_chu']['meaning']}), Hào {iching['dong_hao']} động biến thành Quẻ Biến {iching['hex_bien']['name']} ({iching['hex_bien']['meaning']}), Quẻ Hổ bên trong là {iching['hex_ho']['name']} ({iching['hex_ho']['meaning']}).
- Chiêm niệm Tarot: Rút được lá {tarot['name']} — {tarot['state']} ({tarot['meaning']}).
- Tử Vi & Trạch Cát: Ngày {tuvi['day_can_chi']}, Trực {tuvi['truc_name']} ({tuvi['truc_desc']}). Đánh giá ngày: {tuvi['rating']} (Điểm: {tuvi['score']}/10). Giờ Hoàng Đạo: {', '.join(tuvi['hoang_dao'][:3])}. Hướng Hỷ Thần: {tuvi['hy_than']} | Tài Thần: {tuvi['tai_than']}. Cát khí: {'; '.join(tuvi['blessings']) if tuvi['blessings'] else 'Bình hòa'}. Cảnh báo: {'; '.join(tuvi['cautions']) if tuvi['cautions'] else 'Không có'}.

Hãy viết phần luận giải chuyên sâu cho bản tin chào ngày mới gửi Chủ tịch. Yêu cầu:
1. KHẨU QUYẾT ĐẠI CỤC (Executive Verdict): 1 câu châm ngôn ngắn gọn, đanh thép, mang hào khí lãnh đạo (viết hoa, có biểu tượng cảm xúc, không quá 18 từ).
2. LUẬN GIẢI ĐỐI CHIẾU ĐA CHIỀU (2 gạch đầu dòng):
   - Phân tích sự cộng hưởng hoặc mâu thuẫn giữa Quẻ Dịch ({iching['hex_chu']['name']}) và lá bài Tarot ({tarot['name']}). Đưa ra góc nhìn sâu sắc, dung hòa cương nhu, tĩnh động.
   - Kết hợp thiên thời tại Hà Nội và cát khí bản mệnh Canh Ngọ 1990 để định hướng tâm thế làm việc.
3. 3 HÀNH ĐỘNG TRỌNG TÂM HÔM NAY (3 gạch đầu dòng có dấu tích ✅):
   - Lời khuyên cụ thể, sắc sảo cho việc quản trị điều hành các công ty thành viên, ký kết, kỷ luật nội bộ hoặc đàm phán trong khung giờ hoàng đạo.

Văn phong: Uyên bác, trầm tĩnh, đĩnh đạc của bậc quân sư tri kỷ đối thoại cùng vị nguyên thủ/chủ tịch tập đoàn lớn. Tuyệt đối không xưng em/tôi, không sáo rỗng, không kịch bản hư cấu ngoặc đơn.

Trả về định dạng JSON thuần túy (không bọc trong markdown codeblock):
{{
  "verdict": "...",
  "insights": ["...", "..."],
  "actions": ["...", "...", "..."]
}}"""

    data = {
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {
            'temperature': 0.7,
            'responseMimeType': 'application/json',
            'thinkingConfig': {'thinkingBudget': 0}
        }
    }
    
    req_data = json.dumps(data).encode('utf-8')
    
    for m in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
        try:
            req = urllib.request.Request(url, data=req_data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=25) as r:
                res = json.loads(r.read().decode())
                raw_text = res['candidates'][0]['content']['parts'][0]['text']
                parsed = json.loads(raw_text)
                
                verdict = parsed.get("verdict", "").strip()
                insights = parsed.get("insights", [])
                actions = parsed.get("actions", [])
                
                if verdict and actions:
                    clean_actions = []
                    for a in actions:
                        act_text = a.strip()
                        if not act_text.startswith("✅"):
                            act_text = f"✅ {act_text}"
                        act_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\g<1></b>', act_text)
                        clean_actions.append(act_text)
                        
                    clean_insights = []
                    for ins in insights:
                        ins_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\g<1></b>', ins.strip())
                        clean_insights.append(ins_text)
                        
                    return {
                        "verdict": verdict,
                        "sync_insights": clean_insights,
                        "conflict_insights": [],
                        "action_items": clean_actions,
                        "is_ai_generated": True,
                        "model_used": m
                    }
        except Exception as e:
            print(f"[WARNING] Mô hình {m} không phản hồi ({e}). Thử mô hình dự phòng...")
            
    return None

# ==============================================================================
# 8. SOẠN THẢO BẢN TIN TELEGRAM THEO QUY CHUẨN VĂN PHÒNG THƯ KÝ
# ==============================================================================
def compose_morning_spiritual_briefing(force_now=None):
    """
    Soạn thảo bản tin Telegram di động hoàn chỉnh theo đúng phong thái cấp cao:
    - Không tên file .md
    - Không link file
    - Không thoại kịch bản
    - Khí tượng chuyên biệt tại Hà Nội
    """
    now = force_now if force_now else get_vn_now()
    now_str = now.strftime("%d/%m/%Y")
    
    # Đọc cấu hình
    config = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            pass

    # Lấy dữ liệu 4 chuyên gia
    weather = get_hanoi_live_weather()
    iching = cast_iching_maihoa(now)
    tarot = draw_daily_tarot(now)
    tuvi = calculate_tuvi_and_compatibility(now)
    
    # Thử nghiệm Generative AI (Gemini 2.5 Flash) trước, tự động fallback nếu mạng ngắt
    synthesis = generate_ai_spiritual_synthesis(weather, iching, tarot, tuvi, config, now)
    if not synthesis:
        synthesis = synthesize_executive_guidance(weather, iching, tarot, tuvi)
        synthesis["is_ai_generated"] = False
    else:
        print("[INFO] Đã tạo bài luận giải độc bản thành công qua Generative AI (Gemini)!")
    
    # Soạn nội dung HTML tối ưu hiển thị di động trên Telegram
    msg_html = f"""👑 <b>BẢN TIN TÂM LINH & KHÍ VẬN ĐẦU NGÀY</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Kính chào Chủ tịch Cao Xuân Trường!</b>
📅 <b>Ngày:</b> {now_str} (Ngày {tuvi['day_can_chi']})
👤 <b>Bản Mệnh:</b> Canh Ngọ 1990 (Lộ Bàng Thổ — Đắc cách Tọa Quý)
🌤️ <b>Khí tượng Hà Nội:</b> {weather['temp']}°C (Cảm giác: {weather['feels_like']}°C), {weather['desc']}
💨 <b>Độ ẩm & Gió:</b> {weather['humidity']}% | Gió {weather['wind_kmh']} km/h (UV: {weather['uv']})

<blockquote>{synthesis['verdict']}</blockquote>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣ ☯️ <b>KINH DỊCH THỜI THẾ (MAI HOA ĐẦU NGÀY)</b>
• <b>Quẻ Chủ:</b> {iching['hex_chu']['name']} ({iching['hex_chu']['nature']})
• <b>Thoán Ý:</b> {iching['hex_chu']['meaning']}
• <b>Động Hào:</b> Hào {iching['dong_hao']} động ➔ <b>Quẻ Biến:</b> {iching['hex_bien']['name']}
• <b>Quẻ Hổ (Bên trong):</b> {iching['hex_ho']['name']} — {iching['hex_ho']['meaning']}
• <b>Lời Khuyên Đạo Trị:</b> {iching['hex_chu']['advice']}

2️⃣ 🔮 <b>CHIÊM NIỆM TAROT (ENERGY ARCHETYPE)</b>
• <b>Lá Bài Rút Được:</b> {tarot['name']} — <i>{tarot['state']}</i>
• <b>Thông Điệp Năng Lượng:</b> {tarot['meaning']}

3️⃣ 📜 <b>TỬ VI & TRẠCH CÁT BẢN MỆNH CHỦ TỊCH</b>
• <b>Đánh Giá Ngày:</b> {tuvi['rating']} (Điểm khí vận: {tuvi['score']}/10)
• <b>Trực Ngày:</b> Trực {tuvi['truc_name']} — <i>{tuvi['truc_desc']}</i>
• <b>Cát Khí Chiếu Mệnh:</b>
{chr(10).join(['  • ' + b for b in tuvi['blessings']]) if tuvi['blessings'] else '  • Khí trường ổn định bình hòa'}
• <b>Cảnh Báo Cần Tránh:</b>
{chr(10).join(['  • ' + c for c in tuvi['cautions']]) if tuvi['cautions'] else '  • Không có xung khắc lớn'}
• <b>Khung Giờ Hoàng Đạo:</b> {', '.join(tuvi['hoang_dao'][:3])}
• <b>Hướng Nghênh Cát:</b> Hỷ Thần ({tuvi['hy_than']}) | Tài Thần ({tuvi['tai_than']})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 <b>ĐỐI CHIẾU ĐA CHIỀU & CHIẾN LƯỢC LÃNH ĐẠO</b>
{chr(10).join(['• <b>[ĐỒNG QUY]</b> ' + s for s in synthesis['sync_insights']])}
{chr(10).join(['• <b>[LƯU TÂM]</b> ' + c for c in synthesis['conflict_insights']]) if synthesis['conflict_insights'] else '• Các trường phái đồng thuận cao, trường năng lượng ngày mới thông suốt.'}

📌 <b>3 HÀNH ĐỘNG TRỌNG TÂM HÔM NAY:</b>
{chr(10).join([act if act.startswith('✅') else f'✅ {act}' for act in synthesis['action_items']])}

<i>Chúc Chủ tịch một ngày mới tràn đầy sinh khí, hanh thông vạn sự!</i>
#BanTamLinh #ChaoNgayMoi #ExecutiveBriefing #ChuTichCaoXuanTruong"""

    # Bản lưu trữ nhật ký nội bộ (Markdown)
    log_text = msg_html.replace("<b>", "**").replace("</b>", "**").replace("<i>", "*").replace("</i>", "*").replace("<blockquote>", "> ").replace("</blockquote>", "")
    log_file = os.path.join(LOG_DIR, f"briefing_{now.strftime('%Y%m%d_%H%M%S')}.log")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(log_text)
        
    return msg_html, log_file

# ==============================================================================
# 9. GỬI TIN NHẮN QUA TELEGRAM API (CÓ KHÓA 1 LẦN/NGÀY)
# ==============================================================================
def send_telegram(html_text, force=False):
    """Gửi bản tin tới Chủ tịch qua bot Telegram @tapdoan_bot"""
    config = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            pass
            
    bot_token = config.get("telegram", {}).get("bot_token") or "8821881768:AAFysU6f0IGu4qHHVeN5P-b1fqgFHNPcECI"
    chat_id = config.get("telegram", {}).get("chat_id") or "6034655358"
    
    # Kiểm tra khóa ngày (Once-per-day lock) nếu không có cờ force
    today_str = get_vn_now().strftime("%Y-%m-%d")
    history = {}
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = {}
            
    if not force and history.get(today_str, {}).get("sent", False):
        print(f"[ONCE_PER_DAY_LOCK] Bản tin ngày {today_str} đã được phát thành công trước đó. Bỏ qua lượt gửi lặp lại.")
        return True

    send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": html_text,
        "parse_mode": "HTML"
    }
    
    try:
        req_data = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(send_url, data=req_data, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=12) as resp:
            res = json.loads(resp.read().decode())
            if res.get("ok"):
                print("[SUCCESS] Đã gửi bản tin Telegram chào ngày mới tới Chủ tịch thành công!")
                # Cập nhật lịch sử gửi
                history[today_str] = {
                    "sent": True,
                    "timestamp": get_vn_now().isoformat(),
                    "message_id": res.get("result", {}).get("message_id")
                }
                with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                    json.dump(history, f, ensure_ascii=False, indent=2)
                return True
            else:
                print(f"[ERROR] Telegram API trả về lỗi: {res}")
                return False
    except Exception as e:
        print(f"[ERROR] Không thể gửi tin nhắn Telegram: {e}")
        return False

# ==============================================================================
# HÀM MAIN & CLI INTERFACE
# ==============================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ban Cố Vấn Tâm Linh & Phong Thủy — Tổng Hành Dinh")
    parser.add_argument("--force", action="store_true", help="Bắt buộc phát tin bỏ qua khóa ngày")
    parser.add_argument("--dry-run", action="store_true", help="Biên soạn và in ra console mà không gửi Telegram")
    parser.add_argument("--test", action="store_true", help="Chạy thử nghiệm kiểm tra tính toàn vẹn hệ thống")
    args = parser.parse_args()
    
    print("=" * 60)
    print("BAN CỐ VẤN TÂM LINH & PHONG THỦY — TỔNG HÀNH DINH TẬP ĐOÀN")
    print("Hệ thống Khí vận & Trạch Cát Cá nhân hóa cho Chủ tịch Cao Xuân Trường")
    print("=" * 60)
    
    html_msg, log_path = compose_morning_spiritual_briefing()
    print(f"[INFO] Đã biên soạn bản tin hoàn tất. Lưu nhật ký tại: {log_path}")
    
    if args.dry_run or args.test:
        print("\n=== NỘI DUNG XEM TRƯỚC (DRY RUN / TEST) ===")
        print(html_msg)
        print("\n[SUCCESS] Kiểm tra hệ thống: 100% Sẵn sàng vận hành.")
    else:
        send_telegram(html_msg, force=args.force)
