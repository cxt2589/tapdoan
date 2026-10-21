"""
TRADE MATCHER ENGINE (BÀN KHỚP GIAO DỊCH B2B TỰ ĐỘNG)
Ma Trận Đối Chiếu 6 Chiều Dữ Liệu Giữa Nhà Cung Cấp & Khách Hàng Thu Mua Quốc Tế
Tập đoàn Tổng Hành Dinh - Khối Xuất Nhập Khẩu (SUBSIDIARY-05) & Agency Digital
"""

import json
import os
import re
from datetime import datetime, timezone, timedelta

def normalize_text(text):
    if not text:
        return ""
    return str(text).strip().lower()

def extract_hs_digits(code):
    if not code:
        return ""
    return re.sub(r"[^\d]", "", str(code))

def parse_revenue_usd(val):
    if not val:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().upper()
    multiplier = 1.0
    if "B" in s:
        multiplier = 1_000_000_000.0
        s = s.replace("B", "")
    elif "M" in s:
        multiplier = 1_000_000.0
        s = s.replace("M", "")
    elif "K" in s:
        multiplier = 1_000.0
        s = s.replace("K", "")
    s = re.sub(r"[^\d.]", "", s)
    try:
        return float(s) * multiplier
    except:
        return 0.0

def score_hs_match(buyer_commodities, supplier_commodities):
    """
    Chiều 1: Mã HS & Đặc Tính Sản Phẩm (Trọng số 30%)
    - Khớp chính xác 6 số: 100 điểm
    - Khớp 4 số nhóm: 85 điểm
    - Khớp 2 số chương HS: 60 điểm
    - Lệch hoàn toàn: 0 điểm (Gatekeeper: Loại bỏ)
    """
    best_score = 0
    best_match_info = None

    b_items = buyer_commodities if isinstance(buyer_commodities, list) else []
    s_items = supplier_commodities if isinstance(supplier_commodities, list) else []

    if not b_items or not s_items:
        return 0, None, "Thiếu dữ liệu mặt hàng của một trong hai bên"

    for b in b_items:
        b_hs = extract_hs_digits(b.get("hs_code", ""))
        b_name = normalize_text(b.get("name", ""))
        for s in s_items:
            s_hs = extract_hs_digits(s.get("hs_code", ""))
            s_name = normalize_text(s.get("name", ""))

            score = 0
            match_type = "none"

            if len(b_hs) >= 6 and len(s_hs) >= 6 and b_hs[:6] == s_hs[:6]:
                score = 100
                match_type = "Trùng khớp chính xác 6 số HS (Subheading)"
            elif len(b_hs) >= 4 and len(s_hs) >= 4 and b_hs[:4] == s_hs[:4]:
                score = 85
                match_type = "Trùng khớp 4 số HS (Heading chung nhóm)"
            elif len(b_hs) >= 2 and len(s_hs) >= 2 and b_hs[:2] == s_hs[:2]:
                score = 65
                match_type = "Cùng Chương HS WCO (Chapter level)"
            elif any(w in s_name for w in b_name.split() if len(w) > 3) or any(w in b_name for w in s_name.split() if len(w) > 3):
                score = 50
                match_type = "Tương đồng tên danh mục hàng hóa"

            if score > best_score:
                best_score = score
                best_match_info = {
                    "buyer_hs": b.get("hs_code"),
                    "buyer_item": b.get("name"),
                    "supplier_hs": s.get("hs_code"),
                    "supplier_item": s.get("name"),
                    "match_type": match_type
                }

    if best_score == 0:
        return 0, None, "Không tìm thấy điểm chung về mã HS và mặt hàng"

    return best_score, best_match_info, best_match_info["match_type"]

