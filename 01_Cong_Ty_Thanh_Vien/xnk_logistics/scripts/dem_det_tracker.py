#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Công cụ Giám sát Thời hạn Lưu bãi & Lưu container (DEM/DET Alert System)
Khối Xuất Nhập Khẩu & Thương Mại Quốc Tế Tập Đoàn
"""

import sys
from datetime import datetime, date

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def track_dem_det(
    container_no: str,
    port_name: str,
    shipping_line: str,
    arrival_date_str: str, # YYYY-MM-DD
    free_days_combined: int = 14,
    daily_penalty_usd: float = 45.0,
    exchange_rate_vnd: float = 25450.0
):
    print("=" * 70)
    print("⏱️ HỆ THỐNG CẢNH BÁO THỜI HẠN LƯU BÃI & LƯU CONTAINER (DEM/DET)")
    print(f"Container: {container_no} | Cảng: {port_name} | Hãng tàu: {shipping_line}")
    print("=" * 70)

    arrival_date = datetime.strptime(arrival_date_str, "%Y-%m-%d").date()
    today = date.today()
    days_elapsed = (today - arrival_date).days

    remaining_free_days = free_days_combined - days_elapsed

    print(f"Ngày cập cảng (ATA):          {arrival_date.strftime('%d/%m/%Y')}")
    print(f"Ngày kiểm tra hiện tại:       {today.strftime('%d/%m/%Y')}")
    print(f"Tổng số ngày đã ở tại cảng:   {days_elapsed} ngày")
    print(f"Thời gian miễn phí (Free time): {free_days_combined} ngày")

    print("-" * 70)
    if remaining_free_days > 3:
        status = "🟢 AN TOÀN (SAFE)"
        advice = f"Còn {remaining_free_days} ngày miễn phí. Tiếp tục hoàn thiện thủ tục thông quan bình thường."
        penalty_vnd = 0
    elif 0 <= remaining_free_days <= 3:
        status = "🟡 CẢNH BÁO NÓNG (WARNING - EXPIRING SOON)"
        advice = f"CHÚ Ý: Chỉ còn {remaining_free_days} ngày miễn phí! Yêu cầu bộ phận hiện trường đẩy nhanh kiểm hóa và kéo cont trước ngày {(today + datetime.timedelta(days=remaining_free_days)).strftime('%d/%m/%Y')}!"
        penalty_vnd = 0
    else:
        overdue_days = abs(remaining_free_days)
        status = "🔴 BÁO ĐỘNG ĐỎ: ĐÃ QUÁ HẠN PHẠT TIỀN (OVERDUE)"
        penalty_usd = overdue_days * daily_penalty_usd
        penalty_vnd = penalty_usd * exchange_rate_vnd
        advice = f"KHẨN CẤP: Đã quá hạn {overdue_days} ngày! Đang phát sinh phạt hãng tàu ${penalty_usd:,.2f} USD (~ {penalty_vnd:,.0f} VND). Cần liên hệ hãng tàu gia hạn hoặc kéo vỏ gấp!"

    print(f"TRẠNG THÁI HIỆN TẠI: {status}")
    print(f"KHUYẾN NGHỊ ĐIỀU HÀNH: {advice}")
    if penalty_vnd > 0:
        print(f"SỐ TIỀN PHẠT ƯỚC TÍNH: {penalty_vnd:,.0f} VND")
    print("=" * 70)

if __name__ == "__main__":
    # Ví dụ kiểm tra container về cảng Hải Phòng ngày 10/10/2026
    track_dem_det(
        container_no="MSKU1234567 (40'HC)",
        port_name="Tân Cảng Đình Vũ (Hải Phòng)",
        shipping_line="Maersk Line",
        arrival_date_str="2026-10-10",
        free_days_combined=14,
        daily_penalty_usd=50.0
    )
