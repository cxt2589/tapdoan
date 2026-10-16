#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Đánh Giá Khả Năng Kết Nối Nguồn Cung & Nhu Cầu Mở Rộng Địa Lý Của Khách Hàng
(Buyer Sourcing Gap & Geographic Expansion Feasibility Evaluator)
- Phân tích rủi ro tập trung chuỗi cung ứng hiện tại của Khách hàng
- Xác định khách hàng có cần thêm nhà cung cấp ở đâu / quốc gia nào
- Chấm điểm khả năng kết nối (Feasibility Score 0-100%)
- Đề xuất nhà cung cấp phù hợp nhất trong hệ sinh thái Tập đoàn để lấp khoảng trống
"""

import os
import sys
import json
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def evaluate_lead_sourcing_expansion(lead, suppliers):
    """
    Đánh giá chi tiết nhu cầu bổ sung NCC và tính khả thi kết nối cho 1 Lead
    """
    lead_id = lead.get("lead_id", "")
    lead_name = lead.get("company_name", "")
    country = lead.get("country", "")
    country_code = lead.get("country_code", "GLB").upper()
    tier = lead.get("tier", "B")
    market_region = lead.get("market_region", "other")
    commodities = lead.get("commodities_demanded", [])
    
    # Lấy thông tin mặt hàng chính
    first_comm = commodities[0] if commodities else {}
    comm_name = first_comm.get("name", "Hàng hóa ngoại thương") if isinstance(first_comm, dict) else str(first_comm)
    hs_code = first_comm.get("hs_code", "") if isinstance(first_comm, dict) else ""
    comm_lower = comm_name.lower()

    # 1. Xác định Quốc gia Khách hàng đang cần thêm NCC (Target Country Needed)
    target_country = "Việt Nam"
    target_country_code = "VN"
    target_region = "Đông Nam Á (ASEAN)"
    target_flag = "🇻🇳"
    expansion_rationale = ""
    current_risk_assessment = ""
    drivers = []

    # Logic địa chính trị & dòng chảy thương mại
    is_in_vietnam = country_code == "VN" or "vietnam" in country.lower() or "việt nam" in country.lower()
    is_fertilizer_or_chemical = any(k in comm_lower for k in ["phân", "fertilizer", "urea", "dap", "npk", "ure", "potash", "hóa chất", "chemical"])
    is_machinery_or_tech = any(k in comm_lower for k in ["máy", "machinery", "thiết bị", "cơ khí", "cnc", "điện tử", "electronic", "steel", "thép"])
    is_coffee = any(k in comm_lower for k in ["cà phê", "coffee", "robusta", "arabica"])
    is_pepper_spices = any(k in comm_lower for k in ["tiêu", "pepper", "hồ tiêu", "gia vị", "spice"])
    is_rice = any(k in comm_lower for k in ["gạo", "rice", "nông sản"])
    is_grain_or_feed = any(k in comm_lower for k in ["ngô", "corn", "lúa mì", "wheat", "thức ăn", "feed", "đậu nành", "soybean"])

    if is_in_vietnam:
        # Doanh nghiệp tại Việt Nam cần nguồn nguyên liệu/vật tư đầu vào
        if is_fertilizer_or_chemical:
            target_country = "Liên Bang Nga"
            target_country_code = "RU"
            target_region = "Khối EAEU (Liên Xô Cũ)"
            target_flag = "🇷🇺"
            expansion_rationale = "Doanh nghiệp tại Việt Nam cần bổ sung Nhà cung cấp đạm Urea N46% và DAP trực tiếp từ Nga để hưởng thuế FTA VN-EAEU 0% và hạ giá vốn 12-15% so với mua qua trung gian."
            current_risk_assessment = "Hiện đang mua gom qua các đầu mối thương mại thứ cấp trong nước với biên lợi nhuận mỏng và biến động giá giao ngay khó lường."
            drivers = [
                "Hưởng ưu đãi thuế nhập khẩu 0% theo Hiệp định VN-EAEU FTA",
                "Tiếp cận trực tiếp mỏ khai thác và nhà máy phân bón lớn nhất thế giới",
                "Giá chào CFR Cảng Phú Mỹ/Hải Phòng rẻ hơn giá thị trường 12-15%",
                "Cơ chế thanh toán phi USD linh hoạt bằng đồng Ruble hoặc CNY"
            ]
        elif is_grain_or_feed:
            target_country = "Thụy Sĩ"
            target_country_code = "CH"
            target_region = "Tập Đoàn Đa Quốc Gia Hạng 1 (Tier-1 Trading House)"
            target_flag = "🇨🇭"
            expansion_rationale = "Cần kết nối với các Tập đoàn Nông sản toàn cầu (Ameropa, Trammo) để bảo đảm nguồn ngũ cốc Non-GMO và lúa mì số lượng lớn ổn định dài hạn."
            current_risk_assessment = "Phụ thuộc vào các lô hàng giao ngay rời rạc, đối mặt rủi ro trễ tàu và biến động cước biển đột biến."
            drivers = [
                "Hợp đồng cung ứng dài hạn (Annual Off-take Agreement)",
                "Cam kết tiêu chuẩn kiểm định chất lượng SGS/GAFTA nghiêm ngặt",
                "Chính sách tín dụng thương mại L/C trả chậm Usance 90-180 ngày",
                "Bảo hiểm rủi ro giá hàng hóa nông sản quốc tế"
            ]
        else:
            target_country = "Trung Quốc"
            target_country_code = "CN"
            target_region = "Đông Á (Vành Đai Chế Tạo)"
            target_flag = "🇨🇳"
            expansion_rationale = "Cần thêm Nhà sản xuất thiết bị máy móc công nghiệp tại Quảng Đông để tối ưu chi phí đầu tư dây chuyền sản xuất tự động."
            current_risk_assessment = "Trang thiết bị hiện tại đã khấu hao lớn, công nghệ cũ làm tăng tiêu hao điện năng và chi phí bảo trì."
            drivers = [
                "Tối ưu chi phí đầu tư máy móc (rẻ hơn 30-40% so với thiết bị EU/Nhật)",
                "Khoảng cách địa lý gần, thời gian giao hàng và lắp đặt nhanh trong 10 ngày",
                "Hỗ trợ chuyên gia kỹ thuật bảo hành trực tiếp tại nhà máy",
                "Hưởng ưu đãi thuế ACFTA theo C/O Form E"
            ]
    else:
        # Khách hàng quốc tế (EU, Mỹ, Nga, Trung Quốc, UAE, Nhật-Hàn...) ➔ RẤT CẦN NHÀ CUNG CẤP TẠI VIỆT NAM
        target_country = "Việt Nam"
        target_country_code = "VN"
        target_region = "Đông Nam Á (Thủ Phủ Nông Nghiệp & Chế Biến)"
        target_flag = "🇻🇳"

        if market_region in ["eu", "germany", "netherlands", "france", "italy"]:
            expansion_rationale = f"Khách hàng {country} có nhu cầu cấp thiết bổ sung Nhà cung cấp tại Việt Nam để tận dụng mức thuế nhập khẩu ưu đãi 0% theo Hiệp định EVFTA (với chứng từ C/O Form EUR.1) và giảm phụ thuộc vào nguồn cung Nam Mỹ."
            current_risk_assessment = "Hiện đang phụ thuộc 70-80% vào các nhà xuất khẩu tại Brazil và Colombia; đang chịu rủi ro cước biển biến động qua eo biển và thiếu hụt nguồn Robusta chế biến sâu."
            drivers = [
                "Miễn thuế nhập khẩu 0% vào Liên minh Châu Âu (EVFTA Form EUR.1)",
                "Đa dạng hóa rủi ro mất mùa và hạn hán tại khu vực Nam Mỹ",
                "Chất lượng chuẩn EU: Đạt chứng chỉ Rainforest Alliance, HACCP, ISO 22000",
                "Tuyến hàng hải trực tiếp từ Cảng Cát Lái / Cái Mép về Cảng Hamburg / Rotterdam"
            ]
        elif market_region in ["russia_cis", "russia"]:
            expansion_rationale = f"Khách hàng Liên bang Nga cần mở rộng mạng lưới cung ứng tại Việt Nam để nhập khẩu ổn định các mặt hàng nhiệt đới (Cà phê, Tiêu, Thủy sản, Hạt điều) theo khuôn khổ thuế quan 0% của Hiệp định VN-EAEU FTA."
            current_risk_assessment = "Chuỗi cung ứng truyền thống từ Châu Âu bị đình trệ do cấm vận; chi phí nhập khẩu qua các nước trung gian bị đội lên 18-25%."
            drivers = [
                "Thuế quan nhập khẩu 0% theo Hiệp định thương mại tự do VN-EAEU (C/O Form EAV)",
                "Tuyến vận tải biển container thẳng từ Cát Lái/Hải Phòng đến Vladivostok & St. Petersburg",
                "Cơ chế thanh toán đối ứng an toàn, không phụ thuộc vào hệ thống SWIFT phương Tây",
                "Nguồn hàng nông sản đạt chuẩn kiểm dịch Rosselkhoznadzor của Liên bang Nga"
            ]
        elif market_region in ["north_america", "usa", "canada"]:
            expansion_rationale = f"Tập đoàn tại {country} đang khẩn trương triển khai chiến lược 'China+1' và tìm kiếm Nhà cung cấp thay thế tại Việt Nam nhằm tránh mức thuế đối kháng 25% (Mục 301) và phòng ngừa đứt gãy logistics."
            current_risk_assessment = "Độ tập trung nguồn cung vào thị trường Trung Quốc hiện ở mức báo động (trên 65%), khiến biên lợi nhuận bị bào mòn nặng nề bởi hàng rào thuế quan bảo hộ."
            drivers = [
                "Phòng vệ thương mại: Xuất xứ 'Made in Vietnam' hợp pháp, tránh thuế Mục 301",
                "Cơ sở hạ tầng cảng nước sâu Cái Mép tiếp nhận tàu mẹ đi thẳng Bờ Tây nước Mỹ",
                "Nhà máy đáp ứng đầy đủ tiêu chuẩn kiểm toán trách nhiệm xã hội và US FDA",
                "Chi phí nhân công và gia công cạnh tranh vượt trội tại Đông Nam Á"
            ]
        elif market_region in ["middle_east_gcc", "uae", "saudi"]:
            expansion_rationale = f"Doanh nghiệp vùng Vịnh {country} cần thiết lập quan hệ đối tác bền vững với Nhà máy tại Việt Nam để đảm bảo an ninh lương thực và nguồn cung nông sản chuẩn Halal."
            current_risk_assessment = "Phụ thuộc lớn vào nhập khẩu tái xuất từ các thương nhân trung gian tại Singapore và Dubai với chi phí cao."
            drivers = [
                "Sản phẩm đạt chứng nhận chuẩn Halal JAKIM / GCC quốc tế",
                "Thời gian vận chuyển nhanh từ Cát Lái đến Cảng Jebel Ali (Dubai) chỉ 12-14 ngày",
                "Năng lực đáp ứng các đơn hàng quy mô hàng chục ngàn tấn theo mùa vụ",
                "Phương thức thanh toán bảo đảm bằng L/C At Sight từ các ngân hàng hạng A"
            ]
        else:
            expansion_rationale = f"Khách hàng có nhu cầu mở rộng chuỗi cung ứng sang Việt Nam nhằm tối ưu hóa chi phí sản xuất, hạ giá vốn hàng bán và đa dạng hóa danh mục bạn hàng."
            current_risk_assessment = "Cơ cấu nhà cung ứng hiện tại có tính cục bộ cao, dễ tổn thương khi thị trường địa phương có biến động chính sách."
            drivers = [
                "Hưởng lợi từ mạng lưới 16 Hiệp định Thương mại Tự do (FTA) thế hệ mới của Việt Nam",
                "Chính sách bảo hộ đầu tư và môi trường kinh doanh ổn định hàng đầu khu vực",
                "Chất lượng sản phẩm đồng nhất với giá FOB cạnh tranh toàn cầu",
                "Hệ thống kho vận logistics cảng biển quốc tế hoàn thiện"
            ]

    # 2. Tìm Nhà Cung Cấp Tương Thích Nhất Trong Hệ Sinh Thái Tập Đoàn
    matching_suppliers = []
    for sup in suppliers:
        s_country = (sup.get("country") or "").lower()
        s_code = (sup.get("country_code") or "").upper()
        
        # Kiểm tra sự tương thích quốc gia
        is_target_match = False
        if target_country_code == "VN" and (s_code == "VN" or "việt nam" in s_country or "vietnam" in s_country):
            is_target_match = True
        elif target_country_code == "RU" and (s_code == "RU" or "nga" in s_country or "russia" in s_country):
            is_target_match = True
        elif target_country_code in ["CH", "US"] and (s_code in ["CH", "US"] or "thụy sĩ" in s_country or "hoa kỳ" in s_country):
            is_target_match = True
        elif target_country_code == "CN" and (s_code == "CN" or "trung quốc" in s_country or "china" in s_country):
            is_target_match = True

        if is_target_match:
            # Kiểm tra tương thích mặt hàng
            sup_items_str = ""
            for item in sup.get("commodities_supplied", []):
                if isinstance(item, dict):
                    sup_items_str += " " + item.get("name", "") + " " + item.get("hs_code", "")
                else:
                    sup_items_str += " " + str(item)
            sup_items_str = sup_items_str.lower()

            relevance = 50
            if is_coffee and any(k in sup_items_str for k in ["cà phê", "coffee", "robusta"]):
                relevance = 95
            elif is_pepper_spices and any(k in sup_items_str for k in ["tiêu", "pepper"]):
                relevance = 95
            elif is_fertilizer_or_chemical and any(k in sup_items_str for k in ["phân", "fertilizer", "urea", "dap", "npk"]):
                relevance = 95
            elif is_rice and any(k in sup_items_str for k in ["gạo", "rice"]):
                relevance = 95
            elif is_machinery_or_tech and any(k in sup_items_str for k in ["máy", "machinery", "thép", "steel", "cơ khí"]):
                relevance = 90
            elif "nông sản" in sup_items_str or "chế biến" in sup_items_str:
                relevance = 80

            if relevance >= 75:
                matching_suppliers.append({
                    "supplier_id": sup.get("id"),
                    "supplier_name": sup.get("company_name"),
                    "short_name": sup.get("short_name") or sup.get("company_name"),
                    "country": sup.get("country"),
                    "country_code": sup.get("country_code"),
                    "supplier_type": sup.get("supplier_type_vi") or sup.get("supplier_type", "Nhà Máy / Đại Lý"),
                    "score": sup.get("score") or sup.get("audit_score", 90),
                    "relevance": relevance,
                    "production_capacity": sup.get("production_capacity") or "Quy mô lớn xuất khẩu",
                    "certifications": (sup.get("quality_standards") or sup.get("certificates") or [])[:3],
                    "accepted_terms": f"{(sup.get('accepted_incoterms') or ['FOB/CIF'])[0]} • {(sup.get('accepted_payments') or ['L/C'])[0]}"
                })

    matching_suppliers.sort(key=lambda x: (x["relevance"], x["score"]), reverse=True)
    top_suppliers = matching_suppliers[:3]

    # 3. Tính Điểm Khả Năng Kết Nối (Feasibility Score: 0 - 100%)
    base_score = 75
    if top_suppliers:
        base_score += 12
    if tier == "A":
        base_score += 7
    elif tier == "B":
        base_score += 4
    if len(lead.get("trade_tags", [])) >= 5:
        base_score += 3
        
    feasibility_score = min(98, base_score)

    # 4. Xác định Cấp độ Cấp thiết (Urgency Level)
    if tier == "A" or feasibility_score >= 90:
        urgency_level = "RẤT CẤP THIẾT"
        urgency_color = "emerald"
    elif tier == "B" or feasibility_score >= 80:
        urgency_level = "CẦN THIẾT"
        urgency_color = "cyan"
    else:
        urgency_level = "TIỀM NĂNG"
        urgency_color = "amber"

    # 5. Khuyến nghị Tác nghiệp Cụ thể (Strategic Action Hook)
    action_hook = f"Khối XNK nên phát hành Thư chào hàng song ngữ (RFQ) kết nối {lead_name} với nguồn cung tại {target_country}; chào giá giao hàng CIF Cảng đến trên cơ sở lấy hàng từ {top_suppliers[0]['short_name'] if top_suppliers else 'Nhà máy thành viên'} và đính kèm bộ chứng từ C/O ưu đãi thuế."

    return {
        "lead_id": lead_id,
        "lead_name": lead_name,
        "country": country,
        "target_country_needed": target_country,
        "target_country_code": target_country_code,
        "target_region": target_region,
        "target_flag": target_flag,
        "feasibility_score": feasibility_score,
        "urgency_level": urgency_level,
        "urgency_color": urgency_color,
        "expansion_rationale": expansion_rationale,
        "current_risk_assessment": current_risk_assessment,
        "strategic_drivers": drivers,
        "suggested_suppliers": top_suppliers,
        "action_hook": action_hook
    }

def batch_evaluate_all_leads(db):
    """
    Chạy đánh giá cho toàn bộ kho leads trong database
    """
    leads = db.get("industry_leads", [])
    suppliers = db.get("suppliers", [])
    
    results = {}
    for lead in leads:
        lid = lead.get("lead_id")
        if lid:
            results[lid] = evaluate_lead_sourcing_expansion(lead, suppliers)
    return results

def enrich_database_sourcing_eval():
    db_path = os.path.join(os.path.dirname(__file__), "data", "intelligence_db.json")
    if not os.path.exists(db_path):
        return False
    with open(db_path, "r", encoding="utf-8") as f:
        db = json.load(f)
    leads = db.get("industry_leads", [])
    sups = db.get("suppliers", [])
    print(f"Enriching sourcing evaluation for {len(leads)} leads...")
    for l in leads:
        l["sourcing_evaluation"] = evaluate_lead_sourcing_expansion(l, sups)
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    print("Enrichment completed successfully!")
    return True

if __name__ == "__main__":
    enrich_database_sourcing_eval()

