#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Công cụ Tra cứu Nhanh Quy tắc Xuất Xứ & Form C/O Ưu Đãi Thuế FTA
Khối Xuất Nhập Khẩu & Thương Mại Quốc Tế Tập Đoàn
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

FTA_DATABASE = {
    "TRUNG QUOC": {
        "fta_name": "Hiệp định Thương mại Tự do ASEAN - Trung Quốc (ACFTA)",
        "co_form": "Form E",
        "primary_rules": ["WO (Wholly Obtained)", "RVC >= 40%", "CTH (Chuyển đổi nhóm 4 số)"],
        "key_notes": "Yêu cầu kiểm tra chặt chẽ ô số 13 (Third Party Invoicing nếu bên bán khác nhà máy). Kiểm tra tính hợp lệ của chữ ký/con dấu điện tử trên cổng hải quan.",
        "tax_benefit": "Thuế suất ưu đãi đặc biệt phần lớn giảm về 0% đối với linh kiện, máy móc, nông sản, hóa chất."
    },
    "ASEAN": {
        "fta_name": "Hiệp định Thương mại Hàng hóa ASEAN (ATIGA)",
        "co_form": "Form D (hoặc Tự chứng nhận xuất xứ AWSC)",
        "primary_rules": ["RVC >= 40%", "CTH (Chuyển đổi nhóm 4 số)"],
        "key_notes": "Sử dụng C/O điện tử e-Form D thông qua Cơ chế một cửa quốc gia (NSW). 98% dòng thuế đã về 0%.",
        "tax_benefit": "Thuế suất ưu đãi đặc biệt 0% cho hầu hết mọi mặt hàng."
    },
    "CHAU AU": {
        "fta_name": "Hiệp định Thương mại Tự do Việt Nam - EU (EVFTA)",
        "co_form": "Form EUR.1 (cho lô hàng > 6,000 EUR nếu chưa có mã REX) hoặc Khai báo xuất xứ trên hóa đơn (REX code)",
        "primary_rules": ["Quy tắc cụ thể mặt hàng (PSR)", "Hàm lượng nguyên liệu không xuất xứ tối đa (MaxNOM)", "Công đoạn gia công cụ thể"],
        "key_notes": "Từ phía EU nhập về VN: Nhà xuất khẩu tự chứng nhận xuất xứ theo hệ thống REX nếu > 6,000 EUR.",
        "tax_benefit": "Lộ trình xóa bỏ 99% dòng thuế nhập khẩu trong vòng 7 - 10 năm."
    },
    "HAN QUOC": {
        "fta_name": "Hiệp định Thương mại Tự do Việt Nam - Hàn Quốc (VKFTA) & AKFTA",
        "co_form": "Form VK (hoặc Form AK)",
        "primary_rules": ["RVC >= 40%", "CTH", "CTC"],
        "key_notes": "Form VK thường có ưu đãi sâu hơn Form AK. Chấp nhận C/O điện tử có mã QR tra cứu trực tuyến.",
        "tax_benefit": "Cắt giảm thuế mạnh cho thiết bị điện tử, vải sợi, mỹ phẩm và phụ tùng ô tô."
    },
    "NHAT BAN": {
        "fta_name": "Hiệp định VJEPA & AJCEP",
        "co_form": "Form VJ (hoặc Form AJ)",
        "primary_rules": ["RVC >= 40%", "CTC", "PSR"],
        "key_notes": "Nên so sánh giữa biểu thuế VJEPA, AJCEP và CPTPP để chọn form C/O có thuế suất thấp nhất.",
        "tax_benefit": "Ưu đãi thuế suất 0% cho linh kiện cơ khí, máy móc, nguyên liệu công nghiệp."
    },
    "RCEP": {
        "fta_name": "Hiệp định Đối tác Kinh tế Toàn diện Khu vực (RCEP)",
        "co_form": "Form RCEP",
        "primary_rules": ["Quy tắc cộng gộp toàn khu vực RCEP 15 nước (ASEAN + TQ, HQ, NB, Úc, NZ)"],
        "key_notes": "Cực kỳ thuận lợi khi chuỗi cung ứng sử dụng nguyên phụ liệu luân chuyển qua nhiều nước thành viên.",
        "tax_benefit": "Xóa bỏ rào cản xuất xứ nhờ cơ chế cộng gộp linh hoạt nhất thế giới."
    }
}

def lookup_fta(country_keyword: str):
    kw = country_keyword.strip().upper()
    print("=" * 70)
    print(f"🔍 TRA CỨU QUY TẮC XUẤT XỨ & MẪU C/O ƯU ĐÃI THUẾ CHO THỊ TRƯỜNG: {country_keyword}")
    print("=" * 70)

    matched = None
    for k, v in FTA_DATABASE.items():
        if k in kw or kw in k:
            matched = v
            break

    if not matched:
        print(f"Chưa tìm thấy dữ liệu trực tiếp cho từ khóa: '{country_keyword}'.")
        print("Các thị trường hỗ trợ sẵn: Trung Quốc, ASEAN, Châu Âu (EU), Hàn Quốc, Nhật Bản, RCEP.")
        return

    print(f"Hiệp định áp dụng:   {matched['fta_name']}")
    print(f"Mẫu C/O yêu cầu:     {matched['co_form']}")
    print(f"Tiêu chí xuất xứ:    {', '.join(matched['primary_rules'])}")
    print(f"Lợi ích thuế quan:   {matched['tax_benefit']}")
    print(f"Lưu ý nghiệp vụ:     {matched['key_notes']}")
    print("=" * 70)

if __name__ == "__main__":
    market = sys.argv[1] if len(sys.argv) > 1 else "Trung Quoc"
    lookup_fta(market)