def score_certifications(buyer_certs, supplier_certs, buyer_country_code=""):
    """
    Chiều 2: Tiêu Chuẩn & Chứng Chỉ Chất Lượng (Trọng số 20%)
    - Đầy đủ chứng chỉ yêu cầu: 100 điểm
    - Thiếu chứng chỉ bắt buộc vào thị trường ngặt nghèo (US: FDA; EU: CE/REACH/GlobalGAP): Gatekeeper Warning
    """
    b_certs = set(normalize_text(c) for c in (buyer_certs or []))
    s_certs = set(normalize_text(c) for c in (supplier_certs or []))

    if not b_certs:
        return 100, list(supplier_certs or []), [], False, "Khách hàng không yêu cầu chứng chỉ đặc thù"

    matched = []
    missing = []
    for c in b_certs:
        found = False
        for sc in s_certs:
            if c in sc or sc in c:
                matched.append(c)
                found = True
                break
        if not found:
            missing.append(c)

    ratio = len(matched) / len(b_certs) if b_certs else 1.0
    score = round(ratio * 100, 1)

    # Gatekeeper check
    is_gatekeeper_fail = False
    country = str(buyer_country_code).upper()
    if country in ["US", "USA"] and "fda" in missing:
        is_gatekeeper_fail = True
        reason = "Vi phạm Gatekeeper: Xuất khẩu thị trường Hoa Kỳ bắt buộc chứng chỉ FDA"
    elif country in ["DE", "FR", "NL", "IT", "ES"] and any("gap" in m or "iso" in m for m in missing) and ratio < 0.5:
        reason = f"Thị trường EU yêu cầu ngặt nghèo về chứng chỉ sinh thái; NCC còn thiếu: {', '.join(missing)}"
    else:
        reason = f"Đáp ứng {len(matched)}/{len(b_certs)} chứng chỉ yêu cầu"

    return score, matched, missing, is_gatekeeper_fail, reason

def score_capacity_moq(buyer_scale, buyer_import_cap, supplier_capacity, supplier_moq):
    """
    Chiều 3: Sản Lượng, Năng Lực & MOQ (Trọng số 15%)
    """
    score = 80
    details = "Quy mô cung cầu nằm trong biên độ tương thích"

    b_scale = normalize_text(buyer_scale)
    s_cap = normalize_text(supplier_capacity)

    if "tier-1" in b_scale or "mega" in b_scale or "tập đoàn" in b_scale:
        if "triệu" in s_cap or "nghìn tấn" in s_cap or "lớn" in s_cap or "toàn cầu" in s_cap:
            score = 100
            details = "Năng lực cung ứng của NCC đáp ứng hoàn hảo quy mô tập đoàn thu mua"
        else:
            score = 70
            details = "Quy mô Buyer lớn, NCC cần hợp tác cùng các đơn vị vệ tinh để gom đủ sản lượng"
    else:
        score = 90
        details = "Nhu cầu mua hàng vừa vặn với công suất sản xuất của nhà máy"

    return score, details

def score_payments(buyer_payments, supplier_payments):
    """
    Chiều 4: Điều Kiện Thanh Toán Quốc Tế (Trọng số 15%)
    - Trùng L/C At Sight hoặc T/T: 100 điểm
    - Có thể đàm phán Usance L/C thông qua Chiết khấu L/C ngân hàng: 75 điểm
    - Hoàn toàn xung đột: 30 điểm
    """
    b_pay = set(normalize_text(p) for p in (buyer_payments or []))
    s_pay = set(normalize_text(p) for p in (supplier_payments or []))

    if not b_pay or not s_pay:
        return 75, ["L/C At Sight (Đàm phán)"], "Cần mở vòng đàm phán phương thức thanh toán an toàn"

    # Giao thoa trực tiếp
    common = []
    for bp in b_pay:
        for sp in s_pay:
            if bp in sp or sp in bp or ("l/c" in bp and "l/c" in sp) or ("t/t" in bp and "t/t" in sp):
                common.append(bp)
                break

    if common:
        return 100, list(set(common)), f"Phương thức thanh toán đồng thuận cao: {', '.join(set(common))}"
    elif any("l/c" in p for p in b_pay) and any("l/c" in p for p in s_pay):
        return 85, ["L/C Tín dụng thư"], "Cả hai bên đều chấp nhận L/C, có thể chốt L/C At Sight"
    elif any("usance" in p for p in b_pay):
        return 70, ["Usance L/C kèm Tài trợ thương mại"], "Buyer cần trả chậm, Khối XNK có thể đứng ra tài trợ vốn hoặc chiết khấu L/C"
    else:
        return 40, [], "Lệch phương thức thanh toán, cần giải pháp bảo lãnh tín dụng ngân hàng"

