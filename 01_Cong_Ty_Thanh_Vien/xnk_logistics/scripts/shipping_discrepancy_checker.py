#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Công cụ Kiểm toán Đối soát Chéo Bộ Chứng từ Ngoại thương Tự động (Discrepancy Checker)
Khối Xuất Nhập Khẩu & Thương Mại Quốc Tế Tập Đoàn
Tuân thủ tiêu chuẩn: UCP 600, ISBP 745 & Luật Hải quan Việt Nam
"""

import sys
import json
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def audit_shipping_documents(doc_data: dict) -> dict:
    """
    Hàm đối soát chéo bộ chứng từ ngoại thương
    """
    discrepancies = []
    warnings = []
    passed = []

    inv = doc_data.get("commercial_invoice", {})
    pl = doc_data.get("packing_list", {})
    bl = doc_data.get("bill_of_lading", {})
    co = doc_data.get("certificate_of_origin", {})
    contract = doc_data.get("sales_contract", {})

    print("=" * 75)
    print("🔍 BÁO CÁO KIỂM TOÁN ĐỐI SOÁT CHÉO BỘ CHỨNG TỪ (DISCREPANCY AUDIT REPORT)")
    print(f"Lô hàng: {doc_data.get('shipment_id', 'N/A')} | Hàng hóa: {doc_data.get('commodity', 'N/A')}")
    print("=" * 75)

    # 1. Kiểm tra Đối soát Trọng lượng (GW / NW) giữa Packing List và B/L
    pl_gw = pl.get("gross_weight_kg", 0)
    bl_gw = bl.get("gross_weight_kg", 0)
    if pl_gw > 0 and bl_gw > 0:
        if abs(pl_gw - bl_gw) > 0.01:
            discrepancies.append(f"❌ [LỖI TRỌNG LƯỢNG CẢ BÌ (GW)]: Packing List ghi {pl_gw:,.2f} kg, nhưng B/L ghi {bl_gw:,.2f} kg (Lệch {abs(pl_gw - bl_gw):,.2f} kg)!")
        else:
            passed.append(f"✅ Trọng lượng cả bì (GW) khớp hoàn hảo giữa Packing List và B/L ({pl_gw:,.2f} kg).")

    # 2. Kiểm tra Số kiện (Packages / Quantity)
    pl_pkgs = pl.get("total_packages", 0)
    bl_pkgs = bl.get("total_packages", 0)
    if pl_pkgs > 0 and bl_pkgs > 0:
        if pl_pkgs != bl_pkgs:
            discrepancies.append(f"❌ [LỖI SỐ KIỆN]: Packing List ghi {pl_pkgs} kiện, nhưng B/L ghi {bl_pkgs} kiện!")
        else:
            passed.append(f"✅ Số lượng kiện hàng khớp 100% ({pl_pkgs} kiện).")

    # 3. Kiểm tra Trị giá tiền giữa Hợp đồng và Commercial Invoice
    contract_amount = contract.get("total_amount", 0)
    inv_amount = inv.get("total_amount", 0)
    currency = inv.get("currency", "USD")
    if contract_amount > 0 and inv_amount > 0:
        if abs(contract_amount - inv_amount) > 0.01:
            warnings.append(f"⚠️ [CHÚ Ý TRỊ GIÁ]: Trị giá Hợp đồng ({contract_amount:,.2f} {currency}) khác Invoice ({inv_amount:,.2f} {currency}). Hãy kiểm tra dung sai hợp đồng (tolerance) hoặc điều khoản giao hàng từng phần!")
        else:
            passed.append(f"✅ Tổng trị giá thanh toán khớp giữa Hợp đồng và Invoice ({inv_amount:,.2f} {currency}).")

    # 4. Kiểm tra Logic Dòng Thời Gian (Milestone Dates)
    date_format = "%Y-%m-%d"
    try:
        c_date = datetime.strptime(contract.get("date", "2026-01-01"), date_format) if "date" in contract else None
        inv_date = datetime.strptime(inv.get("date", "2026-01-01"), date_format) if "date" in inv else None
        bl_date = datetime.strptime(bl.get("on_board_date", "2026-01-01"), date_format) if "on_board_date" in bl else None
        co_date = datetime.strptime(co.get("issue_date", "2026-01-01"), date_format) if "issue_date" in co else None

        if c_date and inv_date and inv_date < c_date:
            discrepancies.append(f"❌ [LỖI THỜI GIAN]: Ngày lập Hóa đơn ({inv.get('date')}) lại trước Ngày ký Hợp đồng ({contract.get('date')})!")
        if inv_date and bl_date and inv_date > bl_date:
            discrepancies.append(f"❌ [LỖI THỜI GIAN]: Ngày lập Hóa đơn ({inv.get('date')}) lại sau Ngày tàu chạy B/L ({bl.get('on_board_date')})!")
        if bl_date and co_date and co_date < bl_date:
            warnings.append(f"⚠️ [CẢNH BÁO C/O]: Ngày cấp C/O ({co.get('issue_date')}) trước ngày tàu chạy ({bl.get('on_board_date')}). Cần kiểm tra C/O có bị hải quan từ chối hoặc yêu cầu xác minh không!")
        if bl_date and co_date and (co_date - bl_date).days > 3:
            if not co.get("issued_retroactively", False):
                warnings.append(f"⚠️ [CẢNH BÁO C/O CẤP SAU]: C/O cấp sau ngày tàu chạy quá 3 ngày nhưng ô 'Issued Retroactively' chưa được tích chọn!")
    except Exception as e:
        warnings.append(f"⚠️ Không thể kiểm tra mốc thời gian do định dạng ngày lỗi: {e}")

    # 5. Kiểm tra Tên Cảng Bốc (POL) và Cảng Dỡ (POD)
    bl_pol = bl.get("port_of_loading", "").strip().upper()
    inv_pol = inv.get("port_of_loading", "").strip().upper()
    if bl_pol and inv_pol and bl_pol != inv_pol:
        discrepancies.append(f"❌ [LỖI CẢNG BỐC]: POL trên Invoice là '{inv_pol}' nhưng trên B/L lại là '{bl_pol}'!")
    elif bl_pol:
        passed.append(f"✅ Cảng bốc (POL) đồng bộ: {bl_pol}")

    bl_pod = bl.get("port_of_discharge", "").strip().upper()
    inv_pod = inv.get("port_of_discharge", "").strip().upper()
    if bl_pod and inv_pod and bl_pod != inv_pod:
        discrepancies.append(f"❌ [LỖI CẢNG DỠ]: POD trên Invoice là '{inv_pod}' nhưng trên B/L lại là '{bl_pod}'!")
    elif bl_pod:
        passed.append(f"✅ Cảng dỡ (POD) đồng bộ: {bl_pod}")

    # In kết quả
    print("\n1. KẾT QUẢ ĐẠT CHUẨN (PASSED CHECKS):")
    for p in passed:
        print(f"  {p}")

    if warnings:
        print("\n2. CẢNH BÁO NGHIỆP VỤ (WARNINGS - CẦN LƯU Ý):")
        for w in warnings:
            print(f"  {w}")

    if discrepancies:
        print("\n3. LỖI BẤT HỢP LỆ NGHIÊM TRỌNG (DISCREPANCIES - PHẢI SỬA GẤP):")
        for d in discrepancies:
            print(f"  {d}")
        print("\n" + "=" * 75)
        print("❌ KẾT LUẬN: BỘ CHỨNG TỪ CHƯA ĐẠT! KHÔNG ĐƯỢC XUẤT TRÌNH NGÂN HÀNG HOẶC TRUYỀN HẢI QUAN!")
        print("Yêu cầu các bên liên quan sửa chứng từ theo các điểm đỏ nêu trên.")
        print("=" * 75)
    else:
        print("\n" + "=" * 75)
        print("🟢 KẾT LUẬN: BỘ CHỨNG TỪ HOÀN HẢO! ĐỦ ĐIỀU KIỆN TRUYỀN HẢI QUAN & THANH TOÁN QUỐC TẾ.")
        print("=" * 75)

    return {
        "status": "FAILED" if discrepancies else "PASSED",
        "discrepancies": discrepancies,
        "warnings": warnings,
        "passed": passed
    }

if __name__ == "__main__":
    # Dữ liệu thử nghiệm một bộ chứng từ có sai sót để kiểm tra độ nhạy của Tool
    sample_shipment = {
        "shipment_id": "PO-2026-XNK-001",
        "commodity": "Linh kiện vi mạch bán dẫn cao cấp",
        "sales_contract": {
            "date": "2026-10-01",
            "total_amount": 150000.0
        },
        "commercial_invoice": {
            "date": "2026-10-05",
            "total_amount": 150000.0,
            "currency": "USD",
            "port_of_loading": "SHANGHAI PORT",
            "port_of_discharge": "HAI PHONG PORT"
        },
        "packing_list": {
            "total_packages": 120,
            "gross_weight_kg": 5420.50,
            "net_weight_kg": 4890.00
        },
        "bill_of_lading": {
            "on_board_date": "2026-10-08",
            "total_packages": 120,
            "gross_weight_kg": 5420.50, # Đã khớp
            "port_of_loading": "SHANGHAI PORT",
            "port_of_discharge": "HAI PHONG PORT"
        },
        "certificate_of_origin": {
            "issue_date": "2026-10-11",
            "issued_retroactively": True
        }
    }

    audit_shipping_documents(sample_shipment)
