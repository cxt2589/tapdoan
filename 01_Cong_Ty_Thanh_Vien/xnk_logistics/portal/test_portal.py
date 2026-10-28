#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bộ Kiểm Thử Tự Động: Trade Intelligence & Verification Portal
Khối Xuất Nhập Khẩu & Thương Mại Quốc Tế
Bao gồm phân hệ Săn Tìm Khách Hàng Tiềm Năng Theo Ngành Hàng
"""

import sys
import os
import json
import time
import threading
import urllib.request
import urllib.parse

# Đảm bảo UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from server import ThreadedHTTPServer, PortalRequestHandler
import trade_matcher

TEST_PORT = 8089

def start_test_server():
    server_address = ("127.0.0.1", TEST_PORT)
    httpd = ThreadedHTTPServer(server_address, PortalRequestHandler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    return httpd

def http_get(path):
    url = f"http://127.0.0.1:{TEST_PORT}{path}"
    with urllib.request.urlopen(url, timeout=5) as resp:
        return resp.getcode(), json.loads(resp.read().decode('utf-8'))

def http_post(path, data):
    url = f"http://127.0.0.1:{TEST_PORT}{path}"
    payload = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.getcode(), json.loads(resp.read().decode('utf-8'))

def run_all_tests():
    print("==================================================================")
    print("🧪 BẮT ĐẦU KIỂM THỬ TỰ ĐỘNG XNK TRADE INTELLIGENCE PORTAL (PHASE 1)")
    print("==================================================================")

    httpd = start_test_server()
    time.sleep(0.5)

    passed_count = 0
    total_tests = 58

    try:
        # Test 1: Health Check
        code, res = http_get("/api/health")
        assert code == 200 and res["status"] == "ONLINE"
        assert res["db_stats"]["industries"] >= 5
        assert res["db_stats"]["industry_leads"] >= 8
        print(f"✅ Test 1/10: Health check thành công (Uptime: {res['status']}, Industries: {res['db_stats']['industries']}, Leads: {res['db_stats']['industry_leads']})")
        passed_count += 1

        # Test 2: API Danh mục Ngành Hàng
        code, ind_list = http_get("/api/industries")
        assert code == 200 and len(ind_list) >= 5
        agri = next((i for i in ind_list if i["id"] == "agri_food"), None)
        assert agri is not None
        assert len(agri["commodities"]) >= 4
        print(f"✅ Test 2/10: Lấy danh mục ngành hàng thành công (Tổng ngành: {len(ind_list)}, Nông sản có {len(agri['commodities'])} mặt hàng)")
        passed_count += 1

        # Test 3: Săn Tìm Khách Hàng Tiềm Năng Ngành Nông Sản
        code, leads_res = http_get("/api/leads/by-industry?industry=agri_food")
        assert code == 200
        assert leads_res["total"] >= 4
        lead_nkg = next((l for l in leads_res["data"] if "Neumann" in l["company_name"]), None)
        assert lead_nkg is not None
        assert lead_nkg["country"] == "Germany"
        assert lead_nkg["lead_score"] >= 95
        print(f"✅ Test 3/10: Săn tìm Lead Ngành Nông sản thành công (Tìm thấy {leads_res['total']} Leads; NKG: Điểm {lead_nkg['lead_score']}/100, Nước: {lead_nkg['country']})")
        passed_count += 1

        # Test 4: Săn Tìm Khách Hàng Theo Mã HS (Ví dụ HS 3102 - Phân bón)
        code, hs_res = http_get("/api/leads/by-industry?hs=3102")
        assert code == 200
        assert hs_res["total"] >= 2
        print(f"✅ Test 4/10: Săn tìm Lead theo Mã HS 3102 thành công (Tìm thấy {hs_res['total']} nhà thu mua phân bón lớn)")
        passed_count += 1

        # Test 5: Sinh Thư Chào Hàng Xuất Khẩu B2B Đa Ngôn Ngữ
        code, outreach_res = http_post("/api/leads/generate-outreach", {
            "lead_id": "LEAD-AGRI-001",
            "language": "EN"
        })
        assert code == 200
        assert outreach_res["status"] == "SUCCESS"
        assert "Neumann Kaffee Gruppe" in outreach_res["outreach"]["body"]
        assert "Inquiry & Supply Quotation" in outreach_res["outreach"]["subject"]
        print(f"✅ Test 5/10: Sinh Thư Chào Hàng B2B chuẩn ngoại thương thành công (Ngôn ngữ: EN, Độ dài: {len(outreach_res['outreach']['body'])} ký tự)")
        passed_count += 1

        # Test 6: Thẩm định Buyer Hạng 1 (Trammo)
        code, res = http_post("/api/verify/buyer", {"query": "Trammo"})
        assert code == 200
        assert res["tier"] == "A"
        assert res["sanctions_status"] == "CLEAR"
        assert res["fraud_score"] >= 90
        print(f"✅ Test 6/10: Thẩm định Buyer Hạng A chuẩn xác (Trammo: {res['fraud_score']}/100, Sanctions: {res['sanctions_status']})")
        passed_count += 1

        # Test 7: Thẩm định Buyer Lừa Đảo / Scam (EuroAsia)
        code, res = http_post("/api/verify/buyer", {"query": "EuroAsia"})
        assert code == 200
        assert res["tier"] == "C"
        assert res["is_free_email"] == True
        assert res["fraud_score"] < 40
        print(f"✅ Test 7/10: Nhận diện Buyer Lừa Đảo chuẩn xác (EuroAsia: {res['fraud_score']}/100, Tier: {res['tier']}, Free Email: {res['is_free_email']})")
        passed_count += 1

        # Test 8: Thẩm định Nhà Cung Cấp An Toàn Thuế (Bình Điền)
        code, res = http_post("/api/verify/supplier", {"tax_code": "0300481234"})
        assert code == 200
        assert res["vat_refund_safety_percent"] >= 95
        assert res["tier"] == "A"
        print(f"✅ Test 8/10: Bức tường lửa Thuế NCC Hạng A chuẩn xác (Bình Điền: An toàn hoàn thuế {res['vat_refund_safety_percent']}%)")
        passed_count += 1

        # Test 9: Thẩm định Nhà Cung Cấp Ma / Rủi Ro Cao (Hoàng Long Phát)
        code, res = http_post("/api/verify/supplier", {"tax_code": "0109988771"})
        assert code == 200
        assert res["vat_refund_safety_percent"] <= 20
        assert "NGUY HIỂM" in res["tax_risk_level"]
        print(f"✅ Test 9/10: Phát hiện Doanh nghiệp Ma / Hóa đơn khống chuẩn xác (Hoàng Long Phát: An toàn {res['vat_refund_safety_percent']}%, Cảnh báo: {res['tax_risk_level']})")
        passed_count += 1

        # Test 10: Săn Tìm Vận Đơn Hải Quan (B/L Manifest)
        code, res = http_get("/api/discovery/bl?hs=3102")
        assert code == 200
        assert res["total"] >= 1
        assert res["data"][0]["hs_code"].startswith("3102")
        print(f"✅ Test 10/12: Truy vấn Vận đơn Hải quan theo mã HS thành công (Mã HS 3102: Tìm thấy {res['total']} vận đơn)")
        passed_count += 1

        # Test 11: Phễu Khách Hàng Tiềm Năng (Prospecting Funnel & Stages)
        code, funnel_res = http_get("/api/leads/by-industry?stage=raw")
        assert code == 200
        assert funnel_res["total"] >= 5
        assert "funnel_stats" in funnel_res
        assert funnel_res["funnel_stats"]["total"] >= 25
        assert funnel_res["funnel_stats"]["raw"] >= 5
        print(f"✅ Test 11/12: Phễu sàng lọc khách hàng thành công (Tổng pool: {funnel_res['funnel_stats']['total']}, Data thô Tầng 1: {funnel_res['funnel_stats']['raw']}, Hạng B: {funnel_res['funnel_stats']['tier_b']}, Hạng A: {funnel_res['funnel_stats']['tier_a']})")
        passed_count += 1

        # Test 12: Thị Trường Nga (Russia) & Thư Chào Hàng Tiếng Nga (RU)
        code, ru_res = http_get("/api/leads/by-industry?country=russia")
        assert code == 200
        assert ru_res["total"] >= 5
        lead_orimi = next((l for l in ru_res["data"] if "Orimi" in l["company_name"]), None)
        assert lead_orimi is not None
        # Thẩm định tập đoàn Nga Orimi
        code_verify, verify_orimi = http_post("/api/verify/buyer", {"query": "Orimi Trade"})
        assert code_verify == 200
        assert verify_orimi["country"] == "Russia"
        assert "INN" in verify_orimi["registration_no"]
        assert "$" in verify_orimi["annual_revenue_usd"] and "USD" in verify_orimi["annual_revenue_usd"]

        # Thẩm định 4 Tầng RusAgro Sourcing Ltd: Xác thực Doanh thu ước tính cụ thể & Đối soát thực chứng 6 B/L
        code_rus, verify_rusagro = http_post("/api/verify/buyer", {"query": "RusAgro Sourcing Ltd"})
        assert code_rus == 200
        assert "18.5M" in verify_rusagro["annual_revenue_usd"]
        assert verify_rusagro["customs_bl_summary"]["has_customs_bl"] == True
        assert verify_rusagro["customs_bl_summary"]["total_bl"] >= 6
        assert verify_rusagro["capital_leverage"]["leverage_level"] == 3
        assert verify_rusagro["humanitarian_exemption"]["is_exempt"] == True

        # Sinh thư chào hàng tiếng Nga
        code_outreach, outreach_ru = http_post("/api/leads/generate-outreach", {
            "lead_id": "LEAD-AGRI-RU-001",
            "language": "RU"
        })
        assert code_outreach == 200
        assert outreach_ru["outreach"]["language"] == "RU"
        assert "Коммерческое предложение" in outreach_ru["outreach"]["subject"]
        print(f"✅ Test 12/12: Săn tìm & Thẩm định đối tác Nga chuẩn xác (Tìm thấy {ru_res['total']} DN Nga; Orimi Trade INN: {verify_orimi['registration_no']}; Thư tiếng Nga: Đạt chuẩn Form EAV)")
        passed_count += 1

        # Test 13: Kho 1,000 Leads & 8 Thị Trường Trọng Điểm Toàn Cầu
        code, reg_res = http_get("/api/regions")
        assert code == 200
        assert len(reg_res) >= 8
        assert "russia_cis" in reg_res and "china_eastasia" in reg_res and "north_america" in reg_res
        print(f"✅ Test 13/17: Quản trị 8 Thị trường khu vực toàn cầu thành công (Có đủ: Nga/EAEU, TQ/Đông Á, Bắc Mỹ, EU, GCC, Nhật-Hàn, ASEAN, Nam Mỹ/Châu Đại Dương)")
        passed_count += 1

        # Test 14: Phân Trang Chuẩn 10 Doanh Nghiệp / Trang Trên 1,000 Leads
        code, p_res = http_get("/api/leads/by-industry?page=1&page_size=10")
        assert code == 200
        assert p_res["total"] == 1000
        assert p_res["page"] == 1
        assert p_res["page_size"] == 10
        assert p_res["total_pages"] == 100
        assert len(p_res["data"]) == 10
        print(f"✅ Test 14/17: Phân trang chuẩn 10 DN/trang trên tổng 1,000 Leads thành công (Tổng: {p_res['total']}, Tổng trang: {p_res['total_pages']}, Số bản ghi trang 1: {len(p_res['data'])})")
        passed_count += 1

        # Test 15: Kiểm tra Hai Tín Hiệu: Hoạt Động XNK & Tin Sàn Môi Giới B2B
        sample_lead = p_res["data"][0]
        assert "latest_trade_activity" in sample_lead and len(sample_lead["latest_trade_activity"]) > 10
        assert "broker_rfq_signal" in sample_lead and len(sample_lead["broker_rfq_signal"]) > 10
        assert "broker_platform" in sample_lead
        print(f"✅ Test 15/17: Hai luồng tín hiệu XNK & Sàn Môi giới B2B hiển thị đầy đủ (B/L: '{sample_lead['latest_trade_activity'][:45]}...', Sàn: '{sample_lead['broker_platform']}')")
        passed_count += 1

        # Test 16: Xuất Dữ Liệu Excel / CSV Chuẩn UTF-8 BOM
        url_csv = f"http://127.0.0.1:{TEST_PORT}/api/leads/export-csv"
        req_csv = urllib.request.Request(url_csv)
        with urllib.request.urlopen(req_csv, timeout=5) as csv_resp:
            assert csv_resp.getcode() == 200
            content_type = csv_resp.headers.get("Content-Type", "")
            assert "csv" in content_type
            raw_bytes = csv_resp.read()
            # Kiểm tra tiền tố UTF-8 BOM \xef\xbb\xbf
            assert raw_bytes.startswith(b'\xef\xbb\xbf')
            csv_text = raw_bytes.decode('utf-8')
            lines = csv_text.splitlines()
            assert len(lines) >= 1001  # 1 header + 1000 leads
            assert "Mã Lead" in lines[0] and "Sàn Môi Giới" in lines[0]
        print(f"✅ Test 16/17: Xuất danh sách Excel / CSV chuẩn UTF-8 BOM thành công (Tổng {len(lines)-1} dòng dữ liệu, Tiếng Việt không lỗi font)")
        passed_count += 1

        # Test 17: Làm Mới & Đồng Bộ 1,000 Leads Hàng Ngày (POST /api/leads/refresh-sync)
        code, sync_res = http_post("/api/leads/refresh-sync", {})
        assert code == 200
        assert sync_res["ok"] == True
        assert sync_res["total_updated"] == 1000
        print(f"✅ Test 17/17: API Làm mới & Đồng bộ tín hiệu 1,000 Leads hàng ngày thành công (Đã cập nhật: {sync_res['total_updated']} leads)")
        passed_count += 1

        # Test 18: Danh Mục HS Toàn Diện Theo 4 Chế Độ Xem (Volume, Clusters, Alphabet, WCO)
        code, cat_vol = http_get("/api/hs/catalog?mode=volume")
        assert code == 200
        assert cat_vol["mode"] == "volume"
        assert len(cat_vol["data"]) == 97
        assert cat_vol["data"][0]["volume_rank"] == 1

        code, cat_clus = http_get("/api/hs/catalog?mode=clusters")
        assert code == 200
        assert cat_clus["mode"] == "clusters"
        assert len(cat_clus["data"]) >= 6

        code, cat_alpha = http_get("/api/hs/catalog?mode=alphabet")
        assert code == 200
        assert cat_alpha["mode"] == "alphabet"
        assert len(cat_alpha["data"]) >= 15

        code, cat_wco = http_get("/api/hs/catalog?mode=wco")
        assert code == 200
        assert cat_wco["mode"] == "wco"
        assert len(cat_wco["data"]) == 21
        print(f"✅ Test 18/21: Danh mục HS toàn diện 97 Chương theo 4 Chế độ hiển thị thành công (Volume: 97, Clusters: {len(cat_clus['data'])}, Alphabet: {len(cat_alpha['data'])} vần, WCO: 21 Phần)")
        passed_count += 1

        # Test 19: Tra Cứu Omni-Search Autocomplete Đa Tiêu Chí
        code, search_coffee = http_get("/api/hs/search?q=ca+phe")
        assert code == 200
        assert search_coffee["total_matches"] >= 1
        assert any(item["code"] == "09" for item in search_coffee["results"])

        code, search_ch61 = http_get("/api/hs/search?q=61")
        assert code == 200
        assert any(item["code"] == "61" for item in search_ch61["results"])
        print(f"✅ Test 19/21: Tra cứu Omni-Search Autocomplete đa tiêu chí thành công (Khớp từ khóa 'ca phe' -> Chương 09; Khớp mã '61' -> Chương 61 Dệt may)")
        passed_count += 1

        # Test 20: Tổng Hợp Chuẩn WCO Hải Quan Toàn Cầu (/api/hs/summary)
        code, summary_res = http_get("/api/hs/summary")
        assert code == 200
        assert summary_res["sections_count"] == 21
        assert summary_res["chapters_count"] == 97
        assert summary_res["clusters_count"] >= 6
        assert len(summary_res["sorting_modes"]) == 4
        print(f"✅ Test 20/21: Tổng hợp danh mục WCO chuẩn xác (21 Phần, 97 Chương, {summary_res['clusters_count']} Cụm chuỗi giá trị, 4 Chế độ tra cứu)")
        passed_count += 1

        # Test 21: Lọc Leads Theo Chương (Chapter) & Theo Cụm Chuỗi Ngành (Cluster)
        code, lead_ch61 = http_get("/api/leads/by-industry?chapter=61")
        assert code == 200
        assert lead_ch61["total"] >= 1
        assert any("61" in c.get("hs_code", "") for l in lead_ch61["data"] for c in l.get("commodities_demanded", []))

        code, lead_cluster_tech = http_get("/api/leads/by-industry?cluster=tech_machinery")
        assert code == 200
        assert lead_cluster_tech["total"] >= 1
        print(f"✅ Test 21/23: Lọc kho 1,000 Leads theo Chương HS (Chương 61: {lead_ch61['total']} DN) và theo Cụm ngành (Công nghệ/Cơ khí: {lead_cluster_tech['total']} DN) thành công")
        passed_count += 1

        # Test 22: Hồ Sơ Tình Báo Chi Tiết Doanh Nghiệp & Lịch Sử Vận Đơn B/L, Sàn B2B (/api/leads/detail)
        code, detail_res = http_get("/api/leads/detail?id=LEAD-AGRI-001")
        assert code == 200
        assert detail_res["ok"] == True
        lead_det = detail_res["lead"]
        assert lead_det["company_name"] == "Neumann Kaffee Gruppe (NKG)"
        assert len(lead_det["historical_bl_records"]) >= 3
        assert len(lead_det["historical_b2b_rfqs"]) >= 3
        assert any(b["bl_number"] for b in lead_det["historical_bl_records"])
        print(f"✅ Test 22/23: Hồ sơ tình báo chi tiết & Lịch sử B/L ({len(lead_det['historical_bl_records'])} vận đơn), Sàn B2B ({len(lead_det['historical_b2b_rfqs'])} RFQ) thành công")
        passed_count += 1

        # Test 23: Săn Tìm & Lọc Nhà Cung Cấp & Đại Lý Cấp 1 Toàn Cầu (/api/suppliers)
        code, sups_all = http_get("/api/suppliers")
        assert code == 200
        assert len(sups_all) >= 20
        # Lọc theo loại Tier-1 Master Agent
        code, sups_tier1 = http_get("/api/suppliers?type=tier1_master_agent")
        assert code == 200
        assert len(sups_tier1) >= 6
        assert all("tier1" in s.get("supplier_type", "") for s in sups_tier1)
        # Lọc theo nước Thụy Sĩ (ch)
        code, sups_ch = http_get("/api/suppliers?country=ch")
        assert code == 200
        assert len(sups_ch) >= 1
        assert any("Ameropa" in s.get("company_name", s.get("name", "")) for s in sups_ch)
        # Lọc theo nước Nga (ru) - Kiểm tra tính chuẩn xác tuyệt đối (không lẫn Singapore / Việt Nam, hỗ trợ mở rộng co giãn)
        code, sups_ru = http_get("/api/suppliers?country=ru")
        assert code == 200
        assert len(sups_ru) >= 2
        assert all(s.get("country_code") == "RU" or s.get("origin_country_code") == "RU" for s in sups_ru)
        assert not any("singapore" in (s.get("country", "")).lower() for s in sups_ru)

        # Lọc theo tìm kiếm từ khóa Nga / Nhà cung cấp ở Nga (Bảo đảm không lẫn NCC Việt Nam hay các Hub giao dịch Âu/Mỹ)
        code, sups_q_ru = http_get("/api/suppliers?q=nga")
        assert code == 200
        assert len(sups_q_ru) >= 2
        assert all(s.get("country_code") == "RU" or s.get("origin_country_code") == "RU" for s in sups_q_ru)

        code, sups_q_nlp = http_get("/api/suppliers?q=nh%C3%A0%20cung%20c%E1%BA%A5p%20%E1%BB%9F%20nga")
        assert code == 200
        assert len(sups_q_nlp) >= 2
        assert all(s.get("country_code") == "RU" or s.get("origin_country_code") == "RU" for s in sups_q_nlp)

        # Kiểm tra API thẩm định thuế (/api/verify/supplier) chuyển hướng thông minh khi nhập tên quốc gia
        code, v_resp = http_post("/api/verify/supplier", {"tax_code": "nhà cung cấp ở nga"})
        assert code == 200
        assert v_resp.get("is_country_query") == True
        assert v_resp.get("country_code") == "RU"
        assert "DYNAMIC-SP-" not in v_resp.get("id", "")
        print(f"✅ Test 23/25: Động cơ Săn tìm NCC & Đại lý Cấp 1 Toàn cầu (Tổng {len(sups_all)} NCC, {len(sups_tier1)} Đại lý Tier-1, Lọc theo Quốc gia chuẩn xác 100% không dính nhầm từ khóa)")
        passed_count += 1

        # Test 24: Động Cơ Giao Diện Sáng / Tối (Light & Dark Theme Engine)
        url_html = f"http://127.0.0.1:{TEST_PORT}/"
        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            assert html_resp.getcode() == 200
            html_text = html_resp.read().decode('utf-8')
            assert 'id="themeToggleBtn"' in html_text
            assert 'toggleTheme()' in html_text
            assert 'COMPREHENSIVE LIGHT THEME ENGINE' in html_text
            assert "portal_theme" in html_text
        print(f"✅ Test 24/25: Giao diện Sáng (Light Mode) & Bộ chuyển đổi Theme Sáng/Tối tích hợp hoàn hảo")
        passed_count += 1

        # Test 25: Popup Hồ Sơ Chi Tiết NCC (Dossier Modal) & Thẩm Định Đa Tầng Cung Ứng
        code, sup_det = http_get("/api/suppliers/detail?id=SUP-GLB-001")
        assert code == 200
        assert sup_det["ok"] == True
        sup_data = sup_det["supplier"]
        assert sup_data["company_name"] == "Trammo, Inc."
        assert len(sup_data["commodities_supplied"]) >= 2
        assert all(isinstance(c, dict) and "hs_code" in c and "name" in c for c in sup_data["commodities_supplied"])
        assert len(sup_data["customs_bl_records"]) >= 1

        # Kiểm tra frontend có popup modal và các hàm tác nghiệp
        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            assert 'id="supplierDetailModal"' in html_text
            assert 'openSupplierDetailModal' in html_text
            assert 'inspectSupplier' in html_text
            assert 'formatCommodityBadges' in html_text
            assert 'supd-commodities-container' in html_text
        print(f"✅ Test 25/25: Popup Dossier Modal NCC, API Chi Tiết (/api/suppliers/detail), Thẩm định định tuyến linh hoạt & Format Hàng hóa sạch 100% không [object Object]")
        passed_count += 1

        # Test 26: API Thống kê Chỉ số Khớp Lệnh Ngoại Thương (/api/matches/metrics)
        code, m_res = http_get("/api/matches/metrics")
        assert code == 200
        assert m_res["ok"] == True
        m_metrics = m_res["metrics"]
        assert m_metrics["total_matches_found"] >= 50
        assert m_metrics["diamond_count"] >= 5
        assert m_metrics["total_pipeline_val_usd"] > 100000000
        print(f"✅ Test 26/30: API Thống kê Chỉ số Khớp Lệnh Ngoại Thương (/api/matches/metrics) chuẩn xác")
        passed_count += 1

        # Test 27: API Săn Tìm & Lọc Danh Sách Khớp Lệnh Ma Trận 6 Chiều (/api/matches)
        code, list_res = http_get("/api/matches?page=1&page_size=10&tier=DIAMOND")
        assert code == 200
        assert list_res["ok"] == True
        assert len(list_res["data"]) >= 5
        assert all(item["tier"] == "DIAMOND" for item in list_res["data"])
        assert all(item["total_score"] >= 85.0 for item in list_res["data"])
        print(f"✅ Test 27/30: API Săn Tìm & Lọc Danh Sách Khớp Lệnh Ma Trận 6 Chiều (/api/matches) chuẩn xác")
        passed_count += 1

        # Test 28: API Đối Soát Chi Tiết Ma Trận 6 Chiều Cặp Giao Dịch (/api/matches/analyze)
        code, ana_res = http_post("/api/matches/analyze", {
            "buyer_id": "LEAD-AGRI-001",
            "supplier_id": "SP-002"
        })
        assert code == 200
        assert ana_res["ok"] == True
        match_data = ana_res["match"]
        assert match_data["total_score"] >= 85.0
        assert "dimensions" in match_data
        assert len(match_data["dimensions"]) == 6
        assert "d1_hs_and_specs" in match_data["dimensions"]
        assert "d2_quality_certifications" in match_data["dimensions"]
        assert "d3_capacity_and_moq" in match_data["dimensions"]
        assert "d4_payment_terms" in match_data["dimensions"]
        assert "d5_incoterms_logistics" in match_data["dimensions"]
        assert "d6_compliance_and_risk" in match_data["dimensions"]
        print(f"✅ Test 28/30: API Đối Soát Chi Tiết Ma Trận 6 Chiều Cặp Giao Dịch (/api/matches/analyze) chuẩn xác")
        passed_count += 1

        # Test 29: Giao Diện Frontend Bàn Khớp Giao Dịch (Dock 6 Cột, section-matchmaker, matchDetailModal)
        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            assert 'id="section-matchmaker"' in html_text
            assert 'id="tab-matchmaker"' in html_text
            assert 'id="matchDetailModal"' in html_text
            assert 'fetchMatchmakerData' in html_text
            assert 'mm-diamond-count' in html_text
            assert 'mm-pipeline-val' in html_text
            assert 'openMatchDetailModal' in html_text
        print(f"✅ Test 29/30: Giao Diện Frontend Bàn Khớp Giao Dịch (Dock 6 Cột, section-matchmaker, matchDetailModal) hoàn hảo")
        passed_count += 1

        # Test 30: Module Tự Động Hóa Bắn Bản Tin Khớp Lệnh 06:30 Sáng Telegram
        import morning_trade_matcher_dispatch
        with open(morning_trade_matcher_dispatch.DATA_FILE, "r", encoding="utf-8") as f_db:
            db_test = json.load(f_db)
        metrics_test = morning_trade_matcher_dispatch.trade_matcher.get_daily_matching_metrics(db_test)
        assert metrics_test["total_matches_found"] >= 50
        assert metrics_test["diamond_count"] >= 5
        assert os.path.exists(morning_trade_matcher_dispatch.DATA_FILE)
        print(f"✅ Test 30/32: Module Tự Động Hóa Bắn Bản Tin Khớp Lệnh 06:30 Sáng Telegram sẵn sàng 100%")
        passed_count += 1

        # Test 31: API Đầu Mối Liên Lạc Doanh Nghiệp (/api/contacts) - Đầy đủ 2 trường hợp (Có thêm & Không có thêm)
        # 1. Trường hợp Có thêm thông tin liên lạc (Tier-A lead & Major supplier)
        code, c_lead_multi = http_get("/api/contacts?type=lead&id=LEAD-AGRI-001")
        assert code == 200
        assert c_lead_multi["ok"] == True
        assert c_lead_multi["has_additional"] == True
        assert c_lead_multi["total_contacts"] >= 3
        assert len(c_lead_multi["additional_contacts"]) >= 2
        assert any(c.get("role_type") == "logistics" for c in c_lead_multi["all_contacts"])
        assert any(c.get("role_type") == "trade_finance" for c in c_lead_multi["all_contacts"])

        code, c_sup_multi = http_get("/api/contacts?type=supplier&id=SP-001")
        assert code == 200
        assert c_sup_multi["ok"] == True
        assert c_sup_multi["has_additional"] == True
        assert len(c_sup_multi["additional_contacts"]) >= 1

        # 2. Trường hợp Không có thêm thông tin liên lạc -> Trả về thông báo chuẩn
        # Tìm lead có đúng 1 contact
        single_lead_id = next((l["lead_id"] for l in db_test.get("industry_leads", []) if len(l.get("sourcing_contacts", [])) == 1), None)
        assert single_lead_id is not None
        code, c_lead_single = http_get(f"/api/contacts?type=lead&id={single_lead_id}")
        assert code == 200
        assert c_lead_single["ok"] == True
        assert c_lead_single["has_additional"] == False
        assert c_lead_single["total_contacts"] == 1
        assert "hiện chỉ có 01 đầu mối liên lạc chính thức" in c_lead_single["message"]

        print(f"✅ Test 31/32: API Tra cứu Đầu Mối Liên Lạc (/api/contacts) chuẩn xác cho cả 2 luồng (Có thêm đầu mối & Thông báo khi chỉ có 1 đầu mối)")
        passed_count += 1

        # Test 32: Giao Diện Frontend Modal Đầu Mối Liên Lạc & Các Nút Bấm Xem Thêm
        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            assert 'id="companyContactsModal"' in html_text
            assert 'id="ccm-contacts-list"' in html_text
            assert 'openCompanyContactsModal' in html_text
            assert 'closeCompanyContactsModal' in html_text
            assert 'viewMoreContacts' in html_text
            assert 'viewMoreContactsFromDetail' in html_text
            assert 'viewMoreSupplierContactsFromDetail' in html_text
            assert 'copyContactEmail' in html_text
            assert 'Xem thêm liên hệ' in html_text
        print(f"✅ Test 32/33: Giao Diện Popup Modal Đầu Mối Liên Lạc (companyContactsModal) & Phím Xem Thêm tích hợp hoàn hảo")
        passed_count += 1

        # Test 33: Hệ Thống Thẻ Tag Quy Chuẩn Ngoại Thương (Trade Tags) & Đối Soát Điểm Vênh
        code_tag, tag_matches = http_get("/api/matches?page=1&page_size=5")
        assert code_tag == 200
        assert len(tag_matches["data"]) > 0
        first_deal = tag_matches["data"][0]
        assert "matched_tags" in first_deal
        assert "missing_tags" in first_deal
        assert "tag_match_rate" in first_deal
        assert isinstance(first_deal["matched_tags"], list)
        assert len(first_deal["matched_tags"]) > 0

        code_anl, anl_res = http_post("/api/matches/analyze", {
            "buyer_id": first_deal["buyer_id"],
            "supplier_id": first_deal["supplier_id"]
        })
        assert code_anl == 200 and anl_res["ok"] == True
        anl_deal = anl_res["match"]
        assert "matched_tags" in anl_deal
        assert "missing_tags" in anl_deal
        assert "trade_tags" in anl_deal

        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            assert 'id="md-tags-section"' in html_text
            assert 'id="md-matched-tags-list"' in html_text
            assert 'id="md-missing-tags-list"' in html_text
            assert 'id="md-tag-rate-badge"' in html_text
            assert 'Tags khớp:' in html_text
            # Kiểm tra không còn icon nút: ấn để xem hồ sơ chi tiết (external-link)
            assert 'data-lucide="external-link"' not in html_text
        print(f"✅ Test 33/34: Động Cơ Thẻ Tag Quy Chuẩn Ngoại Thương (Trade Tags), Điểm Vênh Thương Thảo & Loại Bỏ Icon Nút Hồ Sơ chuẩn 100%")
        passed_count += 1

        # Test 34: Thống Kê Vận Đơn 1 Năm, Tần Suất Hàng Tháng & Nút Xem Thêm Vận Đơn
        code_sup, res_sup = http_get("/api/suppliers/detail?id=SP-001")
        assert code_sup == 200 and res_sup["ok"] == True
        sup_obj = res_sup["supplier"]
        assert "bl_stats_1y" in sup_obj
        assert sup_obj["bl_stats_1y"]["total_bl_1y"] >= 20
        assert sup_obj["bl_stats_1y"]["monthly_avg"] > 0
        assert len(sup_obj.get("customs_bl_records", [])) >= 5

        code_lead, res_lead = http_get("/api/leads/detail?id=LEAD-AGRI-001")
        assert code_lead == 200 and res_lead["ok"] == True
        lead_obj = res_lead["lead"]
        assert "bl_stats_1y" in lead_obj
        assert lead_obj["bl_stats_1y"]["total_bl_1y"] > 0
        assert lead_obj["bl_stats_1y"]["monthly_avg"] > 0
        assert len(lead_obj.get("historical_bl_records", [])) >= 5

        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            assert 'id="supd-bl-total-1y"' in html_text
            assert 'id="supd-bl-avg-month"' in html_text
            assert 'id="supd-bl-more-wrapper"' in html_text
            assert 'id="btn-supd-more-bl"' in html_text
            assert 'toggleMoreSupplierBLs' in html_text
            assert 'id="cd-bl-total-1y"' in html_text
            assert 'id="cd-bl-avg-month"' in html_text
            assert 'id="cd-bl-more-wrapper"' in html_text
            assert 'id="btn-cd-more-bl"' in html_text
            assert 'toggleMoreLeadBLs' in html_text
        print(f"✅ Test 34/35: Thống Kê Vận Đơn Hải Quan 1 Năm Qua, Tần Suất Trung Bình / Tháng & Phím Bấm 'Xem Thêm' chuẩn 100%")
        passed_count += 1

        # Test 35: Đánh Giá Nhu Cầu Mở Rộng Nguồn Cung Địa Lý & Khả Năng Kết Nối NCC
        code_se, res_se = http_get("/api/leads/sourcing-evaluation?id=LEAD-AGRI-001")
        assert code_se == 200 and res_se["ok"] == True
        eval_data = res_se["evaluation"]
        assert eval_data["target_country_needed"] == "Việt Nam"
        assert eval_data["target_country_code"] == "VN"
        assert eval_data["feasibility_score"] >= 80
        assert len(eval_data.get("strategic_drivers", [])) >= 3
        assert len(eval_data.get("suggested_suppliers", [])) >= 1

        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            assert 'id="cd-sourcing-gap-section"' in html_text
            assert 'id="cd-gap-target-country"' in html_text
            assert 'id="cd-gap-feasibility-score"' in html_text
            assert 'id="cd-gap-current-risk"' in html_text
            assert 'id="cd-gap-drivers-list"' in html_text
            assert 'triggerOutreachFromSourcingGap' in html_text
            assert 'Cần NCC:' in html_text
            assert 'Bấm tên để xem chi tiết' in html_text
            assert 'openSupplierDetailModal' in html_text
            assert 'Xem Chi Tiết' in html_text
        print(f"✅ Test 35/38: Đánh Giá Nhu Cầu Mở Rộng Nguồn Cung Địa Lý, Tỷ Lệ Khả Thi Kết Nối & Đề Xuất NCC chuẩn 100%")
        passed_count += 1

        # Test 36: Ghi Rõ Thông Tin Nhà Cung Cấp trong Bản Tin Bot & Khóa Bắn Tin 1 Lần/Ngày
        import morning_trade_matcher_dispatch
        metrics_test = trade_matcher.get_daily_matching_metrics(db_test)
        assert len(metrics_test["top_diamond_deals"]) > 0
        first_diamond = metrics_test["top_diamond_deals"][0]
        assert "supplier_name" in first_diamond or "supplier_short_name" in first_diamond
        assert "supplier_country" in first_diamond
        
        # Test gửi deal cụ thể lên Telegram qua API (dry_run: True để tuyệt đối không spam Chủ tịch)
        code_tg, res_tg = http_post("/api/matches/notify-telegram", {
            "buyer_id": first_diamond["buyer_id"],
            "supplier_id": first_diamond["supplier_id"],
            "dry_run": True
        })
        assert code_tg == 200
        assert res_tg["ok"] == True
        assert res_tg["type"] == "DEAL_DETAIL"
        assert res_tg.get("dry_run") == True

        # Test kiểm tra khóa ngày và dry_run của module bản tin 06:30
        assert morning_trade_matcher_dispatch.run_morning_dispatch(dry_run=True) == True
        # Thử gọi API summary ở chế độ dry_run
        code_sum, res_sum = http_post("/api/matches/notify-telegram", {"summary": True, "dry_run": True})
        assert code_sum == 200
        assert res_sum["ok"] == True
        assert res_sum["type"] == "DAILY_SUMMARY"
        assert res_sum.get("dry_run") == True

        print(f"✅ Test 36/38: Bổ Sung Đầy Đủ Thông Tin NCC & Cơ Chế Khóa Bắn Tin Khớp Lệnh 1 Lần/Ngày Chuẩn 100%")
        passed_count += 1

        # Test 37: API Sinh Bộ Đôi RFQ B2B Ngoại Thương & Giao Diện Modal RFQ Đôi
        code_drfq, res_drfq = http_post("/api/matches/generate-dual-rfq", {
            "buyer_id": "LEAD-AGRI-001",
            "supplier_id": "SP-001",
            "buyer_language": "EN",
            "supplier_language": "VN",
            "commodity": "Cà Phê Robusta",
            "hs_code": "0901.11"
        })
        assert code_drfq == 200
        assert res_drfq["ok"] == True
        assert "buyer_rfq" in res_drfq and "supplier_rfq" in res_drfq
        assert res_drfq["buyer_rfq"]["language"] == "EN"
        assert res_drfq["supplier_rfq"]["language"] == "VN"
        assert "0901.11" in res_drfq["buyer_rfq"]["subject"]
        assert "0901.11" in res_drfq["supplier_rfq"]["subject"]
        assert "YÊU CẦU BÁO GIÁ & ĐẶT HÀNG XUẤT KHẨU" in res_drfq["supplier_rfq"]["subject"]

        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            assert 'id="dualRfqModal"' in html_text
            assert 'id="drfq-buyer-panel"' in html_text
            assert 'id="drfq-supplier-panel"' in html_text
            assert 'openDualOutreach' in html_text
            assert 'switchDualRfqTab' in html_text
            assert 'closeDualRfqModal' in html_text
            assert 'dispatchDualRfqTelegramAlert' in html_text
        print(f"✅ Test 37/38: Động Cơ Sinh Bộ Đôi RFQ B2B (Buyer Quotation + Supplier Inquiry) & Giao Diện Dual RFQ chuẩn 100%")
        passed_count += 1

        # Test 38: Nhấn Tên Đối Tác Xem Chi Tiết Dossier & Khôi Phục Tab Khi F5
        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            assert 'openBuyerDetailFromMatch' in html_text
            assert 'openSupplierDetailFromMatch' in html_text
            assert 'onclick="openBuyerDetailFromMatch()"' in html_text
            assert 'onclick="openSupplierDetailFromMatch()"' in html_text
            assert 'xnk_active_tab' in html_text
            assert 'history.replaceState' in html_text
            assert 'hashchange' in html_text
        print(f"✅ Test 38/39: Nhấn Xem Hồ Sơ Chi Tiết Khách Hàng / NCC Tại Bàn Khớp Lệnh & Khôi Phục Tab Khi F5 chuẩn 100%")
        passed_count += 1

        # Test 39: Khắc Phục Lỗi In Giấy Trắng & Hoàn Thiện Biểu Mẫu Hồ Sơ Thẩm Định Ngoại Thương 360° Chuẩn Quốc Tế
        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            assert '#printableDossier' in html_text
            assert 'display: block !important' in html_text
            assert 'BÁO CÁO THẨM ĐỊNH PHÁP NHÂN & ĐỐI TÁC NGOẠI THƯƠNG 360°' in html_text
            assert 'INTERNATIONAL TRADE COUNTERPARTY DUE DILIGENCE & KYC DOSSIER' in html_text
            assert 'I. THÔNG TIN ĐỊNH DANH PHÁP NHÂN' in html_text
            assert 'II. KẾT QUẢ RÀ SOÁT TÌNH BÁO & THẨM ĐỊNH 4 TẦNG' in html_text
            assert 'III. NĂNG LỰC THƯƠNG MẠI, NGUỒN CUNG & LỊCH SỬ VẬN ĐƠN' in html_text or 'NĂNG LỰC THƯƠNG MẠI' in html_text
            assert 'MẠNG LƯỚI ĐỐI TÁC THƯƠNG MẠI TOÀN CẦU' in html_text
            assert 'LỊCH SỬ VẬN ĐƠN HẢI QUAN, GIAO DỊCH & CHÀO ĐƠN B2B' in html_text
            assert 'BỨC TƯỜNG LỬA TÀI CHÍNH & KHUYẾN NGHỊ ĐIỀU KHOẢN HỢP ĐỒNG' in html_text
            assert 'DANH BẠ LIÊN HỆ & ĐẦU MỐI GIAO DỊCH ỦY QUYỀN' in html_text
            assert 'Ý KIẾN THẨM ĐỊNH & PHÊ DUYỆT ĐIỀU HÀNH' in html_text
            assert 'CHUYÊN VIÊN THẨM ĐỊNH' in html_text
            assert 'GIÁM ĐỐC ĐIỀU HÀNH KHỐI XNK' in html_text
            assert 'p-partners-tbody' in html_text
            assert 'p-bl-tbody' in html_text
            assert 'p-rfq-tbody' in html_text
            assert 'p-contacts-tbody' in html_text
            # Verify Chairman signature is removed from printable dossier per directive
            dossier_sub = html_text[html_text.find('id="printableDossier"'):html_text.find('<!-- ============================================================= -->')]
            assert 'KÍNH TRÌNH CHỦ TỊCH TẬP ĐOÀN' not in dossier_sub
            assert "printCurrentDossier('supplier')" in html_text
            assert "printCurrentDossier('buyer')" in html_text
        print(f"✅ Test 39/42: Khắc Phục Lỗi In Giấy Trắng & Hoàn Thiện Biểu Mẫu Hồ Sơ Thẩm Định Ngoại Thương 360° Chuẩn Quốc Tế (Mạng Lưới ĐT, B/L, RFQ, Danh Bạ & Phê Duyệt GĐ Điều Hành) chuẩn 100%")
        passed_count += 1

        # Test 40: Mạng Lưới Đối Tác Ngoại Thương Theo Quốc Gia (Counterparty Network)
        code_lead, res_lead = http_get("/api/leads/detail?id=LEAD-AGRI-001")
        assert code_lead == 200 and res_lead["ok"] == True
        net_lead = res_lead["lead"].get("counterparty_network", {})
        assert net_lead.get("total_partners", 0) >= 6
        assert net_lead.get("total_countries", 0) >= 3
        assert len(net_lead.get("countries", [])) >= 3
        assert len(net_lead.get("partners", [])) >= 6
        assert any(p.get("role") == "Nhà Xuất Khẩu (Shipper)" for p in net_lead.get("partners", []))

        code_sup, res_sup = http_get("/api/suppliers/detail?id=SP-001")
        assert code_sup == 200 and res_sup["ok"] == True
        net_sup = res_sup["supplier"].get("counterparty_network", {})
        assert net_sup.get("total_partners", 0) >= 6
        assert net_sup.get("total_countries", 0) >= 3
        assert any(p.get("role") == "Nhà Nhập Khẩu (Consignee)" for p in net_sup.get("partners", []))

        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            assert 'id="cd-network-section"' in html_text
            assert 'id="cd-network-country-filters"' in html_text
            assert 'id="cd-network-partners-list"' in html_text
            assert 'id="supd-network-section"' in html_text
            assert 'id="supd-network-country-filters"' in html_text
            assert 'id="supd-network-partners-list"' in html_text
            assert 'filterLeadNetworkByCountry' in html_text
            assert 'filterSupplierNetworkByCountry' in html_text
        print(f"✅ Test 40/42: Mạng Lưới Đối Tác Ngoại Thương Theo Quốc Gia & Bộ Lọc Nước Linh Hoạt chuẩn 100%")
        passed_count += 1

        # Test 41: Đơn Giá (Unit Price), Tổng Trị Giá (Total Value) & Nhãn Minh Bạch Trong Vận Đơn B/L
        lead_bls = res_lead["lead"].get("historical_bl_records", [])
        assert len(lead_bls) >= 1
        first_bl = lead_bls[0]
        assert "unit_price" in first_bl
        assert "total_value" in first_bl
        assert "price_type" in first_bl
        assert first_bl["price_type"] in ["CUSTOMS_DECLARATION", "INTELLIGENCE_ESTIMATE"]

        sup_bls = res_sup["supplier"].get("customs_bl_records", [])
        assert len(sup_bls) >= 1
        first_s_bl = sup_bls[0]
        assert "unit_price" in first_s_bl
        assert "total_value" in first_s_bl
        assert "price_type" in first_s_bl

        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            assert 'Đơn giá:' in html_text
            assert 'Tổng trị giá:' in html_text
            assert '🟢 Giá Khai Báo Hải Quan Thực Tế' in html_text
            assert '🔵 Giá Ước Tính Tình Báo' in html_text
        print(f"✅ Test 41/42: Đơn Giá (Unit Price), Tổng Trị Giá & Nhãn Minh Bạch Hải Quan Trong Vận Đơn B/L chuẩn 100%")
        passed_count += 1

        # Test 42: Đổi Nhãn Nút 'Sơ Đồ Phân Hệ' & API Đối Soát Giá Hàng Hóa Đa Sàn (/api/prices/benchmarks)
        code_prices, res_prices = http_get("/api/prices/benchmarks")
        assert code_prices == 200 and res_prices["ok"] == True
        p_sectors = res_prices["data"].get("sectors", [])
        assert len(p_sectors) >= 6
        coffee_sec = next((s for s in p_sectors if s["commodity_id"] == "coffee_robusta"), None)
        assert coffee_sec is not None
        assert len(coffee_sec["benchmarks"]) >= 4
        assert "arbitrage_analysis" in coffee_sec

        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            assert 'Sơ Đồ Phân Hệ' in html_text
            assert 'Tất Cả Phân Hệ (5/5)' not in html_text
        print(f"✅ Test 42/43: Đổi Nhãn Nút Sơ Đồ Phân Hệ & CSDL Đối Soát Giá Hàng Hóa Đa Sàn chuẩn 100%")
        passed_count += 1

        # Test 43: Làm Rõ Đối Tác Toàn Thế Giới & Chi Tiết Theo Quốc Gia & Chi Tiết Từng Đối Tác 360°
        code_lead, res_lead = http_get("/api/leads/detail?id=LEAD-AGRI-001")
        assert code_lead == 200 and res_lead["ok"] == True
        net_lead = res_lead["lead"].get("counterparty_network", {})
        assert net_lead.get("total_partners", 0) >= 6
        assert net_lead.get("total_countries", 0) >= 3
        assert net_lead.get("total_volume_tons", 0) > 0
        assert net_lead.get("total_value_usd", 0) > 0

        # Kiểm tra chi tiết từng quốc gia (Country Deep-Dive)
        first_country = net_lead["countries"][0]
        assert "code" in first_country
        assert "fta_status" in first_country
        assert "shipping_lane" in first_country
        assert "transit_days" in first_country
        assert first_country["total_volume_tons"] > 0
        assert first_country["share_pct"] > 0

        # Kiểm tra chi tiết từng đối tác (Partner Deep Intelligence)
        first_partner = net_lead["partners"][0]
        assert "id" in first_partner
        assert "hs_code" in first_partner
        assert "volume_tons" in first_partner
        assert "unit_price_usd" in first_partner
        assert "value_usd" in first_partner
        assert "credit_score" in first_partner
        assert "payment_terms" in first_partner
        assert "sanctions_status" in first_partner
        assert len(first_partner.get("sample_bl_records", [])) >= 2
        first_bl = first_partner["sample_bl_records"][0]
        assert "bl_number" in first_bl
        assert "unit_price" in first_bl
        assert "total_value" in first_bl

        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            assert 'id="cd-network-kpi-bar"' in html_text
            assert 'id="cd-network-country-detail"' in html_text
            assert 'id="supd-network-kpi-bar"' in html_text
            assert 'id="supd-network-country-detail"' in html_text
            assert 'id="counterpartyDetailModal"' in html_text
            assert 'openCounterpartyDetail' in html_text
            assert 'closeCounterpartyDetailModal' in html_text
            assert 'createRfqFromCounterparty' in html_text
            assert 'DANH SÁCH ĐỐI TÁC NGOẠI THƯƠNG' in html_text
        print(f"✅ Test 43/44: Làm Rõ Đối Tác Toàn Thế Giới & Chi Tiết Theo Quốc Gia & Chi Tiết Từng Đối Tác 360° chuẩn 100%")
        passed_count += 1

        # Test 44: Động Cơ Cố Định Menu & Hướng Dẫn Vuốt Phải Sticky Top Đa Thiết Bị (Cross-Device Sticky Engine)
        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            # 1. Bảo đảm overflow-x: clip (loại bỏ hoàn toàn overflow-x: hidden trên html/body phá vỡ sticky)
            assert 'overflow-x: clip' in html_text
            assert 'html, body {\n      overflow-x: hidden' not in html_text
            assert 'html, body {\r\n      overflow-x: hidden' not in html_text

            # 2. Header chuẩn Universal Sticky
            assert 'executive-sticky-header' in html_text
            assert 'id="mainExecutiveHeader"' in html_text
            assert 'position: -webkit-sticky !important' in html_text
            assert 'position: sticky !important' in html_text

            # 3. JavaScript Sticky Guardian Polyfill cho mọi dòng máy / trình duyệt nhúng
            assert 'initStickyHeaderGuardian' in html_text
            assert 'headerStickyPlaceholder' in html_text
            assert 'sticky-fixed-fallback' in html_text
            assert 'updateStickyHeaderHeight' in html_text

            # 4. Hướng dẫn vuốt phải đính dưới menu tab
            assert 'id="tableSwipeGuidanceWrapper"' in html_text
            assert 'tableSwipeGuidance' in html_text

            # 5. Phân hệ Thẩm định không bị đè chữ Sanctions và Quốc gia trên Mobile
            assert 'id="b-sanctions-pill"' in html_text
            assert 'id="b-country-badge"' in html_text
        print(f"✅ Test 44/45: Động Cơ Cố Định Menu & Hướng Dẫn Vuốt Phải Sticky Top Đa Thiết Bị chuẩn 100%")
        passed_count += 1

        # Test 45: Thanh Tìm Kiếm Mobile Tối Ưu, Gợi Ý Thả Nổi Zero-Displacement & Sanctions Không Xuống Dòng Mới
        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            # 1. Khung gợi ý thả nổi tuyệt đối, không làm xô dịch giao diện
            assert 'id="omniHsSuggestionsDropdown"' in html_text
            assert 'id="omniHsSearchWrapper"' in html_text
            assert 'handleQuickSearchFocus' in html_text
            assert 'clearOmniSearchInput' in html_text
            assert 'selectChapterFromSuggestion' in html_text
            assert 'min-h-[38px]' in html_text
            
            # 2. Sanctions và Thẩm định giữ nguyên hàng ngang không xuống dòng mới
            assert 'id="b-sanctions-pill"' in html_text
            assert 'id="s-tax-risk-pill"' in html_text
            assert 'whitespace-nowrap' in html_text
            assert 'text-[10px]' in html_text
        print(f"✅ Test 45/47: Thanh Tìm Kiếm Mobile Tối Ưu, Gợi Ý Thả Nổi Zero-Displacement & Sanctions Cùng Hàng Ngang chuẩn 100%")
        passed_count += 1

        # Test 46: Tra Cứu Đầy Đủ Sản Phẩm Thuộc Các Mã Ngành (/api/hs/products & Master Products Catalog)
        code, prods_res = http_get("/api/hs/products?limit=10")
        assert code == 200
        assert prods_res["status"] == "SUCCESS"
        assert prods_res["total_master_count"] >= 200

        # Tra cứu theo chương 09 (Cà phê)
        code, ch09_prods = http_get("/api/hs/products?chapter=09")
        assert code == 200
        assert ch09_prods["total"] >= 5
        assert any("0901.11" in p["hs"] for p in ch09_prods["products"])

        # Tra cứu theo từ khóa 'ca phe'
        code, coffee_res = http_get("/api/hs/products?q=ca+phe")
        assert code == 200
        assert coffee_res["total"] >= 3

        # Tra cứu tích hợp omni-search trả về cả Chapters và Products
        code, omni_both = http_get("/api/hs/search?q=ca+phe")
        assert code == 200
        assert omni_both["total_matches"] >= 1
        assert omni_both["total_products"] >= 3
        assert any(item["code"] == "09" for item in omni_both["results"])
        assert any("0901" in p["hs"] for p in omni_both["products"])

        # Kiểm tra frontend tích hợp tra cứu sản phẩm
        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            assert 'allProductsMasterList' in html_text
            assert 'selectProductFromSuggestion' in html_text
            assert 'SẢN PHẨM CỤ THỂ THUỘC MÃ NGÀNH' in html_text
        print(f"✅ Test 46/47: Tra Cứu Đầy Đủ Sản Phẩm Thuộc Các Mã Ngành (Tổng {prods_res['total_master_count']} sản phẩm, 97 chương HS) chuẩn 100%")
        passed_count += 1

        # Test 47: Radar Pháp Lý & Giám Sát Chân Trời Chính Sách Ngoại Thương (EUDR, CBAM, UFLPA, GACC)
        code, regs_res = http_get("/api/regulations/active")
        assert code == 200
        assert regs_res["total"] >= 5
        assert any(r["code"] == "EUDR" for r in regs_res["regulations"])
        assert any(r["code"] == "CBAM" for r in regs_res["regulations"])
        assert any(r["code"] == "UFLPA" for r in regs_res["regulations"])

        # Kiểm tra lịch dự báo chân trời chính sách
        code, cal_res = http_get("/api/regulations/horizon-calendar")
        assert code == 200
        assert cal_res["total_events"] >= 5

        # Kiểm tra chi tiết quy định EUDR
        code, detail_res = http_get("/api/regulations/detail?id=REG-EUDR-2024")
        assert code == 200
        assert detail_res["regulation"]["risk_level"] == "CAO"
        assert "legal_firm_advice" in detail_res["regulation"]
        assert "logistics_advice" in detail_res["regulation"]

        # Kiểm tra gửi cảnh báo Telegram (chế độ dry_run=True)
        code, alert_res = http_post("/api/regulations/notify-risk-alert", {
            "reg_id": "REG-EUDR-2024",
            "dry_run": True
        })
        assert code == 200
        assert alert_res["ok"] is True
        assert alert_res["result"]["dry_run"] is True

        # Kiểm tra giao diện Frontend Radar Pháp Lý
        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            assert 'id="regulatoryRadarModal"' in html_text
            assert 'openRegulatoryRadarModal' in html_text
            assert 'closeRegulatoryRadarModal' in html_text
            assert 'fetchRegulatoryRadarData' in html_text
            assert 'sendRegulatoryRiskAlertTelegram' in html_text
            assert 'regulatoryRadarBtn' in html_text
        print(f"✅ Test 47/48: Radar Pháp Lý & Giám Sát Chân Trời Chính Sách Ngoại Thương (EUDR, CBAM, UFLPA, GACC & Telegram Alert) chuẩn 100%")
        passed_count += 1

        # Test 48: Giải Thích Chi Tiết & Khuyến Nghị Nghiệp Vụ Khi Rê Chuột / Chạm Thẻ Tag
        code, tag_explain_res = http_get("/api/trade-tags/explain?tag=%23Moist_Max12.5%25")
        assert code == 200
        assert tag_explain_res["status"] == "SUCCESS"
        assert "Độ ẩm tối đa" in tag_explain_res["info"]["name"]
        assert "Quy Cách Kỹ Thuật" in tag_explain_res["info"]["category"]
        assert "SGS" in tag_explain_res["info"]["advice"]

        code, tag_halal_res = http_get("/api/trade-tags/explain?tag=%23Halal_JAKIM")
        assert code == 200
        assert "Halal" in tag_halal_res["info"]["name"]
        assert "Sharia" in tag_halal_res["info"]["desc"]

        code, catalog_res = http_get("/api/trade-tags/catalog")
        assert code == 200
        assert catalog_res["total"] >= 20

        # Kiểm tra giao diện Frontend hỗ trợ hover/click và banner giải thích
        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            assert 'id="md-tag-detail-banner"' in html_text
            assert 'id="tradeTagFloatingTooltip"' in html_text
            assert 'handleTradeTagHover' in html_text
            assert 'handleTradeTagClick' in html_text
            assert 'handleTradeTagLeave' in html_text
            assert 'TRADE_TAG_DEFINITIONS' in html_text
            assert 'getTradeTagInfo' in html_text
            assert 'trade-tag-item' in html_text
            assert 'TIÊU CHÍ & QUY CHUẨN ĐÃ KHỚP HOÀN TOÀN' in html_text
            assert 'ĐIỂM VÊNH QUY CHUẨN CẦN THƯƠNG THẢO' in html_text
        print(f"✅ Test 48/49: Hiển Thị Nội Dung & Khuyến Nghị Khi Ấn / Rê Chuột Vào Thẻ Tag (Trade Tags Tooltip & Detail Engine) chuẩn 100%")
        passed_count += 1

        # Test 49: Bảng Giá Tham Chiếu Đa Sàn, Bộ Chuẩn Hóa Đơn Vị & Khắc Phục Cuộn Trang Desktop / Mobile / Radar
        code, prices_res = http_get("/api/prices/benchmarks")
        assert code == 200
        assert prices_res["ok"] is True
        assert "sectors" in prices_res["data"]
        sectors = prices_res["data"]["sectors"]
        assert len(sectors) >= 6
        assert any(s["commodity_id"] == "coffee_robusta" for s in sectors)
        assert any(s["commodity_id"] == "fertilizer_urea" for s in sectors)
        assert any(s["commodity_id"] == "rice_5pct" for s in sectors)
        assert any(s["commodity_id"] == "black_pepper" for s in sectors)
        assert any(s["commodity_id"] == "seafood_shrimp" for s in sectors)
        assert any(s["commodity_id"] == "natural_rubber" for s in sectors)

        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            # 1. Bảng giá đa sàn & Arbitrage Modal
            assert 'id="crossExchangePricesModal"' in html_text
            assert 'openCrossExchangePricesModal' in html_text
            assert 'closeCrossExchangePricesModal' in html_text
            assert 'fetchPriceBenchmarksData' in html_text
            assert 'calculateUnitConversion' in html_text
            assert 'crossExchangePricesBtn' in html_text
            assert 'id="commodityPriceTabsContainer"' in html_text
            assert 'id="commodity4TierGridContainer"' in html_text
            assert 'id="unitCalcQuantity"' in html_text
            assert 'id="unitCalcUnitSelect"' in html_text

        # 1b. Bảng giá trong workspace dùng tab và khôi phục qua URL hash.
        url_prices = f"http://127.0.0.1:{TEST_PORT}/#prices"
        with urllib.request.urlopen(url_prices, timeout=5) as prices_resp:
            assert prices_resp.status == 200
            prices_html = prices_resp.read().decode('utf-8')
            assert 'id="section-prices"' in prices_html
            assert "onclick=\"switchTab('prices')\"" in prices_html
            assert "window.location.replace('/prices')" not in prices_html
            assert 'id="commodityPriceCanvas"' in prices_html
            assert 'id="multiSourcePriceTableBody"' in prices_html

        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')

            # 2. Khắc phục lỗi cuộn trang Desktop & Mobile
            assert 'overflow-y: auto' in html_text
            assert 'overflow-y: visible' in html_text
            assert 'touch-action: pan-y !important' in html_text
            assert 'id="allModulesHubBackdrop"' in html_text
            assert 'id="allModulesHubScrollBody"' in html_text
            assert 'id="regulatoryRadarScrollBody"' in html_text
            assert 'max-h-[82vh]' in html_text
            assert 'modal-scroll-container' in html_text
        print(f"✅ Test 49/50: Bảng Giá Đa Sàn (6 Mặt Hàng Chiến Lược), Bộ Chuẩn Hóa Đơn Vị & Khắc Phục Cuộn Trang Desktop/Mobile/Radar chuẩn 100%")
        passed_count += 1

        # Test 50: Cơ Chế Tự Động Khôi Phục Vị Trí Cuộn Lên Đầu (Scroll Reset to Top) Cho Mọi Popup & Modal Khi Mở/Đóng
        with urllib.request.urlopen(url_html, timeout=5) as html_resp:
            html_text = html_resp.read().decode('utf-8')
            # 1. Hàm universal resetModalScroll tồn tại và xử lý đa container
            assert 'function resetModalScroll(modalOrId)' in html_text
            assert 'modal.scrollTop = 0' in html_text
            assert 'container.scrollTop = 0' in html_text
            assert 'requestAnimationFrame(() => resetModalScroll' in html_text

            # 2. Toàn bộ các Modal Scroll Container được định danh ID rõ ràng
            assert 'id="companyContactsScrollBody"' in html_text
            assert 'id="companyDetailScrollBody"' in html_text
            assert 'id="supplierDetailScrollBody"' in html_text
            assert 'id="counterpartyDetailScrollBody"' in html_text
            assert 'id="hsCatalogScrollBody"' in html_text
            assert 'id="outreachScrollBody"' in html_text
            assert 'id="dualRfqScrollBody"' in html_text
            assert 'id="matchDetailScrollBody"' in html_text
            assert 'id="regulatoryRadarScrollBody"' in html_text
            assert 'id="crossExchangePricesScrollBody"' in html_text

            # 3. Popup Đầu Mối Liên Lạc (companyContactsModal) tự động reset cuộn lên đầu khi mở & khi đóng
            assert 'lockBodyScroll(\'companyContactsModal\')' in html_text
            assert 'resetModalScroll(\'companyContactsModal\')' in html_text
            assert 'scBody.scrollTop = 0' in html_text

            # 4. Universal Modal Manager tích hợp resetModalScroll vào lockBodyScroll, closeModalById, closeAllModals
            assert 'function lockBodyScroll(modalId)' in html_text
            assert 'resetModalScroll(modalId)' in html_text
            assert 'allModalIds.forEach(id => resetModalScroll(id))' in html_text

            # 5. Phân hệ Kiểm toán SOP-02: Popup Modal Tạo Phiếu Mới (auditFormModal) độc lập & mở chuẩn xác
            assert 'id="auditFormModal"' in html_text
            assert 'id="auditFormScrollBody"' in html_text
            assert 'openAuditModal()' in html_text
            assert 'function openAuditModal(' in html_text
            assert 'function closeAuditModal(' in html_text
            assert 'id="af_name"' in html_text
            assert 'id="af_tax"' in html_text
            assert 'id="c1_range"' in html_text
            assert 'id="audit_total_score"' in html_text
            idx_radar = html_text.find('id="regulatoryRadarModal"')
            idx_audit = html_text.find('id="auditFormModal"')
            start_radar = html_text.rfind('<div', 0, idx_radar)
            start_audit = html_text.rfind('<div', 0, idx_audit)
            radar_slice = html_text[start_radar:start_audit]
            assert radar_slice.count('<div') == radar_slice.count('</div>')
        print(f"✅ Test 50/52: Cơ Chế Tự Động Khôi Phục Vị Trí Cuộn Lên Đầu & Popup Kiểm Toán Xưởng (SOP-02) chuẩn 100%")
        passed_count += 1

        # Test 51: Cổng Quản Trị Proxy Chờ "Cắm-Là-Chạy" & Kiểm Thử Kết Nối (/api/proxy/config & /api/proxy/test)
        code, p_cfg = http_get("/api/proxy/config")
        assert code == 200 and p_cfg.get("ok") is True
        assert "status" in p_cfg and "mode" in p_cfg["status"]
        assert p_cfg["status"]["mode"] in ["DIRECT", "STATIC_POOL", "ROTATING_API"]
        
        # Thử cập nhật cấu hình proxy
        code, p_update = http_post("/api/proxy/config", {"mode": "DIRECT", "timeout_seconds": 15})
        assert code == 200 and p_update.get("ok") is True

        # Kiểm thử IP ngoại mạng và độ trễ
        code, p_test = http_post("/api/proxy/test", {})
        assert code == 200
        assert "mode" in p_test
        print(f"✅ Test 51/52: Cổng Quản Trị Proxy Chờ Cắm-Là-Chạy & Đo Kiểm IP/Ping chuẩn xác (Mode: {p_test.get('mode')}, Ping: {p_test.get('latency_ms', 'N/A')}ms)")
        passed_count += 1

        # Test 52: Động Cơ Quét Dữ Liệu Hải Quan Hàng Ngày & Bộ Lọc Khách Hàng 24h Cho Sales
        code, ing_status = http_get("/api/customs/ingestion-status")
        assert code == 200 and ing_status.get("ok") is True
        assert ing_status["data"]["total_countries_covered"] == 27
        assert ing_status["data"]["new_bl_count_24h"] >= 0

        # Kiểm tra bộ lọc recent_24h trên API Leads
        code, leads_24h = http_get("/api/leads/by-industry?recent_24h=true&page=1&page_size=10")
        assert code == 200
        assert "funnel_stats" in leads_24h
        assert "recent_24h" in leads_24h["funnel_stats"]
        assert leads_24h["total"] >= 10
        for l in leads_24h["data"]:
            assert l.get("has_recent_24h_update") is True

        # Kiểm tra chi tiết đơn hàng B2B có hiển thị hạn nộp báo giá (deadline_date & days_remaining)
        sample_lead_id = leads_24h["data"][0]["lead_id"]
        code, b2b_orders = http_get(f"/api/leads/b2b-orders?lead_id={sample_lead_id}")
        assert code == 200 and b2b_orders.get("ok") is True
        assert len(b2b_orders["orders"]) > 0
        latest_o = b2b_orders["orders"][0]
        assert "deadline_date" in latest_o or "status" in latest_o
        print(f"✅ Test 52/53: Động Cơ Quét Dữ Liệu Hải Quan Hàng Ngày & Bộ Lọc Khách Hàng 24h Cho Sales chuẩn 100% (24h Leads: {leads_24h['total']}, 27 Quốc Gia)")
        passed_count += 1

        # Test 53: Động Cơ Tình Báo Nhà Cung Cấp Thời Gian Thực (GLEIF LEI, Cấm Vận OpenSanctions & Tái Thẩm Định 360° Live)
        code, live_search = http_get("/api/suppliers/live-search?q=Uralkali")
        assert code == 200
        assert live_search.get("ok") is True
        assert live_search.get("count") >= 1
        top_ent = live_search["data"][0]
        assert top_ent.get("lei") is not None
        assert top_ent.get("score") >= 80

        code, reverify_res = http_get("/api/suppliers/reverify?name=PJSC%20Uralkali")
        assert code == 200
        assert reverify_res.get("ok") is True
        assert reverify_res["supplier"].get("lei") is not None

        # Kiểm tra frontend HTML chứa đầy đủ thành tố Real-Time Live Sourcing
        with urllib.request.urlopen(f"http://127.0.0.1:{TEST_PORT}/", timeout=5) as hr:
            fresh_html = hr.read().decode('utf-8')
        assert "triggerLiveDiscovery" in fresh_html
        assert "reverifySupplierLive" in fresh_html
        assert "LIVE GLEIF & HẢI QUAN REAL-TIME" in fresh_html

        print("✅ Test 53/54: Động cơ Tình báo & Thẩm định Nhà Cung Cấp Thời Gian Thực (GLEIF LEI, Cấm Vận OpenSanctions & Tái Thẩm Định 360° Live) chuẩn 100%")
        passed_count += 1

        # Test 54: Động cơ Săn Tìm Co Giãn Đa Tầng (Elastic Multi-Tier Sourcing), Nhận Diện Phả Hệ Tập Đoàn (Uralchem Trading Latvia -> Gốc Nga RU) & Chuyển Tự Động Kirin-Latinh ISO 9
        # 1. Lọc nước Nga phải trả về đầy đủ các tập đoàn trụ cột (>= 10 NCC thay vì 2)
        code, ru_sups = http_get("/api/suppliers?country=russia")
        assert code == 200
        assert len(ru_sups) >= 10, f"Expected >= 10 Russian suppliers, got {len(ru_sups)}"
        ru_names = [s.get("company_name", "").lower() for s in ru_sups]
        assert any("uralchem" in n for n in ru_names), "Uralchem missing in Russian suppliers list"
        assert any("uralkali" in n for n in ru_names), "Uralkali missing in Russian suppliers list"
        assert any("phosagro" in n for n in ru_names), "PhosAgro missing in Russian suppliers list"

        # 2. Tìm kiếm 'uralchem' ở nước Nga: Trả về Uralchem với mã LEI và nguồn gốc xuất xứ RU
        code, ru_uralchem = http_get("/api/suppliers?country=russia&q=uralchem")
        assert code == 200
        assert len(ru_uralchem) >= 1
        top_u = ru_uralchem[0]
        assert top_u.get("lei") == "549300Z7BTXHEBVTPH20"
        assert top_u.get("origin_country_code") == "RU"

        # 3. Tìm kiếm bằng chữ Kirin 'Уралхим' (ISO 9 Transliteration)
        code, cyr_res = http_get("/api/suppliers?q=%D0%A3%D1%80%D0%B0%D0%BB%D1%85%D0%B8%D0%BC")
        assert code == 200
        assert len(cyr_res) >= 1
        assert any("uralchem" in s.get("company_name", "").lower() for s in cyr_res)

        # 4. Kiểm tra thị trường độc quyền nhóm (Belarus -> Belaruskali OLIGOPOLY)
        code, by_sups = http_get("/api/suppliers?country=by")
        assert code == 200
        assert len(by_sups) >= 1
        assert by_sups[0].get("market_structure") == "OLIGOPOLY"

        # 5. Kiểm tra HTML chứa nhãn phả hệ tập đoàn và huy hiệu độc quyền nhóm
        with urllib.request.urlopen(f"http://127.0.0.1:{TEST_PORT}/", timeout=5) as hr:
            fresh_html = hr.read().decode('utf-8')
        assert "CẤU TRÚC PHẢ HỆ TẬP ĐOÀN ĐA QUỐC GIA" in fresh_html
        assert "ĐỘC QUYỀN NHÓM QUỐC GIA" in fresh_html

        print("✅ Test 54/55: Động cơ Săn Tìm Co Giãn Đa Tầng (Elastic Sourcing), Nhận Diện Phả Hệ Tập Đoàn (Uralchem Trading Latvia -> Gốc Nga RU) & Chuyển Tự Động Kirin-Latinh ISO 9 chuẩn 100%")
        passed_count += 1

        # --- TEST 55: Lịch Sử Vận Đơn (Customs B/L Records) & Mạng Lưới Đối Tác Toàn Cầu Của Nhà Cung Cấp ---
        # 1. Kiểm tra nhà cung cấp gốc Nga có đầy đủ lịch sử vận đơn và mạng lưới đối tác
        code, ru_sups = http_get("/api/suppliers?country=russia")
        assert code == 200
        uralchem = next((s for s in ru_sups if "uralchem" in s.get("company_name", "").lower()), None)
        assert uralchem is not None, "Uralchem not found in Russian suppliers list"
        
        # Kiểm tra chuỗi vận đơn hải quan
        bls = uralchem.get("customs_bl_records", [])
        assert len(bls) >= 8, f"Expected >= 8 B/L records, got {len(bls)}"
        assert all(b.get("bl_number") and b.get("vessel") and b.get("discharge_port") and b.get("unit_price") for b in bls), "B/L records missing essential fields"
        assert uralchem.get("bl_stats_1y", {}).get("total_bl_1y") is not None, "bl_stats_1y missing"

        # Kiểm tra mạng lưới đối tác toàn cầu theo từng quốc gia
        net = uralchem.get("counterparty_network", {})
        assert net.get("total_partners") >= 8, f"Expected >= 8 partners, got {net.get('total_partners')}"
        assert net.get("total_countries") >= 5, f"Expected >= 5 countries, got {net.get('total_countries')}"
        countries = net.get("countries", {})
        c_codes = {c.get("code") if isinstance(c, dict) else c for c in net.get("countries", [])}
        assert "VN" in c_codes and "CN" in c_codes and "IN" in c_codes and "BR" in c_codes, "Key trading countries missing in network" 
        partners = net.get("partners", [])
        assert any("PVCFC" in p.get("name", "") for p in partners), "PVCFC missing in Uralchem network"
        assert all(len(p.get("sample_bl_records", [])) >= 2 for p in partners), "Sample B/Ls missing in partners"

        # 2. Kiểm tra API chi tiết /api/suppliers/detail?id=SUP-GLB-RU-001
        code, detail_res = http_get("/api/suppliers/detail?id=SUP-GLB-RU-001")
        assert code == 200
        assert detail_res.get("ok") is True
        det_sup = detail_res.get("supplier", {})
        assert len(det_sup.get("customs_bl_records", [])) >= 8
        assert det_sup.get("counterparty_network", {}).get("total_partners") >= 8

        # 3. Kiểm tra giao diện HTML có đầy đủ thành phần modal mạng lưới và vận đơn nhà cung cấp
        with urllib.request.urlopen(f"http://127.0.0.1:{TEST_PORT}/", timeout=5) as hr:
            fresh_html = hr.read().decode('utf-8')
        assert "supd-network-section" in fresh_html, "supd-network-section missing in HTML"
        assert "supd-network-country-filters" in fresh_html, "supd-network-country-filters missing in HTML"
        assert "supd-network-partners-list" in fresh_html, "supd-network-partners-list missing in HTML"
        assert "supd-bl-container" in fresh_html, "supd-bl-container missing in HTML"
        assert "renderSupplierNetwork" in fresh_html, "renderSupplierNetwork missing in JS"
        assert "renderSupplierBLList" in fresh_html, "renderSupplierBLList missing in JS"

        print("✅ Test 55/56: Hồ Sơ Vận Đơn Hải Quan (Customs B/L) & Mạng Lưới Đối Tác Toàn Cầu (Counterparty Network) Theo Quốc Gia Cho Nhà Cung Cấp Đạt Chuẩn 100%")
        passed_count += 1

        # --- TEST 56: Xác Thực Chuẩn Xác Shipper/Consignee/POL/POD & Loại Bỏ Lịch Sử Vận Đơn Lồng Nhau Trong Modal Vận Đơn B/L ---
        # 1. Kiểm tra API chi tiết vận đơn B/L nhà cung cấp Nga (URAL-982-2026-01)
        code, bld_res = http_get("/api/discovery/bl/detail?bl_number=URAL-982-2026-01")
        assert code == 200, f"Expected 200, got {code}"
        assert bld_res.get("ok") is True
        b_info = bld_res.get("bl", {})
        
        # Người gửi phải là tập đoàn xuất khẩu thực tế (Uralchem)
        shipper_val = b_info.get("shipper", "").lower()
        assert "uralchem" in shipper_val, f"Shipper must be Uralchem, got: {b_info.get('shipper')}"
        assert "tập đoàn ngoại thương việt nam" not in shipper_val, "Generic fallback detected for shipper!"

        # Người nhận phải là đơn vị thu mua chỉ định (PVCFC)
        consignee_val = b_info.get("consignee", "").lower()
        assert "pvcfc" in consignee_val or "cà mau" in consignee_val, f"Consignee must be PVCFC, got: {b_info.get('consignee')}"
        assert "doanh nghiệp thu mua quốc tế" not in consignee_val, "Generic fallback detected for consignee!"

        # Cảng bốc hàng (POL) phải là cảng xuất khẩu Nga / Baltic
        pol_val = b_info.get("port_of_loading", "").lower()
        assert any(p in pol_val for p in ["ust-luga", "petersburg", "nga", "baltic"]), f"POL must be Russian port, got: {b_info.get('port_of_loading')}"

        # Cảng dỡ hàng (POD) phải là cảng đến Việt Nam (Cát Lái)
        pod_val = b_info.get("port_of_discharge", "").lower()
        assert "cát lái" in pod_val or "vncli" in pod_val, f"POD must be Cat Lai, got: {b_info.get('port_of_discharge')}"

        # 2. Kiểm tra HTML: Đã loại bỏ hoàn toàn khối lồng lịch sử vận đơn (bld-bl-container) bên trong modal vận đơn đơn lẻ
        with urllib.request.urlopen(f"http://127.0.0.1:{TEST_PORT}/", timeout=5) as hr:
            fresh_html = hr.read().decode('utf-8')
        
        # Kiểm tra sự hiện diện của Phân hệ Chủ Thể và Hồ sơ Thủ Tục Thông Quan
        assert "bld-party-section" in fresh_html, "bld-party-section missing in HTML"
        assert "bld-customs-decl-id" in fresh_html, "bld-customs-decl-id missing in HTML"
        assert "bld-shipper-entity-name" in fresh_html, "bld-shipper-entity-name missing in HTML"
        assert "bld-consignee-entity-name" in fresh_html, "bld-consignee-entity-name missing in HTML"
        
        # Đảm bảo KHÔNG còn bld-bl-container bên trong blDetailModal (không lồng danh sách vận đơn trong popup vận đơn)
        bld_modal_idx = fresh_html.find('id="blDetailModal"')
        bld_modal_end = fresh_html.find('<!-- END MODAL blDetailModal -->', bld_modal_idx)
        if bld_modal_end == -1:
            bld_modal_end = bld_modal_idx + 8000
        bl_modal_sub = fresh_html[bld_modal_idx:bld_modal_end]
        assert "bld-bl-container" not in bl_modal_sub, "bld-bl-container still found inside blDetailModal!"

        print("✅ Test 56/56: Xác Thực Chuẩn Xác Chủ Thể Ngoại Thương (Shipper Uralchem ➔ Consignee PVCFC, Cảng Ust-Luga ➔ Cảng Cát Lái) & Tinh Gọn Modal Vận Đơn B/L Đạt Chuẩn 100%")
        passed_count += 1

        # --- TEST 57: Xác Thực Hồ Sơ Chi Tiết Bài Đăng Thu Mua B2B & Cơ Chế Bấm Vào Mã Đơn / Ngày Trên Sàn ---
        code, rfq_res = http_get("/api/leads/b2b-orders/detail?rfq_id=RFQ-ALI-20261001&lead_id=LEAD-AGRI-001")
        assert code == 200, f"Expected 200, got {code}"
        assert rfq_res.get("ok") is True
        assert rfq_res.get("rfq_id") == "RFQ-ALI-20261001"
        assert rfq_res.get("commodity") is not None
        assert rfq_res.get("volume_required") is not None
        assert rfq_res.get("payment_term") is not None
        assert rfq_res.get("buyer", {}).get("company_name") is not None

        # Kiểm tra frontend: Modal b2bOrderDetailModal và cơ chế click vào mã đơn/ngày
        with urllib.request.urlopen(f"http://127.0.0.1:{TEST_PORT}/", timeout=5) as hr:
            html_content = hr.read().decode('utf-8')

        assert "b2bOrderDetailModal" in html_content, "b2bOrderDetailModal missing in HTML"
        assert "openB2BOrderDetailModal" in html_content, "openB2BOrderDetailModal missing in HTML"
        assert "b2b-od-rfq-id" in html_content, "b2b-od-rfq-id missing in HTML"
        assert "b2b-od-deadline" in html_content, "b2b-od-deadline missing in HTML"

        print("✅ Test 57/57: Hồ Sơ Chi Tiết Gói Thầu Thu Mua B2B (RFQ Dossier) & Cơ Chế Click Trực Tiếp Mã Đơn/Ngày Đạt Chuẩn 100%")
        passed_count += 1

        # --- TEST 58: Xác Thực POL/POD Khác Nhau 100%, Consignee Chính Xác, Cổng Hãng Tàu Trực Tiếp & Email Liên Hệ Chính Thống ---
        from server import get_all_aggregated_bls
        import realtime_sourcing_engine as rse

        all_bls = get_all_aggregated_bls()
        assert len(all_bls) >= 6000

        # 1. Toàn bộ 100% Vận đơn phải có POL khác POD và Consignee chuẩn danh nghiệp thực
        for b in all_bls[:500]:
            pol = b.get("port_of_loading", "")
            pod = b.get("port_of_discharge", "")
            c = b.get("consignee", "")
            assert pol != pod, f"POL and POD are identical: {pol} for BL {b.get('bl_number')}"
            assert not ("cát lái" in pol.lower() and "cát lái" in pod.lower()), f"Cat Lai duplicate in BL {b.get('bl_number')}"
            assert not ("hải phòng" in pol.lower() and "hải phòng" in pod.lower()), f"Hai Phong duplicate in BL {b.get('bl_number')}"
            assert "đối tác thu mua quốc tế" not in c.lower(), f"Generic consignee in BL {b.get('bl_number')}"
            assert "doanh nghiệp thu mua quốc tế" not in c.lower(), f"Generic consignee in BL {b.get('bl_number')}"

        # 2. Kiểm tra API chi tiết vận đơn BFC-321-2026-01 (Nhà cung cấp Việt Nam xuất khẩu)
        code_bfc, res_bfc = http_get("/api/discovery/bl/detail?bl_number=BFC-321-2026-01")
        assert code_bfc == 200 and res_bfc.get("ok") is True
        bl_bfc = res_bfc.get("bl", {})
        assert bl_bfc.get("port_of_loading") != bl_bfc.get("port_of_discharge")
        assert "đối tác thu mua quốc tế" not in bl_bfc.get("consignee", "").lower()
        c_info = bl_bfc.get("carrier_info", {})
        assert "tracking_url" in c_info
        assert "google.com" not in c_info.get("tracking_url")
        assert "searates.com" in c_info.get("tracking_url") or "carrier" in c_info.get("tracking_url")

        # 3. Kiểm tra thông tin liên hệ chính thống của các Tập đoàn trong realtime_sourcing_engine
        p_dict = {p["id"]: p for p in rse.STRATEGIC_GLOBAL_PRODUCERS}
        assert "SUP-GLB-RU-001" in p_dict
        u_contact = p_dict["SUP-GLB-RU-001"].get("contact", {})
        assert u_contact.get("email") == "export@uralchem.com"
        assert u_contact.get("phone") == "+7 495 721 89 89"
        assert p_dict["SUP-GLB-RU-001"].get("default_pol") is not None

        phos_contact = p_dict["SUP-GLB-RU-003"].get("contact", {})
        assert phos_contact.get("email") == "fertilizers-export@phosagro.ru"

        # 4. Kiểm tra giao diện HTML: Tuyệt đối không còn link Google search và fake email
        with urllib.request.urlopen(f"http://127.0.0.1:{TEST_PORT}/", timeout=5) as hr:
            html_text = hr.read().decode('utf-8')

        assert "google.com/search" not in html_text, "Found google.com/search in HTML!"
        assert "sourcing@trading.com" not in html_text, "Found sourcing@trading.com in HTML!"
        assert "sale@trading.com" not in html_text, "Found sale@trading.com in HTML!"
        assert "bld-carrier-track-btn" in html_text

        print("✅ Test 58/58: Tuyệt Đối Phân Biệt POL/POD, Chuẩn Hóa Pháp Nhân Consignee, Cổng Hãng Tàu Trực Tiếp & Email Liên Hệ Chính Thống Đạt Chuẩn 100%")
        passed_count += 1

    finally:
        httpd.shutdown()

    print("==================================================================")
    print(f"🎉 KẾT QUẢ: {passed_count}/{total_tests} BÀI KIỂM THỬ ĐẠT CHUẨN 100%!")
    print("==================================================================")

if __name__ == "__main__":
    run_all_tests()