def score_incoterms(buyer_incoterms, supplier_incoterms):
    """
    Chiều 5: Điều Kiện Giao Hàng & Incoterms (Trọng số 10%)
    - Trùng Incoterms: 100 điểm
    - Buyer mua CIF, NCC bán FOB: 85 điểm (Khối XNK làm dịch vụ vận chuyển & bảo hiểm tạo doanh thu!)
    - Khác biệt lớn: 60 điểm
    """
    b_inco = set(normalize_text(i) for i in (buyer_incoterms or []))
    s_inco = set(normalize_text(i) for i in (supplier_incoterms or []))

    if not b_inco or not s_inco:
        return 80, ["FOB / CIF"], "Incoterms linh hoạt theo hợp đồng ngoại thương"

    common = b_inco.intersection(s_inco)
    if common:
        return 100, list(common), f"Incoterms trùng khớp hoàn hảo: {', '.join(common)}"
    elif "cif" in b_inco and "fob" in s_inco:
        return 90, ["FOB -> CIF (Synergy XNK)"], "Cơ hội hiệp lực: NCC xuất xưởng FOB, Khối XNK đảm nhận cước tàu & bảo hiểm xuất CIF cho Buyer"
    elif "fob" in b_inco and "cif" in s_inco:
        return 85, ["Đàm phán FOB Cảng xuất"], "Chuyển giao Incoterms dễ dàng tại cảng bốc hàng"
    else:
        return 65, list(b_inco), "Cần chuyên viên Logistics của Khối XNK tư vấn lộ trình vận tải tối ưu"

def score_compliance(buyer_lead, supplier):
    """
    Chiều 6: Điểm Tín Nhiệm & An Toàn Pháp Lý (Trọng số 10%)
    - Cổng khóa tự động (Gatekeeper):
      + Supplier dính Doanh nghiệp ma rủi ro hóa đơn / VAT safety < 30%: 0 điểm (Khóa ngay!)
      + Supplier hoặc Buyer dính OFAC/Sanctions: 0 điểm (Khóa ngay!)
      + Buyer có dấu hiệu Scam (Tier C, Free email): 20 điểm
    """
    # 1. Supplier checks
    sup_risk = str(supplier.get("tax_risk_level", "")).upper()
    sup_vat = supplier.get("vat_refund_safety_percent", 90)
    sup_sanctions = str(supplier.get("sanctions_check", "")).upper()

    if "HIGH_RISK" in sup_risk or "NGUY HIỂM" in sup_risk or sup_vat < 30:
        return 0, True, "Khóa tự động: Nhà cung cấp có rủi ro hóa đơn ma / rủi ro thuế cao nghiêm trọng"

    if "SANCTIONED" in sup_sanctions or "OFAC_HIT" in sup_sanctions:
        return 0, True, "Khóa tự động: Nhà cung cấp nằm trong danh sách cấm vận quốc tế"

    # 2. Buyer checks
    b_tier = str(buyer_lead.get("tier", "")).upper()
    b_score = buyer_lead.get("lead_score", 70)

    if "TIER C" in b_tier or b_score < 40:
        return 30, False, "Buyer có điểm tín nhiệm thấp, chỉ giao dịch khi có cọc 100% hoặc L/C Irrevocable"

    # 3. Both safe
    sup_audit = supplier.get("audit_score", 85)
    avg_score = round((b_score + sup_audit) / 2, 1)
    return avg_score, False, "Hồ sơ pháp lý, lịch sử thông quan và xếp hạng tín nhiệm hai đầu an toàn tuyệt đối"

