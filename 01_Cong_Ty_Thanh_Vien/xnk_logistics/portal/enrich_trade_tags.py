#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script gán Thẻ Tag Quy Chuẩn Ngoại Thương (Trade Criteria Tagging)
- Chuẩn hóa các quy chuẩn kỹ thuật (Specs), tiêu chuẩn chất lượng (Certs), Incoterms và Thanh toán
- Tạo trường `trade_tags` cho cả 1,000 Khách Hàng (Demand Tags) và 20 Nhà Cung Cấp (Supply Tags)
"""

import os
import sys
import json
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "intelligence_db.json")

def generate_tags_for_lead(lead):
    tags = set()
    
    # 1. HS Tags
    for c in lead.get("commodities_demanded", []):
        hs = c.get("hs_code", "")
        clean_hs = re.sub(r'[^0-9]', '', hs)[:4]
        if clean_hs:
            tags.add(f"#HS_{clean_hs}")
            
        req = (c.get("quality_requirements") or "").lower()
        # Specs detection
        if "12.5" in req or "độ ẩm" in req or "moisture" in req:
            tags.add("#Moist_Max12.5%")
        if "s18" in req or "screen 18" in req or "sàng 18" in req:
            tags.add("#Screen_S18")
        if "s16" in req or "screen 16" in req or "sàng 16" in req:
            tags.add("#Screen_S16")
        if "46%" in req or "n46" in req or "đạm" in req or "ure" in req:
            tags.add("#Urea_N46%")
        if "hạt" in req or "granular" in req:
            tags.add("#Granular")
        if "viên" in req or "prilled" in req:
            tags.add("#Prilled")
        if "thịt trắng" in req or "white meat" in req:
            tags.add("#WhiteMeat")
        if "mạ băng" in req or "glazing" in req:
            tags.add("#Glazing_10-20%")
        if "lạnh" in req or "-20" in req or "reefer" in req:
            tags.add("#DeepFrozen_-20C")
        if "astm" in req or "thép" in req:
            tags.add("#ASTM_A500")
        if "mạ kẽm" in req or "galvanized" in req:
            tags.add("#Zinc_Z275")
        if "sinh khối" in req or "pellet" in req or "gỗ" in req:
            tags.add("#WoodPellet_6-8mm")
            tags.add("#Caloric_Min4200kcal")

    # 2. Certification Tags
    certs = lead.get("certification_required", [])
    country = (lead.get("country") or "").lower()
    
    for cert in certs:
        c_low = cert.lower()
        if "haccp" in c_low:
            tags.add("#HACCP")
        if "iso" in c_low or "22000" in c_low or "9001" in c_low:
            tags.add("#ISO22000")
        if "rainforest" in c_low or "4c" in c_low:
            tags.add("#Rainforest_Alliance")
        if "fda" in c_low or "united states" in country or "usa" in country:
            tags.add("#FDA_US")
        if "ce" in c_low:
            tags.add("#CE_Europe")
        if "reach" in c_low or "germany" in country or "europe" in country or "spain" in country or "netherlands" in country:
            tags.add("#REACH_EU")
        if "halal" in c_low or "saudi" in country or "uae" in country:
            tags.add("#Halal_JAKIM")
        if "globalgap" in c_low or "gap" in c_low:
            tags.add("#GlobalGAP")
        if "fsc" in c_low:
            tags.add("#FSC_100%")

    # 3. Incoterms Tags
    inco = (lead.get("preferred_incoterms") or "").upper()
    if "FOB" in inco:
        tags.add("#Inco_FOB")
        if "CÁT LÁI" in inco or "CAT LAI" in inco:
            tags.add("#Inco_FOB_CatLai")
        if "CÁI MÉP" in inco or "CAI MEP" in inco:
            tags.add("#Inco_FOB_CaiMep")
    if "CIF" in inco:
        tags.add("#Inco_CIF")
        if "HAMBURG" in inco:
            tags.add("#Inco_CIF_Hamburg")
        if "ROTTERDAM" in inco:
            tags.add("#Inco_CIF_Rotterdam")
        if "PETERSBURG" in inco:
            tags.add("#Inco_CIF_StPetersburg")
    if "CFR" in inco:
        tags.add("#Inco_CFR")

    # 4. Payment Tags
    pay = (lead.get("payment_terms_accepted") or "").upper()
    if "L/C" in pay or "LC" in pay or "LETTER OF CREDIT" in pay:
        if "SIGHT" in pay or "TRẢ NGAY" in pay:
            tags.add("#LC_AtSight")
        elif "USANCE" in pay or "TRẢ CHẬM" in pay or "90" in pay or "60" in pay:
            tags.add("#Usance_LC")
        else:
            tags.add("#LC_AtSight")
    if "T/T" in pay or "TT" in pay or "TELEGRAPHIC" in pay:
        tags.add("#TT_Deposit_30_70")
    if "CAD" in pay:
        tags.add("#CAD_Payment")

    return sorted(list(tags))

def generate_tags_for_supplier(sup):
    tags = set()
    
    # 1. HS & Commodities
    for c in sup.get("commodities_supplied", []):
        hs = c.get("hs_code", "")
        clean_hs = re.sub(r'[^0-9]', '', hs)[:4]
        if clean_hs:
            tags.add(f"#HS_{clean_hs}")
        c_name = (c.get("name") or "").lower()
        if "cà phê" in c_name or "coffee" in c_name:
            tags.add("#Moist_Max12.5%")
            tags.add("#Screen_S18")
            tags.add("#Screen_S16")
        if "phân bón" in c_name or "ure" in c_name or "urea" in c_name:
            tags.add("#Urea_N46%")
            tags.add("#Granular")
            tags.add("#Prilled")
        if "hồ tiêu" in c_name or "pepper" in c_name:
            tags.add("#Moist_Max12.5%")
            tags.add("#Clean_FAQ")
        if "cá tra" in c_name or "seafood" in c_name:
            tags.add("#WhiteMeat")
            tags.add("#Glazing_10-20%")
            tags.add("#DeepFrozen_-20C")
        if "thép" in c_name or "steel" in c_name:
            tags.add("#ASTM_A500")
            tags.add("#Zinc_Z275")
        if "viên nén" in c_name or "gỗ" in c_name or "pellet" in c_name:
            tags.add("#WoodPellet_6-8mm")
            tags.add("#Caloric_Min4200kcal")

    # 2. Certs
    certs = (sup.get("quality_standards") or []) + (sup.get("certificates") or [])
    country = (sup.get("country") or "").lower()
    
    for cert in certs:
        c_low = str(cert).lower()
        if "haccp" in c_low:
            tags.add("#HACCP")
        if "iso" in c_low or "22000" in c_low or "9001" in c_low:
            tags.add("#ISO22000")
            tags.add("#ISO9001")
        if "rainforest" in c_low or "4c" in c_low or "utz" in c_low:
            tags.add("#Rainforest_Alliance")
        if "fda" in c_low or "hoa kỳ" in country:
            tags.add("#FDA_US")
        if "ce" in c_low:
            tags.add("#CE_Europe")
        if "reach" in c_low:
            tags.add("#REACH_EU")
        if "halal" in c_low:
            tags.add("#Halal_JAKIM")
        if "globalgap" in c_low or "vietgap" in c_low or "gap" in c_low:
            tags.add("#GlobalGAP")
        if "fsc" in c_low:
            tags.add("#FSC_100%")

    # 3. Incoterms
    incos = sup.get("accepted_incoterms", [])
    for inco in incos:
        i_up = str(inco).upper()
        if "FOB" in i_up:
            tags.add("#Inco_FOB")
            if "CÁT LÁI" in i_up or "CAT LAI" in i_up:
                tags.add("#Inco_FOB_CatLai")
            if "CÁI MÉP" in i_up or "CAI MEP" in i_up:
                tags.add("#Inco_FOB_CaiMep")
        if "CIF" in i_up:
            tags.add("#Inco_CIF")
        if "CFR" in i_up:
            tags.add("#Inco_CFR")

    # 4. Payments
    payments = sup.get("accepted_payments", [])
    for pay in payments:
        p_up = str(pay).upper()
        if "L/C" in p_up or "LC" in p_up:
            tags.add("#LC_AtSight")
            if "USANCE" in p_up or "CHẬM" in p_up:
                tags.add("#Usance_LC")
        if "T/T" in p_up or "TT" in p_up:
            tags.add("#TT_Deposit_30_70")
        if "CAD" in p_up:
            tags.add("#CAD_Payment")

    return sorted(list(tags))

def run_enrichment():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)

    leads = db.get("industry_leads", [])
    suppliers = db.get("suppliers", [])

    for l in leads:
        l["trade_tags"] = generate_tags_for_lead(l)

    for s in suppliers:
        s["trade_tags"] = generate_tags_for_supplier(s)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    print(f"[SUCCESS] Tagged {len(leads)} leads and {len(suppliers)} suppliers with standardized trade tags!")
    print(f"Sample lead tags ({leads[0]['company_name']}): {leads[0]['trade_tags']}")
    print(f"Sample supplier tags ({suppliers[0]['company_name']}): {suppliers[0]['trade_tags']}")

if __name__ == "__main__":
    run_enrichment()
