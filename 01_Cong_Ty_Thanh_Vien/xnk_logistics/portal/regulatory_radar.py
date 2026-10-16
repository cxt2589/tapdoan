# -*- coding: utf-8 -*-
"""
Hệ Thống Radar Pháp Lý & Giám Sát Chân Trời Chính Sách Ngoại Thương Toàn Cầu
(Global Regulatory Radar & Policy Horizon Scanning Engine)
Phối hợp: Hãng Luật Doanh Nghiệp (Project/luat) ⇄ Khối XNK & Logistics (Project/XNK) ⇄ Công Nghệ THD (Antigravity)
"""

import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(CURRENT_DIR, "data", "regulatory_radar_db.json")

TELEGRAM_BOT_TOKEN = "8056463991:AAGy5g9B9C4UqY8YkKqY-hPZ4XqJ3R_xX9A"
DEFAULT_CHAT_ID = "6034655358"  # Chủ tịch Cao Xuân Trường

def load_regulations():
    """Tải toàn bộ cơ sở dữ liệu quy định từ JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[regulatory_radar] Lỗi đọc {DATA_FILE}: {e}")
    return []

def get_active_regulations(market=None, hs=None, risk_level=None):
    """
    Truy vấn danh sách quy định pháp lý ngoại thương với các bộ lọc:
    - market: Thị trường (EU, Mỹ, Trung Quốc, ASEAN, GCC...)
    - hs: Mã HS hoặc Chương HS (09, 44, 72, 85...)
    - risk_level: Mức độ rủi ro (CAO, TRUNG BÌNH, THẤP)
    """
    regs = load_regulations()
    results = []
    
    m_filter = (market or "").strip().lower()
    hs_filter = (hs or "").strip().replace(".", "")
    r_filter = (risk_level or "").strip().upper()

    for r in regs:
        # Lọc theo thị trường
        if m_filter:
            m_matched = any(m_filter in m.lower() for m in r.get("markets", []))
            if not m_matched and m_filter not in r.get("title_vi", "").lower() and m_filter not in r.get("summary", "").lower():
                continue

        # Lọc theo mã HS / Chương HS
        if hs_filter:
            hs_matched = any(hs_filter.startswith(ch) or ch.startswith(hs_filter[:2]) for ch in r.get("hs_chapters", []))
            prod_matched = any(hs_filter in p for p in r.get("affected_products", []))
            if not hs_matched and not prod_matched:
                continue

        # Lọc theo mức độ rủi ro
        if r_filter:
            if r.get("risk_level", "").upper() != r_filter:
                continue

        results.append(r)

    return results

def get_horizon_calendar():
    """
    Lấy lịch dự báo chân trời chính sách (Horizon Scanning Calendar)
    Sắp xếp các mốc hiệu lực / ân hạn / báo cáo theo thứ tự thời gian
    """
    regs = load_regulations()
    calendar_events = []
    
    for r in regs:
        calendar_events.append({
            "id": r["id"],
            "code": r["code"],
            "title": r["title_vi"],
            "effective_date": r.get("effective_date", ""),
            "horizon_quarter": r.get("horizon_quarter", ""),
            "days_remaining_est": r.get("days_remaining_est", 0),
            "status": r.get("status", ""),
            "risk_level": r.get("risk_level", "TRUNG BÌNH"),
            "risk_badge_color": r.get("risk_badge_color", "amber"),
            "forecast_notice": r.get("forecast_notice", ""),
            "markets": r.get("markets", []),
            "hs_chapters": r.get("hs_chapters", [])
        })

    # Sắp xếp theo ngày hiệu lực
    calendar_events.sort(key=lambda x: x["effective_date"])
    return calendar_events

def get_regulation_by_id(reg_id):
    """Lấy chi tiết hồ sơ quy định pháp lý 360° theo ID"""
    regs = load_regulations()
    for r in regs:
        if r.get("id") == reg_id or r.get("code") == reg_id:
            return r
    return None

def search_regulations(query):
    """Tìm kiếm nhanh quy định pháp lý theo từ khóa bất kỳ"""
    q = (query or "").strip().lower()
    if not q:
        return load_regulations()
    
    results = []
    for r in load_regulations():
        haystack = " ".join([
            r.get("code", ""),
            r.get("title_vi", ""),
            r.get("title_en", ""),
            r.get("issuing_body", ""),
            " ".join(r.get("markets", [])),
            " ".join(r.get("affected_products", [])),
            r.get("summary", ""),
            r.get("legal_firm_advice", ""),
            r.get("logistics_advice", "")
        ]).lower()
        if q in haystack:
            results.append(r)
    return results

def format_telegram_risk_alert(reg_id):
    """
    Soạn thảo thông điệp cảnh báo rủi ro pháp lý chuẩn bị gửi Telegram
    Định dạng Mobile-First, sử dụng Visual Anchors, tối ưu đọc trong 30 giây
    """
    reg = get_regulation_by_id(reg_id)
    if not reg:
        return "❌ Không tìm thấy hồ sơ quy định trong cơ sở dữ liệu."

    alert_icon = "🔴" if reg.get("risk_level") == "CAO" else "🟡"
    markets_str = ", ".join(reg.get("markets", [])[:3])
    products_str = "; ".join(reg.get("affected_products", [])[:4])
    
    msg_lines = [
        f"🚨 {alert_icon} CẢNH BÁO RỦI RO PHÁP LÝ & CHÍNH SÁCH NGOẠI THƯƠNG",
        "",
        f"⚖️ Quy định: {reg.get('title_vi')} ({reg.get('code')})",
        f"🏛️ Cơ quan ban hành: {reg.get('issuing_body', 'Cơ quan quản lý quốc tế')}",
        f"🌍 Thị trường áp dụng: {markets_str}",
        f"📦 Mặt hàng & Mã HS ảnh hưởng: {products_str}",
        f"⚠️ Mức độ rủi ro: {reg.get('risk_level')} — {reg.get('status')}",
        f"⏱️ Mốc thời gian hiệu lực: {reg.get('effective_date')} ({reg.get('horizon_quarter')})",
        "",
        f"📌 Dự báo tình báo & Tác động:",
        f"{reg.get('forecast_notice')}",
        "",
        f"🛡️ HÃNG LUẬT TẬP ĐOÀN KHUYẾN NGHỊ (Project/luat):",
        f"{reg.get('legal_firm_advice')}",
        "",
        f"🚢 KHỐI XNK & LOGISTICS KHUYẾN NGHỊ (Project/XNK):",
        f"{reg.get('logistics_advice')}",
        "",
        f"🤖 TỰ ĐỘNG HÓA ANTIGRAVITY:",
        f"{reg.get('antigravity_automation')}",
        "",
        f"#RadarPhapLy #CanhBaoRuiRo #XNK #HoldingLegal #{reg.get('code').replace(' ', '').replace('/', '')}"
    ]
    return "\n".join(msg_lines)

def dispatch_telegram_risk_alert(reg_id, chat_id=None, dry_run=False):
    """
    Phát lệnh gửi bản tin cảnh báo rủi ro pháp lý tới Telegram
    Có hỗ trợ cờ dry_run=True cho các bài kiểm thử tự động
    """
    target_chat_id = chat_id or DEFAULT_CHAT_ID
    message_text = format_telegram_risk_alert(reg_id)
    
    if dry_run:
        print(f"[DRY_RUN] Chế độ kiểm thử: Bản tin cảnh báo rủi ro {reg_id} đã được biên soạn thành công.")
        return {
            "status": "SUCCESS",
            "dry_run": True,
            "reg_id": reg_id,
            "chat_id": target_chat_id,
            "message_length": len(message_text),
            "preview": message_text[:200]
        }

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": target_chat_id,
            "text": message_text
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp_body = json.loads(resp.read().decode("utf-8"))
            return {
                "status": "SUCCESS",
                "dry_run": False,
                "reg_id": reg_id,
                "chat_id": target_chat_id,
                "telegram_response": resp_body
            }
    except Exception as e:
        print(f"[regulatory_radar] Lỗi gửi Telegram API: {e}")
        return {
            "status": "ERROR",
            "error": str(e),
            "reg_id": reg_id,
            "chat_id": target_chat_id
        }

def assess_compliance_for_lead(lead_dict):
    """
    Tự động thẩm định rủi ro tuân thủ pháp lý cho 1 lead khách hàng hoặc mặt hàng
    Đối soát mã HS và thị trường xuất xứ / điểm đến
    """
    hs = str(lead_dict.get("hs", "")).strip().replace(".", "")
    country = str(lead_dict.get("country", "")).strip().lower()
    
    all_regs = load_regulations()
    matched_risks = []

    for r in all_regs:
        hs_match = any(hs.startswith(ch) for ch in r.get("hs_chapters", []))
        market_match = any(m.lower() in country for m in r.get("markets", [])) or (country in ["vietnam", "viet nam"] and any("eu" in m.lower() or "mỹ" in m.lower() for m in r.get("markets", [])))
        
        if hs_match and market_match:
            matched_risks.append({
                "reg_id": r["id"],
                "code": r["code"],
                "title": r["title_vi"],
                "risk_level": r["risk_level"],
                "effective_date": r["effective_date"],
                "forecast_notice": r["forecast_notice"],
                "legal_advice": r["legal_firm_advice"]
            })

    return {
        "lead_id": lead_dict.get("id", ""),
        "lead_name": lead_dict.get("company_name", ""),
        "total_regulatory_risks": len(matched_risks),
        "highest_risk": "CAO" if any(m["risk_level"] == "CAO" for m in matched_risks) else ("TRUNG BÌNH" if matched_risks else "THẤP"),
        "risks": matched_risks
    }