def evaluate_deal_match(buyer_lead, supplier):
    """
    Đánh giá toàn diện 1 cặp Buyer - Supplier theo Ma Trận 6 Chiều
    """
    # Chiều 1: HS & Hàng hóa (30%)
    d1_score, d1_match, d1_desc = score_hs_match(
        buyer_lead.get("commodities_demanded", []),
        supplier.get("commodities_supplied", [])
    )

    # Gatekeeper nếu hoàn toàn không liên quan ngành hàng
    if d1_score == 0:
        return None

    # Chiều 2: Chứng chỉ chất lượng (20%)
    d2_score, d2_matched, d2_missing, d2_gk, d2_desc = score_certifications(
        buyer_lead.get("certification_required", []),
        supplier.get("quality_standards", []),
        buyer_lead.get("country_code", "")
    )

    # Chiều 3: Sản lượng & MOQ (15%)
    d3_score, d3_desc = score_capacity_moq(
        buyer_lead.get("scale", ""),
        buyer_lead.get("annual_import_capacity", ""),
        supplier.get("production_capacity", ""),
        supplier.get("min_order_qty", "")
    )

    # Chiều 4: Thanh toán (15%)
    d4_score, d4_matched, d4_desc = score_payments(
        buyer_lead.get("payment_terms_accepted", []),
        supplier.get("accepted_payments", [])
    )

    # Chiều 5: Incoterms (10%)
    d5_score, d5_matched, d5_desc = score_incoterms(
        buyer_lead.get("preferred_incoterms", []),
        supplier.get("accepted_incoterms", [])
    )

    # Chiều 6: Tuân thủ pháp lý & Tín nhiệm (10%)
    d6_score, d6_gk, d6_desc = score_compliance(buyer_lead, supplier)

    # Tính điểm tổng thể có trọng số
    total_score = round(
        d1_score * 0.30 +
        d2_score * 0.20 +
        d3_score * 0.15 +
        d4_score * 0.15 +
        d5_score * 0.10 +
        d6_score * 0.10,
        1
    )

    is_disqualified = False
    disqualify_reason = ""
    if d6_gk:
        is_disqualified = True
        disqualify_reason = d6_desc
        total_score = 0
    elif d2_gk:
        is_disqualified = True
        disqualify_reason = d2_desc
        total_score = 0

    # Phân hạng
    if is_disqualified:
        tier = "DISQUALIFIED"
        tier_vi = "Bị Khóa (Rủi Ro Vi Phạm)"
        badge_color = "rose"
    elif total_score >= 85.0:
        tier = "DIAMOND"
        tier_vi = "Khớp Kim Cương (Xác Suất Chốt Rất Cao)"
        badge_color = "emerald"
    elif total_score >= 70.0:
        tier = "GOLD"
        tier_vi = "Khớp Tiềm Năng (Khả Quan)"
        badge_color = "amber"
    elif total_score >= 50.0:
        tier = "SILVER"
        tier_vi = "Khớp Một Phần (Cần Đàm Phán)"
        badge_color = "blue"
    else:
        tier = "BRONZE"
        tier_vi = "Tương Thích Thấp"
        badge_color = "slate"

    # Ước tính giá trị thương vụ
    deal_value_usd = 0
    buyer_rev = parse_revenue_usd(buyer_lead.get("annual_revenue_usd", 0))
    if buyer_rev > 0:
        deal_value_usd = round(min(buyer_rev * 0.005, 5000000.0), 0)
    else:
        deal_value_usd = 250000.0 # mặc định 1 lô hàng container tiêu chuẩn

    matched_commodity = d1_match.get("buyer_item", "Hàng hóa ngoại thương") if d1_match else "Hàng hóa"
    matched_hs = d1_match.get("buyer_hs", "") if d1_match else ""

    # Phân tích độ trùng khớp Thẻ Tag Quy Chuẩn Ngoại Thương (Trade Tags)
    b_tags = buyer_lead.get("trade_tags", [])
    s_tags = supplier.get("trade_tags", [])
    b_set = set(b_tags)
    s_set = set(s_tags)
    matched_tags = sorted(list(b_set.intersection(s_set)))
    missing_tags = sorted(list(b_set.difference(s_set)))
    tag_match_rate = round((len(matched_tags) / len(b_set) * 100) if b_set else 100.0, 1)

    return {
        "match_id": f"MATCH-{buyer_lead.get('lead_id')}-{supplier.get('id')}",
        "buyer_id": buyer_lead.get("lead_id"),
        "buyer_name": buyer_lead.get("company_name"),
        "buyer_country": buyer_lead.get("country"),
        "buyer_country_code": buyer_lead.get("country_code"),
        "buyer_tier": buyer_lead.get("tier"),
        "supplier_id": supplier.get("id"),
        "supplier_name": supplier.get("company_name"),
        "supplier_short_name": supplier.get("short_name") or supplier.get("company_name"),
        "supplier_country": supplier.get("country"),
        "supplier_country_code": supplier.get("country_code"),
        "supplier_type": supplier.get("supplier_type_vi") or supplier.get("supplier_type"),
        "matched_commodity": matched_commodity,
        "matched_hs": matched_hs,
        "deal_value_usd": deal_value_usd,
        "total_score": total_score,
        "tier": tier,
        "tier_vi": tier_vi,
        "badge_color": badge_color,
        "is_disqualified": is_disqualified,
        "disqualify_reason": disqualify_reason,
        "trade_tags": {
            "buyer_tags": b_tags,
            "supplier_tags": s_tags,
            "matched_tags": matched_tags,
            "missing_tags": missing_tags,
            "tag_match_rate": tag_match_rate
        },
        "matched_tags": matched_tags,
        "missing_tags": missing_tags,
        "tag_match_rate": tag_match_rate,
        "dimensions": {
            "d1_hs_and_specs": {
                "name": "Mã HS & Quy Cách Hàng Hóa",
                "weight": 30,
                "score": d1_score,
                "desc": d1_desc,
                "match_details": d1_match
            },
            "d2_quality_certifications": {
                "name": "Tiêu Chuẩn & Chứng Chỉ",
                "weight": 20,
                "score": d2_score,
                "desc": d2_desc,
                "matched_certs": d2_matched,
                "missing_certs": d2_missing
            },
            "d3_capacity_and_moq": {
                "name": "Năng Lực & MOQ",
                "weight": 15,
                "score": d3_score,
                "desc": d3_desc
            },
            "d4_payment_terms": {
                "name": "Phương Thức Thanh Toán",
                "weight": 15,
                "score": d4_score,
                "desc": d4_desc,
                "matched_methods": d4_matched
            },
            "d5_incoterms_logistics": {
                "name": "Incoterms & Vận Tải",
                "weight": 10,
                "score": d5_score,
                "desc": d5_desc,
                "matched_incoterms": d5_matched
            },
            "d6_compliance_and_risk": {
                "name": "Tín Nhiệm & Pháp Lý",
                "weight": 10,
                "score": d6_score,
                "desc": d6_desc
            }
        },
        "action_recommendation": f"Tạo Thư chào hàng RFQ đôi kết nối {buyer_lead.get('company_name')} ({buyer_lead.get('country')}) và {supplier.get('short_name') or supplier.get('company_name')}."
    }

