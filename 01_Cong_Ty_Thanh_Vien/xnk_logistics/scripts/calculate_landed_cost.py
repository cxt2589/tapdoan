#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool Tính Toán Chi Phí Hàng Nhập Khẩu Về Kho (Landed Cost Calculator)
Khối Xuất Nhập Khẩu & Thương Mại Quốc Tế Tập Đoàn
"""

import sys

# Force UTF-8 stdout for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def calculate_landed_cost(
    product_name: str,
    quantity: float,
    unit: str,
    fob_unit_price_usd: float,
    ocean_freight_usd: float,
    insurance_usd: float,
    exchange_rate_vnd: float,
    import_tax_rate_percent: float,
    vat_rate_percent: float = 10.0,
    special_consumption_tax_percent: float = 0.0,
    local_charges_vnd: float = 3500000.0, # THC, D/O, CIC, CFS...
    customs_brokerage_vnd: float = 1500000.0,
    inland_trucking_vnd: float = 3000000.0
):
    print("=" * 70)
    print(f"🚢 BẢNG TÍNH TOÁN CHI PHÍ NHẬP KHẨU VỀ KHO (LANDED COST)")
    print(f"Hàng hóa: {product_name} | Số lượng: {quantity:,.2f} {unit}")
    print(f"Tỷ giá tính thuế (VND/USD): {exchange_rate_vnd:,.2f}")
    print("=" * 70)

    # 1. Trị giá FOB & CIF
    total_fob_usd = quantity * fob_unit_price_usd
    total_cif_usd = total_fob_usd + ocean_freight_usd + insurance_usd
    cif_vnd = total_cif_usd * exchange_rate_vnd

    print(f"\n1. TRỊ GIÁ HÀNG HÓA NGOẠI TỆ:")
    print(f"  - Tổng FOB (USD):       ${total_fob_usd:,.2f}")
    print(f"  - Cước vận chuyển (USD): ${ocean_freight_usd:,.2f}")
    print(f"  - Bảo hiểm quốc tế (USD): ${insurance_usd:,.2f}")
    print(f"  - Tổng trị giá CIF (USD): ${total_cif_usd:,.2f}")
    print(f"  - Trị giá tính thuế (VND): {cif_vnd:,.0f} VND")

    # 2. Thuế Nhập Khẩu
    import_tax_vnd = cif_vnd * (import_tax_rate_percent / 100.0)

    # 3. Thuế Tiêu Thụ Đặc Biệt (nếu có)
    sct_base_vnd = cif_vnd + import_tax_vnd
    sct_vnd = sct_base_vnd * (special_consumption_tax_percent / 100.0)

    # 4. Thuế Giá Trị Gia Tăng (VAT) hàng nhập khẩu
    vat_base_vnd = cif_vnd + import_tax_vnd + sct_vnd
    vat_vnd = vat_base_vnd * (vat_rate_percent / 100.0)

    total_taxes_vnd = import_tax_vnd + sct_vnd + vat_vnd

    print(f"\n2. NGHĨA VỤ THUẾ ĐỐI VỚI NGÂN SÁCH NHÀ NƯỚC:")
    print(f"  - Thuế Nhập khẩu ({import_tax_rate_percent}%):    {import_tax_vnd:,.0f} VND")
    if special_consumption_tax_percent > 0:
        print(f"  - Thuế TTĐB ({special_consumption_tax_percent}%):          {sct_vnd:,.0f} VND")
    print(f"  - Thuế GTGT/VAT ({vat_rate_percent}%):          {vat_vnd:,.0f} VND (Khấu trừ đầu vào)")
    print(f"  - TỔNG THUẾ PHẢI NỘP TRƯỚC THÔNG QUAN: {total_taxes_vnd:,.0f} VND")

    # 5. Chi phí Dịch vụ Logistics & Bến bãi nội địa
    total_local_fees_vnd = local_charges_vnd + customs_brokerage_vnd + inland_trucking_vnd
    print(f"\n3. CHI PHÍ LOGISTICS & THỦ TỤC NỘI ĐỊA:")
    print(f"  - Phụ phí cảng (Local Charges THC/DO...): {local_charges_vnd:,.0f} VND")
    print(f"  - Phí dịch vụ khai báo hải quan:          {customs_brokerage_vnd:,.0f} VND")
    print(f"  - Cước kéo container / Vận chuyển về kho: {inland_trucking_vnd:,.0f} VND")
    print(f"  - Tổng chi phí nội địa:                    {total_local_fees_vnd:,.0f} VND")

    # 6. Tổng Chi phí Cập kho (Landed Cost)
    # Lưu ý: VAT thường được khấu trừ nên giá vốn hàng hóa (COGS) thường không gồm VAT nếu DN kê khai theo pp khấu trừ
    cogs_total_vnd = cif_vnd + import_tax_vnd + sct_vnd + total_local_fees_vnd
    landed_cost_with_vat_vnd = cogs_total_vnd + vat_vnd

    unit_cost_vnd = cogs_total_vnd / quantity
    unit_cost_usd = unit_cost_vnd / exchange_rate_vnd

    print(f"\n" + "=" * 70)
    print(f"4. TỔNG KẾT GIÁ VỐN HÀNG HÓA VỀ ĐẾN KHO (LANDED COST):")
    print(f"  - TỔNG GIÁ VỐN NHẬP KHO (chưa VAT): {cogs_total_vnd:,.0f} VND (~ ${cogs_total_vnd / exchange_rate_vnd:,.2f} USD)")
    print(f"  - TỔNG DÒNG TIỀN CHI RA (gồm VAT):  {landed_cost_with_vat_vnd:,.0f} VND")
    print(f"  - ĐƠN GIÁ VỐN TRÊN MỖI ĐƠN VỊ:      {unit_cost_vnd:,.2f} VND / {unit} (~ ${unit_cost_usd:.2f})")
    print(f"  - TỶ LỆ ĐỘN CHI PHÍ (Markup):       {((unit_cost_usd / fob_unit_price_usd) - 1.0) * 100:.2f}% so với giá FOB ban đầu")
    print("=" * 70)

if __name__ == "__main__":
    # Ví dụ mẫu: Nhập khẩu 10 bộ máy móc công nghiệp từ Thượng Hải
    calculate_landed_cost(
        product_name="Hệ thống máy cắt Laser CNC tự động",
        quantity=10,
        unit="Bộ",
        fob_unit_price_usd=8500.0,
        ocean_freight_usd=1200.0,
        insurance_usd=150.0,
        exchange_rate_vnd=25450.0,
        import_tax_rate_percent=0.0, # Nhờ C/O Form E thuế NK về 0%
        vat_rate_percent=10.0,
        local_charges_vnd=4200000.0,
        customs_brokerage_vnd=1500000.0,
        inland_trucking_vnd=4500000.0
    )