def classify_deal_industry(match):
    """
    Phân loại ngành hàng chuẩn xác cho từng cặp giao dịch theo mã HS và tên hàng hóa
    """
    hs = str(match.get("matched_hs", "")).strip()
    item = normalize_text(match.get("matched_commodity", ""))
    
    # 1. Thép, Máy móc, Công nghiệp
    if hs.startswith(("72", "73", "84", "85", "87", "90")) or any(k in item for k in ["thép", "máy móc", "thiết bị", "steel", "machinery", "hrc"]):
        return "machinery_industrial", "⚙️ Máy Móc, Thép & Công Nghiệp"
    # 2. Thủy sản
    elif hs.startswith(("03", "1604", "1605")) or any(k in item for k in ["thủy sản", "tôm", "cá", "shrimp", "fish", "seafood", "vannamei"]):
        return "seafood", "🐟 Thủy Hải Sản"
    # 3. Nông sản & Lương thực
    elif hs.startswith(("09", "10", "12", "08", "07", "11", "17", "18", "19", "20", "21", "04")) or any(k in item for k in ["cà phê", "gạo", "tiêu", "điều", "nông sản", "coffee", "rice", "pepper", "cashew", "sữa", "milk"]):
        return "agri_food", "🌾 Nông Sản & Lương Thực"
    # 4. Phân bón & Hóa chất
    elif hs.startswith(("31", "28", "29", "38")) or any(k in item for k in ["phân bón", "npk", "ure", "fertilizer", "dap", "kali", "chemical"]):
        return "fertilizer_chemical", "🧪 Phân Bón & Hóa Chất"
    # 5. Gỗ, Cao su, Sinh khối, Vật liệu
    elif hs.startswith(("39", "40", "44", "47", "48")) or any(k in item for k in ["cao su", "gỗ", "viên nén", "nhựa", "rubber", "wood", "pellet", "plastic"]):
        return "wood_rubber", "🪵 Cao Su, Gỗ & Vật Liệu"
    else:
        return "general_trade", "🌐 Ngoại Thương Tổng Hợp"

def interleave_diverse_matches(matches, max_items=200):
    """
    Xen kẽ đa chiều các kết quả khớp lệnh (Round-robin Interleaving)
    Chống tình trạng dồn dập 10 dòng cùng một khách hàng hoặc cùng một nhà cung cấp
    """
    if not matches:
        return []
    
    # Nhóm theo (industry_key, supplier_id)
    grouped = {}
    for m in matches:
        ind_key, ind_name = classify_deal_industry(m)
        m["industry_cluster"] = ind_key
        m["industry_label"] = ind_name
        sup_id = m.get("supplier_id") or "UNKNOWN_SUP"
        group_key = f"{ind_key}::{sup_id}"
        grouped.setdefault(group_key, []).append(m)

    # Lấy lần lượt từng phần tử từ mỗi nhóm (Interleaving)
    interleaved = []
    keys = list(grouped.keys())
    # Sắp xếp các nhóm theo điểm cao nhất của nhóm để duy trì chất lượng
    keys.sort(key=lambda k: grouped[k][0]["total_score"], reverse=True)

    max_depth = max(len(v) for v in grouped.values()) if grouped else 0
    for depth in range(max_depth):
        for k in keys:
            if depth < len(grouped[k]):
                interleaved.append(grouped[k][depth])
                if len(interleaved) >= max_items:
                    break
        if len(interleaved) >= max_items:
            break

    return interleaved

def select_diversified_daily_deals(matches, target_date=None, count=4):
    """
    Thuật toán Tuyển chọn Bản Tin Khớp Lệnh Xoay Vòng Đa Ngành Hàng Ngày (06:30 AM):
    - Đảm bảo 100%: 3-4 thương vụ đề xuất thuộc 3-4 NGÀNH HÀNG KHÁC NHAU
    - Đảm bảo 100%: 3-4 NHÀ CUNG CẤP KHÁC NHAU & KHÁCH HÀNG KHÁC NHAU
    - Xoay tua theo ngày (Daily Deterministic Rotation Seed), không lặp lại quanh quẩn vài đối tác cũ
    """
    if target_date is None:
        target_date = datetime.now(timezone(timedelta(hours=7)))

    day_seed = target_date.year * 1000 + target_date.timetuple().tm_yday

    # Lọc danh sách ứng viên có điểm cao (Score >= 75.0, Diamond & High Gold)
    valid_matches = [m for m in matches if m.get("total_score", 0) >= 75.0 and not m.get("is_disqualified")]
    if len(valid_matches) < count:
        valid_matches = [m for m in matches if not m.get("is_disqualified")]

    # Phân loại theo ngành hàng
    by_industry = {}
    for m in valid_matches:
        ind_key, ind_name = classify_deal_industry(m)
        m_copy = dict(m)
        m_copy["industry_cluster"] = ind_key
        m_copy["industry_label"] = ind_name
        by_industry.setdefault(ind_key, []).append(m_copy)

    core_order = ["agri_food", "fertilizer_chemical", "seafood", "machinery_industrial", "wood_rubber", "general_trade"]
    # Xoay thứ tự ưu tiên ngành theo ngày
    shift = day_seed % len(core_order)
    rotated_order = core_order[shift:] + core_order[:shift]

    chosen = []
    used_suppliers = set()
    used_buyers = set()
    used_industries = set()

    # Vòng 1: Chọn mỗi ngành 1 deal tiêu biểu nhất của ngày hôm đó
    for ind in rotated_order:
        candidates = by_industry.get(ind, [])
        if not candidates:
            continue

        # Điểm xoay tua theo hạt giống ngày
        offset = (day_seed + len(chosen) * 3) % len(candidates)
        ordered_candidates = candidates[offset:] + candidates[:offset]

        for cand in ordered_candidates:
            s_id = cand.get("supplier_id")
            b_id = cand.get("buyer_id")
            if s_id not in used_suppliers and b_id not in used_buyers and ind not in used_industries:
                cand["daily_spotlight"] = True
                chosen.append(cand)
                used_suppliers.add(s_id)
                used_buyers.add(b_id)
                used_industries.add(ind)
                break
        if len(chosen) >= count:
            break

    # Vòng 2: Nếu chưa đủ count, bù thêm từ các deal chất lượng cao còn lại (vẫn giữ khác NCC và Buyer)
    if len(chosen) < count:
        for cand in valid_matches:
            s_id = cand.get("supplier_id")
            b_id = cand.get("buyer_id")
            if s_id not in used_suppliers and b_id not in used_buyers:
                cand_copy = dict(cand)
                ind_key, ind_name = classify_deal_industry(cand_copy)
                cand_copy["industry_cluster"] = ind_key
                cand_copy["industry_label"] = ind_name
                chosen.append(cand_copy)
                used_suppliers.add(s_id)
                used_buyers.add(b_id)
                if len(chosen) >= count:
                    break

    return chosen[:count]

def scan_all_matches(db, min_score=60.0, top_n=100, industry_filter=None, diversity=True):
    """
    Quét toàn bộ kho dữ liệu để tìm các cặp giao dịch khớp nhất
    Hỗ trợ chế độ diversity=True giúp xen kẽ đa dạng ngành và nhà cung cấp
    """
    leads = db.get("industry_leads", [])
    suppliers = db.get("suppliers", [])

    matches = []
    for lead in leads:
        if industry_filter and lead.get("industry_id") != industry_filter:
            continue
        for sup in suppliers:
            eval_res = evaluate_deal_match(lead, sup)
            if eval_res and eval_res["total_score"] >= min_score and not eval_res["is_disqualified"]:
                matches.append(eval_res)

    # Sắp xếp giảm dần theo điểm khớp
    matches.sort(key=lambda x: (x["total_score"], x["deal_value_usd"]), reverse=True)

    if diversity:
        interleaved = interleave_diverse_matches(matches, max_items=top_n)
        if len(interleaved) >= min(top_n, len(matches)):
            return interleaved

    return matches[:top_n]

def get_daily_matching_metrics(db, target_date=None):
    """
    Tính toán các chỉ số khớp giao dịch phục vụ báo cáo 06:30 sáng & Dashboard
    Tích hợp bộ tuyển chọn xoay tua đa ngành (select_diversified_daily_deals)
    """
    # Lấy danh sách khớp lệnh cơ sở (không interleaving để tính metrics chuẩn)
    all_raw = scan_all_matches(db, min_score=65.0, top_n=300, diversity=False)

    diamond_matches = [m for m in all_raw if m["tier"] == "DIAMOND"]
    gold_matches = [m for m in all_raw if m["tier"] == "GOLD"]
    silver_matches = [m for m in all_raw if m["tier"] == "SILVER"]

    # Phân bổ theo ngành hàng
    industry_counts = {}
    for m in all_raw:
        _, ind_name = classify_deal_industry(m)
        industry_counts[ind_name] = industry_counts.get(ind_name, 0) + 1

    total_pipeline_val = sum(m.get("deal_value_usd", 0) for m in diamond_matches + gold_matches)

    # Tuyển chọn 3-4 deal đa dạng xoay vòng cho ngày hôm nay
    diversified_deals = select_diversified_daily_deals(all_raw, target_date=target_date, count=4)
    # Nếu vì lý do nào đó không có đủ diversified deals, fallback về diamond_matches
    if not diversified_deals:
        diversified_deals = diamond_matches[:3]

    now_vn = target_date or datetime.now(timezone(timedelta(hours=7)))
    day_name = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"][now_vn.weekday()]
    daily_theme = f"{day_name}: Phân Bổ Đa Ngành & Luân Chuyển Đối Tác Toàn Cầu"

    return {
        "total_scanned_buyers": len(db.get("industry_leads", [])),
        "total_scanned_suppliers": len(db.get("suppliers", [])),
        "total_matches_found": len(all_raw),
        "diamond_count": len(diamond_matches),
        "gold_count": len(gold_matches),
        "silver_count": len(silver_matches),
        "total_pipeline_val_usd": total_pipeline_val,
        "industry_breakdown": industry_counts,
        "top_diamond_deals": diversified_deals,
        "raw_top_diamond": diamond_matches[:3],
        "daily_theme": daily_theme,
        "rotation_seed": now_vn.year * 1000 + now_vn.timetuple().tm_yday
    }
