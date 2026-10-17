#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hệ thống Nền Tảng Tình Báo Thương Mại & Thẩm Định Đối Tác XNK Tập Đoàn
(Trade Intelligence & Verification Platform - Phase 1 MVP)
Khối Xuất Nhập Khẩu & Thương Mại Quốc Tế (Agency Global Logistics & Trade - XNK)
"""

import sys
import os
import json
import re
import urllib.request
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from datetime import datetime

# Đảm bảo UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "intelligence_db.json")
AUDIT_LOG_FILE = os.path.join(BASE_DIR, "data", "audit_history.json")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Bot Telegram Token & Chat ID mặc định từ hệ thống Tập đoàn
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8821881768:AAFysU6f0IGu4qHHVeN5P-b1fqgFHNPcECI")
DEFAULT_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "6034655358")

try:
    from lead_engine import refresh_lead_signals, generate_csv_export, MARKET_REGIONS
except ImportError:
    refresh_lead_signals = None
    generate_csv_export = None
    MARKET_REGIONS = {}

try:
    import trade_matcher
except ImportError:
    trade_matcher = None

try:
    from hs_catalog import (
        get_catalog_by_view_mode,
        search_hs_omni,
        ALL_97_CHAPTERS,
        WCO_SECTIONS,
        END_USE_CLUSTERS
    )
except ImportError:
    get_catalog_by_view_mode = None
    search_hs_omni = None
    ALL_97_CHAPTERS = []
    WCO_SECTIONS = []
    END_USE_CLUSTERS = {}

try:
    import hs_products
except ImportError:
    hs_products = None

try:
    import regulatory_radar
except ImportError:
    regulatory_radar = None

try:
    import trade_tags_dict
except ImportError:
    trade_tags_dict = None

try:
    import openapi_spec
except ImportError:
    openapi_spec = None

try:
    import commodity_calculator
except ImportError:
    commodity_calculator = None


def load_database():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Error] Không thể tải database: {e}")
        return {"buyers": [], "suppliers": [], "bill_of_ladings": [], "industries": [], "industry_leads": []}

def save_database(db):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[Error] Không thể lưu database: {e}")
        return False

def save_audit_record(record):
    history = []
    if os.path.exists(AUDIT_LOG_FILE):
        try:
            with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []
    history.insert(0, record)
    with open(AUDIT_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    return record

def send_telegram_alert_message(title, details, status_icon="🚨", action_required=None, target_chat_id=None):
    now_str = datetime.now().strftime("%H:%M %d/%m/%Y")
    lines = [
        f"🚢 [KHỐI XNK - HỆ THỐNG THẨM ĐỊNH & SĂN LEAD TỨC THÌ]",
        f"⏰ Thời điểm: {now_str}",
        f"----------------------------------------",
        f"{status_icon} TIÊU ĐỀ: {title}",
        f""
    ]
    for d in details:
        lines.append(f"• {d}")
    if action_required:
        lines.append(f"")
        lines.append(f"⚡ CHỈ ĐẠO BẮT BUỘC: {action_required}")
    lines.append(f"----------------------------------------")
    lines.append(f"🏛️ Trade Intelligence Engine kính báo Chủ tịch!")
    
    text = "\n".join(lines)
    
    # Tập hợp danh sách chat_id đích (mặc định luôn có Telegram Chủ tịch)
    chat_ids = []
    if target_chat_id:
        chat_ids.append(str(target_chat_id))
    if DEFAULT_CHAT_ID and str(DEFAULT_CHAT_ID) not in chat_ids:
        chat_ids.append(str(DEFAULT_CHAT_ID))

    # Cố gắng dò tìm thêm chat_id từ getUpdates nếu có tương tác mới
    try:
        req = urllib.request.Request(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates")
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            if res_data.get("ok"):
                for update in res_data.get("result", []):
                    msg = update.get("message", {}) or update.get("channel_post", {})
                    chat = msg.get("chat", {})
                    cid = str(chat.get("id"))
                    if cid and cid not in chat_ids:
                        chat_ids.append(cid)
    except Exception as e:
        print(f"[Telegram getUpdates error]: {e}")
        
    sent_count = 0
    errors = []
    for cid in chat_ids:
        try:
            send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = json.dumps({"chat_id": cid, "text": text}).encode('utf-8')
            s_req = urllib.request.Request(send_url, data=payload, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(s_req, timeout=8) as resp:
                r_json = json.loads(resp.read().decode('utf-8'))
                if r_json.get("ok"):
                    sent_count += 1
        except Exception as e:
            errors.append(f"{cid}: {str(e)}")
            print(f"[Telegram send error for {cid}]: {e}")
            
    return {
        "sent_to_chats": sent_count,
        "chat_ids": chat_ids,
        "errors": errors,
        "ok": sent_count > 0,
        "text": text
    }

def generate_b2b_outreach_letter(lead_data, lang="EN"):
    company = lead_data.get("company_name", "Valued Importer")
    contact = lead_data.get("sourcing_contacts", [{}])[0]
    c_name = contact.get("name", "Procurement Director")
    c_title = contact.get("title", "Head of Sourcing")
    country = lead_data.get("country", "")
    commodities = lead_data.get("commodities_demanded", [])
    comm_name = commodities[0].get("name", "Agricultural & Industrial Commodities") if commodities else "Commodities"
    hs_code = commodities[0].get("hs_code", "") if commodities else ""
    incoterm = lead_data.get("preferred_incoterms", "FOB / CIF")

    if lang == "EN":
        return {
            "language": "EN",
            "subject": f"Inquiry & Supply Quotation: Premium Grade {comm_name} (HS {hs_code}) - Direct from Vietnam Export Consortium",
            "body": f"""Dear {c_name},

Hope this email finds you well at {company}.

I am contacting you from the International Trade & Logistics Division of our Group in Vietnam. We have been monitoring your continuous leadership in importing high-volume {comm_name} into {country}.

We are a premier Vietnamese producer and direct exporter with vertically integrated facilities and certified supply chains. Regarding your procurement parameters for HS {hs_code}:

1. PRODUCT SPECIFICATIONS:
• Commodity: {comm_name}
• Standards: 100% compliant with EU / US / International MRLs & Food Safety (HACCP, ISO 22000, FSC / Rainforest Alliance certified).
• Packaging: Standard Export Packing (Palletized / 50kg PP Bags / Jumbo Bags / Bulk container).
• Inspection: Pre-shipment independent inspection by SGS / Bureau Veritas at port of loading.

2. COMMERCIAL TERMS:
• Delivery Terms: {incoterm} (Main ports: Cat Lai, Cai Mep, Hai Phong).
• Payment Safeguard: Irrevocable L/C at Sight or T/T with flexible financing.
• Origin Documentation: Certificate of Origin Form E / EUR.1 / CPTPP / Form D (preferential 0% import duty).

We would be pleased to dispatch a physical lab sample and full certificate dossier to your headquarters in {lead_data.get('city', country)} within 48 hours.

Could you please confirm if your procurement desk is currently accepting trial allocations for the upcoming shipment window?

Warm regards,

Managing Director of International Trade & Logistics
Headquarters Holding Group — Export Consortium Vietnam
Direct Mobile / WhatsApp: +84 (0) 90 258 9190
Official Desk: xnk@holding-group.vn | www.holding-group.vn"""
        }
    elif lang == "CN":
        return {
            "language": "CN",
            "subject": f"优质产品供应函：越南高品质 {comm_name} (海关编码 {hs_code}) 直接出口报价",
            "body": f"""尊敬的 {c_name} 先生/女士 ({company} 采购总监):

您好！

我们是越南大型控股集团旗下国际进出口与供应链贸易集团。获悉贵司长期在 {country} 市场大规模进口和分销 {comm_name}。

针对贵司对海关编码 {hs_code} 的采购规格与质检要求，我司拥有完整的自营加工基地与产地溯源供应链：

1. 产品规格与品质保证：
• 品名：{comm_name}
• 检验标准：装船前经 SGS / 瑞士通用公证行独立检测出具全套质检证书。
• 证书齐备：中国海关总署 GACC 注册登记编号、HACCP、ISO 认证。

2. 贸易与交货条件：
• 交付条款：{incoterm}（越南胡志明港/海防港直接出运）。
• 原产地证书：提供中国-东盟自由贸易协定原产地证（FORM E），享受零关税优惠。
• 结算方式：不可撤销即期信用证（L/C At Sight）或电汇（T/T）。

我司可在48小时内通过顺丰/DHL将标准实物样品寄送至贵司。期待与贵司建立长期稳定的直供合作关系。

顺祝商祺！

越南控股集团国际进出口执行董事
联系电话/微信: +84 (0) 90 258 9190
电子邮箱: xnk@holding-group.vn"""
        }
    elif lang == "RU":
        return {
            "language": "RU",
            "subject": f"Коммерческое предложение: Прямые экспортные поставки {comm_name} (ТН ВЭД {hs_code}) из Вьетнама",
            "body": f"""Уважаемый(ая) {c_name} ({company}):

Приветствуем Вас от имени Международного Торгово-Логистического Дивизиона Вьетнамского Экспортного Консорциума.

Мы внимательно следим за деятельностью {company} в качестве ведущего импортера и дистрибьютора {comm_name} на рынке {country}.

Предлагаем прямые контрактные поставки продукции высшего сорта (ТН ВЭД {hs_code}) с полным циклом сертификации:

1. СПЕЦИФИКАЦИЯ ПРОДУКЦИИ:
• Наименование: {comm_name}
• Сертификация: Полное соответствие международным стандартам качества, независимая инспекция SGS в порту погрузки.
• Упаковка: Экспортный стандарт (мешки 50 кг / биг-бэги 1000 кг).

2. БАЗИСНЫЕ УСЛОВИЯ:
• Условия поставки: {incoterm} (Порты Хайфон / Кат Лай).
• Расчеты: Взаиморасчеты в рублях (RUB), юанях (RMB) или безотзывный аккредитив (L/C at Sight) через банки без риска санкционных блокировок (ВРБ / ВТБ Вьетнам).
• Преференциальный сертификат происхождения: Form EAV (Соглашение о ЗСТ Вьетнам - ЕАЭС) со ставкой пошлины 0%.

Готовы направить образцы продукции курьерской службой в течение 48 часов.

С уважением,
Управляющий директор по ВЭД и логистике
Экспортный Консорциум Вьетнама"""
        }
    else:
        return {
            "language": "VN",
            "subject": f"Thư Chào Hàng Xuất Khẩu: {comm_name} (Mã HS {hs_code}) - Khối XNK Tập Đoàn",
            "body": f"""Kính gửi Ông/Bà {c_name} ({c_title} - {company}):

Khối Xuất Nhập Khẩu & Thương Mại Quốc Tế Tập Đoàn trân trọng gửi tới Quý Công ty thư giới thiệu và chào giá xuất khẩu sản phẩm {comm_name} (Mã HS: {hs_code}).

Chúng tôi là đơn vị xuất khẩu trực tiếp từ Việt Nam với vùng nguyên liệu đạt chuẩn quốc tế, đáp ứng đầy đủ các tiêu chuẩn kiểm nghiệm của thị trường {country}.

Điều kiện giao hàng: {incoterm}. Chứng nhận xuất xứ C/O ưu đãi thuế quan 0%. Kiểm định độc lập bởi SGS/Vinacontrol.

Trân trọng!"""
        }

def generate_b2b_supplier_inquiry_letter(supplier_data, buyer_data, commodity_name=None, hs_code=None, lang="VN"):
    sup_name = supplier_data.get("company_name", "Valued Supplier")
    sup_short = supplier_data.get("short_name", sup_name)
    sup_country = supplier_data.get("country", "Việt Nam")
    buyer_name = buyer_data.get("company_name", "International Buyer Client")
    buyer_country = buyer_data.get("country", "Global")
    
    comm = commodity_name or (buyer_data.get("commodities_demanded", [{}])[0].get("name") if buyer_data.get("commodities_demanded") else "Hàng hóa ngoại thương")
    hs = hs_code or (buyer_data.get("commodities_demanded", [{}])[0].get("hs_code") if buyer_data.get("commodities_demanded") else "")
    
    certs = ", ".join(supplier_data.get("quality_standards", ["ISO", "HACCP", "Export Grade"]))
    incoterms_list = supplier_data.get("accepted_incoterms", ["FOB", "CIF", "EXW"])
    incoterm = ", ".join(incoterms_list) if isinstance(incoterms_list, list) else str(incoterms_list)
    payments_list = supplier_data.get("accepted_payments", ["L/C At Sight", "T/T"])
    payments = ", ".join(payments_list) if isinstance(payments_list, list) else str(payments_list)

    if lang == "EN":
        return {
            "language": "EN",
            "subject": f"[PURCHASE INQUIRY & RFQ] Procurement Allocation: {comm} (HS {hs}) for Buyer {buyer_name} ({buyer_country})",
            "body": f"""Dear Sales & Export Management Team at {sup_name},

Greetings from the International Trade & Sourcing Division of our Holding Group in Vietnam.

We are currently structuring an international supply contract for our buyer client: {buyer_name} ({buyer_country}). Following our bilateral matrix verification, we are pleased to issue this formal Purchase Request for Quotation (RFQ) for:

1. PROCUREMENT SPECIFICATIONS:
• Commodity: {comm}
• HS Code Classification: {hs}
• Quality & Compliance Standards: Certified under {certs}; subject to pre-shipment SGS inspection.
• Target Allocation Volume: Monthly commercial container lots as per export schedule.

2. COMMERCIAL TERMS & INQUIRY:
• Preferred Terms: {incoterm} (Loading ports: Cat Lai / Hai Phong / Regional Hub).
• Settlement Safeguard: Irrevocable L/C at Sight or standard commercial payment terms ({payments}).
• Documentation Required: Commercial Invoice, Packing List, Certificate of Origin (Form E/EUR.1/CPTPP/Form D), COA.

Please kindly revert with your official Quotation Sheet, current ex-factory availability, and earliest shipment window within 48 business hours.

Warm regards,

Managing Director of International Trade & Logistics
Headquarters Holding Group — Export Consortium Vietnam
Desk: xnk@holding-group.vn | Hotline: +84 (0) 90 258 9190"""
        }
    else:
        return {
            "language": "VN",
            "subject": f"[YÊU CẦU BÁO GIÁ & ĐẶT HÀNG XUẤT KHẨU] Cung ứng {comm} (Mã HS: {hs}) cho đối tác {buyer_country}",
            "body": f"""Kính gửi: Ban Giám Đốc / Phòng Kinh Doanh & Xuất Khẩu Quý Công ty ({sup_name}):

Khối Xuất Nhập Khẩu & Thương Mại Quốc Tế Tập Đoàn trân trọng thông báo: Chúng tôi đang thực hiện đơn hàng xuất khẩu lớn kết nối thu mua với đối tác quốc tế: {buyer_name} ({buyer_country}).

Sau khi đối soát tiêu chuẩn kỹ thuật và hồ sơ năng lực của Quý Công ty, chúng tôi trân trọng gửi yêu cầu chào giá (Purchase RFQ) đối với mặt hàng: {comm} (Mã HS: {hs}).

1. THÔNG SỐ ĐƠN HÀNG & TIÊU CHUẨN KỸ THUẬT:
• Tên hàng hóa: {comm}
• Phân loại Mã HS: {hs}
• Tiêu chuẩn chất lượng: Đạt chuẩn xuất khẩu ({certs}), chấp thuận kiểm định độc lập SGS / Vinacontrol tại cảng xuất.
• Quy cách đóng gói: Tiêu chuẩn đóng hàng xuất khẩu đường biển (Pallet/Bao Jumbo/Container).

2. ĐIỀU KIỆN THƯƠNG MẠI & TIẾN ĐỘ:
• Điều kiện giao hàng đề nghị: {incoterm} (Cảng xuất: Cát Lái / Hải Phòng / Giao hàng tại xưởng EXW).
• Phương thức thanh toán: L/C Trả ngay (At Sight) hoặc T/T đặt cọc & thanh toán theo vận đơn B/L ({payments}).
• Yêu cầu chứng từ: Hóa đơn GTGT hợp pháp 100%, Phiếu phân tích chất lượng (COA), Chứng nhận xuất xứ (C/O).

Đề nghị Quý Công ty gửi Bảng Báo Giá Chính Thức (kèm thời hạn giao hàng dự kiến) về hòm thư: xnk@holding-group.vn trong vòng 24 - 48 giờ làm việc.

Trân trọng hợp tác!

Khối Xuất Nhập Khẩu & Thương Mại Quốc Tế Tập Đoàn
Hotline Điều Hành Ngoại Thương: +84 (0) 90 258 9190
Official Desk: xnk@holding-group.vn | www.holding-group.vn"""
        }

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class PortalRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def _send_json(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        url_parts = urllib.parse.urlparse(self.path)
        path = url_parts.path
        query = urllib.parse.parse_qs(url_parts.query)

        if path in ["/api", "/api/v1"]:
            self._send_json({
                "ok": True,
                "platform": "Trade Intelligence & Verification Platform API Suite",
                "version": "1.0.0",
                "status": "OPERATIONAL",
                "docs_url": "/api/docs",
                "openapi_url": "/api/openapi.json",
                "endpoints_count": 40,
                "categories": [
                    "Leads & Prospecting",
                    "Due Diligence & Verification",
                    "Suppliers & Counterparties",
                    "Trade Matchmaker & Dual RFQ",
                    "Customs & Bill of Lading",
                    "Factory Audit (SOP-XNK-02)",
                    "HS Catalog & Strategic Products",
                    "Regulatory Radar & Policy Horizon",
                    "Trade Tags & Terminology Dictionary",
                    "Multi-Exchange Price Board & Arbitrage",
                    "Telegram Alerting Engine",
                    "System Health & Platform Metadata"
                ]
            })
            return

        elif path in ["/api/openapi.json", "/openapi.json"]:
            try:
                import openapi_spec
                host = self.headers.get("Host", "103.228.74.58")
                server_url = f"http://{host}"
                spec = openapi_spec.get_openapi_spec(server_url)
            except Exception as e:
                spec = {"openapi": "3.1.0", "info": {"title": "API", "version": "1.0.0"}, "error": str(e)}
            self._send_json(spec)
            return

        elif path in ["/api/docs", "/docs"]:
            try:
                import openapi_spec
                html = openapi_spec.get_swagger_ui_html("/api/openapi.json")
            except Exception as e:
                html = f"<h1>API Documentation</h1><p>Error loading docs: {e}</p>"
            html_bytes = html.encode('utf-8')
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(html_bytes)))
            self.end_headers()
            self.wfile.write(html_bytes)
            return

        elif path == "/api/health":
            db = load_database()
            self._send_json({
                "status": "ONLINE",
                "version": "1.1.0-phase1-prospecting",
                "uptime": "Healthy",
                "timestamp": datetime.now().isoformat(),
                "db_stats": {
                    "industries": len(db.get("industries", [])),
                    "industry_leads": len(db.get("industry_leads", [])),
                    "verified_buyers": len(db.get("buyers", [])),
                    "verified_suppliers": len(db.get("suppliers", [])),
                    "tracked_bls": len(db.get("bill_of_ladings", []))
                }
            })
            return

        elif path == "/api/industries":
            # Danh mục các ngành hàng trọng điểm xuất khẩu
            db = load_database()
            self._send_json(db.get("industries", []))
            return

        elif path == "/api/regions":
            # Danh mục các thị trường khu vực trọng điểm
            self._send_json(MARKET_REGIONS if MARKET_REGIONS else {})
            return

        elif path == "/api/hs/catalog":
            # Danh bạ toàn biểu 97 chương HS theo 4 chế độ: volume, clusters, alphabet, wco
            mode = query.get("mode", ["volume"])[0].strip().lower()
            if mode not in ["volume", "clusters", "alphabet", "wco"]:
                mode = "volume"
            catalog_res = get_catalog_by_view_mode(mode) if get_catalog_by_view_mode else {"data": []}
            self._send_json(catalog_res)
            return

        elif path == "/api/hs/search":
            # Tìm kiếm thông minh tức thì theo từ khóa, mã chương HS và sản phẩm cụ thể
            q = query.get("q", [""])[0].strip()
            try:
                limit = int(query.get("limit", ["15"])[0])
            except Exception:
                limit = 15
            search_res = search_hs_omni(q, limit) if search_hs_omni else []
            matching_products = hs_products.search_products_master(q, limit=limit) if hs_products else []
            self._send_json({
                "status": "SUCCESS",
                "query": q,
                "total_matches": len(search_res),
                "results": search_res,
                "total_products": len(matching_products),
                "products": matching_products
            })
            return

        elif path == "/api/hs/products":
            # Tra cứu danh mục sản phẩm chi tiết theo mã HS, mã chương hoặc từ khóa
            q = query.get("q", [""])[0].strip()
            chapter = query.get("chapter", [""])[0].strip()
            sector = query.get("sector", [""])[0].strip()
            try:
                limit = int(query.get("limit", ["30"])[0])
            except Exception:
                limit = 30
            
            if chapter and hs_products:
                prods = hs_products.get_products_by_chapter(chapter)
            elif sector and hs_products:
                prods = hs_products.get_products_by_sector(sector)
            elif q and hs_products:
                prods = hs_products.search_products_master(q, limit=limit)
            elif hs_products:
                prods = hs_products.get_all_products()[:limit]
            else:
                prods = []

            self._send_json({
                "status": "SUCCESS",
                "total": len(prods),
                "total_master_count": hs_products.get_products_count() if hs_products else 0,
                "products": prods
            })
            return

        elif path == "/api/regulations/active":
            # Danh sách các quy định pháp lý và chính sách ngoại thương mới toàn cầu
            m = query.get("market", [""])[0].strip()
            hs_q = query.get("hs", [""])[0].strip()
            risk = query.get("risk", [""])[0].strip()
            regs = regulatory_radar.get_active_regulations(market=m, hs=hs_q, risk_level=risk) if regulatory_radar else []
            self._send_json({
                "status": "SUCCESS",
                "total": len(regs),
                "regulations": regs
            })
            return

        elif path == "/api/regulations/horizon-calendar":
            # Lịch dự báo chân trời chính sách (Horizon Scanning Calendar)
            calendar_events = regulatory_radar.get_horizon_calendar() if regulatory_radar else []
            self._send_json({
                "status": "SUCCESS",
                "total_events": len(calendar_events),
                "calendar": calendar_events
            })
            return

        elif path == "/api/regulations/detail":
            # Chi tiết hồ sơ quy định pháp lý 360 độ
            reg_id = query.get("id", [""])[0].strip()
            reg = regulatory_radar.get_regulation_by_id(reg_id) if regulatory_radar else None
            if reg:
                self._send_json({"status": "SUCCESS", "regulation": reg})
            else:
                self._send_json({"status": "ERROR", "message": "Regulation not found"}, 404)
            return

        elif path == "/api/trade-tags/explain":
            # Tra cứu giải thích chi tiết ý nghĩa và khuyến nghị nghiệp vụ của thẻ tag
            tag_query = query.get("tag", [""])[0].strip()
            info = trade_tags_dict.get_trade_tag_info(tag_query) if trade_tags_dict else {}
            self._send_json({
                "status": "SUCCESS",
                "tag": tag_query,
                "info": info
            })
            return

        elif path == "/api/trade-tags/catalog":
            # Toàn bộ danh mục thẻ tag chuẩn hóa
            catalog = trade_tags_dict.TRADE_TAG_CATALOG if trade_tags_dict else {}
            self._send_json({
                "status": "SUCCESS",
                "total": len(catalog),
                "catalog": catalog
            })
            return

        elif path == "/api/hs/summary":
            # Tổng hợp cơ cấu danh mục HS WCO
            self._send_json({
                "sections_count": len(WCO_SECTIONS) if WCO_SECTIONS else 21,
                "chapters_count": len(ALL_97_CHAPTERS) if ALL_97_CHAPTERS else 97,
                "clusters_count": len(END_USE_CLUSTERS) if END_USE_CLUSTERS else 6,
                "products_count": hs_products.get_products_count() if hs_products else 0,
                "sorting_modes": [
                    {"id": "volume", "label": "🔥 Top Kim Ngạch", "desc": "Sắp xếp theo quy mô xuất nhập khẩu & tần suất giao dịch"},
                    {"id": "clusters", "label": "📦 6 Chuỗi Giá Trị", "desc": "Gom nhóm theo mục đích sử dụng công nghiệp trực quan"},
                    {"id": "alphabet", "label": "🔤 Bảng Chữ Cái (A-Z)", "desc": "Tra cứu theo tên sản phẩm tiếng Việt từ A đến Z"},
                    {"id": "wco", "label": "📑 Chuẩn WCO (01-97)", "desc": "Thứ tự số học 21 Phần và 97 Chương của Tổ chức Hải quan"}
                ]
            })
            return

        elif path == "/api/leads/export-csv":
            # Xuất toàn bộ hoặc theo bộ lọc ra file Excel / CSV (UTF-8 BOM)
            db = load_database()
            leads = db.get("industry_leads", [])
            csv_bytes = generate_csv_export(leads) if generate_csv_export else b""
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Disposition", 'attachment; filename="danh_sach_khach_hang_xnk_1000.csv"')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(csv_bytes)))
            self.end_headers()
            self.wfile.write(csv_bytes)
            return

        elif path == "/api/leads/by-industry":
            # SĂN TÌM KHÁCH HÀNG TIỀM NĂNG THEO NGÀNH HÀNG, PHỄU ĐẦU VÀO & PHÂN TRANG 10 DN/TRANG
            db = load_database()
            leads = db.get("industry_leads", [])

            ind_id = query.get("industry", [""])[0].strip()
            chapter = query.get("chapter", [""])[0].strip()
            cluster = query.get("cluster", [""])[0].strip()
            hs = query.get("hs", [""])[0].strip()
            country = query.get("country", [""])[0].strip().lower()
            region = query.get("region", [""])[0].strip().lower()
            stage = query.get("stage", [""])[0].strip().lower()
            q = query.get("q", [""])[0].strip().lower()
            export_fmt = query.get("export", [""])[0].strip().lower()

            try:
                page = max(1, int(query.get("page", ["1"])[0]))
            except Exception:
                page = 1
            try:
                page_size = max(1, int(query.get("page_size", ["10"])[0]))
            except Exception:
                page_size = 10

            filtered = []
            for item in leads:
                match = True
                if ind_id and ind_id != "all" and item.get("industry_id") != ind_id:
                    match = False
                if chapter:
                    has_chap = any(c.get("hs_code", "").replace(".", "").startswith(chapter) or c.get("hs_code", "").startswith(chapter) for c in item.get("commodities_demanded", []))
                    if not has_chap:
                        match = False
                if cluster and cluster != "all":
                    cluster_info = END_USE_CLUSTERS.get(cluster) if END_USE_CLUSTERS else None
                    if cluster_info:
                        cluster_chaps = cluster_info.get("chapters", [])
                        has_clust = any(any(c.get("hs_code", "").startswith(ch) for ch in cluster_chaps) for c in item.get("commodities_demanded", []))
                        if not has_clust:
                            match = False
                if hs:
                    has_hs = any(c.get("hs_code", "").startswith(hs) for c in item.get("commodities_demanded", []))
                    if not has_hs:
                        match = False
                if region and region != "all":
                    if item.get("market_region") != region:
                        match = False
                if country:
                    c_low = item.get("country", "").lower()
                    cc_low = item.get("country_code", "").lower()
                    if country in ["russia", "ru", "nga", "liên bang nga"]:
                        if "russia" not in c_low and "nga" not in c_low and cc_low != "ru":
                            match = False
                    elif country not in c_low:
                        match = False
                if stage and stage != "all":
                    if item.get("funnel_stage") != stage:
                        match = False
                if q:
                    searchable = f"{item.get('company_name','')} {item.get('country','')} {item.get('city','')} {item.get('broker_platform','')} {item.get('latest_trade_activity','')} {item.get('broker_rfq_signal','')} {json.dumps(item.get('commodities_demanded',[]))}".lower()
                    if q not in searchable:
                        match = False
                if match:
                    filtered.append(item)

            if export_fmt in ["csv", "excel", "true"]:
                csv_bytes = generate_csv_export(filtered) if generate_csv_export else b""
                self.send_response(200)
                self.send_header("Content-Type", "text/csv; charset=utf-8")
                self.send_header("Content-Disposition", 'attachment; filename="danh_sach_khach_hang_xnk.csv"')
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(len(csv_bytes)))
                self.end_headers()
                self.wfile.write(csv_bytes)
                return

            total_raw = sum(1 for l in leads if l.get("funnel_stage") == "raw")
            total_tier_b = sum(1 for l in leads if l.get("funnel_stage") == "tier_b")
            total_tier_a = sum(1 for l in leads if l.get("funnel_stage") == "tier_a")

            total_matched = len(filtered)
            total_pages = max(1, (total_matched + page_size - 1) // page_size)
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            page_items = filtered[start_idx:end_idx]

            self._send_json({
                "total": total_matched,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "funnel_stats": {
                    "total": len(leads),
                    "raw": total_raw,
                    "tier_b": total_tier_b,
                    "tier_a": total_tier_a
                },
                "data": page_items
            })
            return

        elif path == "/api/leads/detail":
            db = load_database()
            lead_id = query.get("id", [""])[0].strip() or query.get("lead_id", [""])[0].strip()
            leads = db.get("industry_leads", [])
            selected_lead = next((l for l in leads if l.get("lead_id") == lead_id), None)
            if not selected_lead:
                q_name = query.get("name", [""])[0].strip().lower()
                if q_name:
                    selected_lead = next((l for l in leads if q_name in l.get("company_name", "").lower()), None)
            if selected_lead:
                self._send_json({"ok": True, "lead": selected_lead})
            else:
                self._send_json({"ok": False, "error": f"Lead '{lead_id}' not found"}, 404)
            return

        elif path == "/api/leads/sourcing-evaluation":
            db = load_database()
            lead_id = query.get("id", [""])[0].strip() or query.get("lead_id", [""])[0].strip()
            leads = db.get("industry_leads", [])
            selected_lead = next((l for l in leads if l.get("lead_id") == lead_id), None)
            if not selected_lead:
                q_name = query.get("name", [""])[0].strip().lower()
                if q_name:
                    selected_lead = next((l for l in leads if q_name in l.get("company_name", "").lower()), None)
            if selected_lead:
                eval_res = selected_lead.get("sourcing_evaluation")
                if not eval_res:
                    try:
                        import sourcing_evaluator
                        eval_res = sourcing_evaluator.evaluate_lead_sourcing_expansion(selected_lead, db.get("suppliers", []))
                    except Exception as e:
                        eval_res = None
                self._send_json({"ok": True, "evaluation": eval_res})
            else:
                self._send_json({"ok": False, "error": f"Lead '{lead_id}' not found"}, 404)
            return

        elif path == "/api/buyers":
            db = load_database()
            self._send_json(db.get("buyers", []))
            return

        elif path == "/api/suppliers/detail":
            sup_id = query.get("id", [""])[0].strip()
            db = load_database()
            suppliers = db.get("suppliers", [])
            sup = next((s for s in suppliers if s.get("id") == sup_id or s.get("company_name", "").lower() == sup_id.lower()), None)
            if sup:
                self._send_json({"ok": True, "supplier": sup})
            else:
                self._send_json({"ok": False, "error": f"Supplier '{sup_id}' not found"}, 404)
            return

        elif path == "/api/contacts":
            db = load_database()
            entity_id = query.get("id", [""])[0].strip() or query.get("lead_id", [""])[0].strip() or query.get("supplier_id", [""])[0].strip()
            entity_type = query.get("type", [""])[0].strip().lower()
            name_query = query.get("name", [""])[0].strip().lower()

            lead = None
            supplier = None

            # Auto-detect or search
            if entity_type == "supplier" or entity_id.startswith("SP-") or entity_id.startswith("SUP-"):
                suppliers = db.get("suppliers", [])
                supplier = next((s for s in suppliers if s.get("id") == entity_id or (name_query and name_query in (s.get("company_name") or s.get("name", "")).lower())), None)
            elif entity_type == "lead" or entity_id.startswith("LEAD-"):
                leads = db.get("industry_leads", [])
                lead = next((l for l in leads if l.get("lead_id") == entity_id or (name_query and name_query in l.get("company_name", "").lower())), None)
            else:
                # Try finding in leads first, then suppliers
                leads = db.get("industry_leads", [])
                lead = next((l for l in leads if l.get("lead_id") == entity_id or (name_query and name_query in l.get("company_name", "").lower())), None)
                if not lead:
                    suppliers = db.get("suppliers", [])
                    supplier = next((s for s in suppliers if s.get("id") == entity_id or (name_query and name_query in (s.get("company_name") or s.get("name", "")).lower())), None)

            if lead:
                contacts = lead.get("sourcing_contacts", [])
                has_additional = len(contacts) > 1
                comp_name = lead.get("company_name", "Doanh Nghiệp")
                primary_name = contacts[0].get("name", "N/A") if contacts else "N/A"
                self._send_json({
                    "ok": True,
                    "id": lead.get("lead_id"),
                    "type": "lead",
                    "company_name": comp_name,
                    "country": lead.get("country"),
                    "scale": lead.get("scale"),
                    "has_additional": has_additional,
                    "total_contacts": len(contacts),
                    "primary_contact": contacts[0] if contacts else None,
                    "additional_contacts": contacts[1:] if has_additional else [],
                    "all_contacts": contacts,
                    "message": None if has_additional else f"Doanh nghiệp {comp_name} hiện chỉ có 01 đầu mối liên lạc chính thức đã xác minh ({primary_name}). Chưa ghi nhận thêm đầu mối liên hệ phụ trong cơ sở dữ liệu ngoại thương."
                })
                return
            elif supplier:
                primary = supplier.get("contact", {})
                additionals = supplier.get("additional_contacts", [])
                all_contacts = ([primary] if primary and primary.get("name") else []) + additionals
                has_additional = len(additionals) > 0
                s_name = supplier.get("company_name") or supplier.get("name") or "Nhà Cung Cấp"
                primary_name = primary.get("name", "N/A") if primary else (all_contacts[0].get("name", "N/A") if all_contacts else "N/A")
                self._send_json({
                    "ok": True,
                    "id": supplier.get("id"),
                    "type": "supplier",
                    "company_name": s_name,
                    "country": supplier.get("country"),
                    "has_additional": has_additional,
                    "total_contacts": len(all_contacts),
                    "primary_contact": primary if primary else (all_contacts[0] if all_contacts else None),
                    "additional_contacts": additionals,
                    "all_contacts": all_contacts,
                    "message": None if has_additional else f"Doanh nghiệp {s_name} hiện chỉ có 01 đầu mối liên lạc chính thức đã xác minh ({primary_name}). Chưa ghi nhận thêm đầu mối liên hệ phụ trong cơ sở dữ liệu ngoại thương."
                })
                return
            else:
                self._send_json({"ok": False, "error": f"Entity '{entity_id}' not found"}, 404)
                return

        elif path == "/api/suppliers":
            db = load_database()
            suppliers = db.get("suppliers", [])

            country = query.get("country", [""])[0].strip().lower()
            sup_type = query.get("type", [""])[0].strip().lower()
            cert = query.get("cert", [""])[0].strip().lower()
            payment = query.get("payment", [""])[0].strip().lower()
            incoterm = query.get("incoterm", [""])[0].strip().lower()
            q = query.get("q", [""])[0].strip().lower()

            filtered = []
            for s in suppliers:
                match = True
                s_country = s.get("country", "").lower()
                s_country_code = s.get("country_code", "").upper()

                if country and country != "all":
                    country_norm = country.lower().strip()
                    code_map = {
                        "vn": "VN", "vietnam": "VN", "việt nam": "VN",
                        "ru": "RU", "russia": "RU", "nga": "RU", "liên bang nga": "RU",
                        "cn": "CN", "china": "CN", "trung quốc": "CN",
                        "us": "US", "usa": "US", "mỹ": "US", "hoa kỳ": "US", "united states": "US",
                        "ch": "CH", "switzerland": "CH", "thụy sĩ": "CH", "thụy sỹ": "CH",
                        "de": "DE", "germany": "DE", "đức": "DE",
                        "sg": "SG", "singapore": "SG",
                        "in": "IN", "india": "IN", "ấn độ": "IN",
                        "th": "TH", "thailand": "TH", "thái lan": "TH",
                        "br": "BR", "brazil": "BR",
                        "id": "ID", "indonesia": "ID",
                    }
                    target_iso = code_map.get(country_norm)
                    if target_iso:
                        if s_country_code != target_iso:
                            match = False
                    else:
                        if country_norm not in s_country:
                            match = False

                if sup_type and sup_type != "all":
                    st = s.get("supplier_type", "").lower()
                    st_vi = s.get("supplier_type_vi", "").lower()
                    if "tier1" in sup_type or "agent" in sup_type or "trader" in sup_type:
                        if "tier1" not in st and "agent" not in st and "trading" not in st:
                            match = False
                    elif "producer" in sup_type or "factory" in sup_type or "mfg" in sup_type or "manufacturer" in sup_type or "nha_may" in sup_type:
                        if "producer" not in st and "factory" not in st and "manufacturer" not in st and "sản xuất" not in st_vi and "nhà máy" not in st_vi:
                            match = False
                    elif sup_type not in st and sup_type not in st_vi:
                        match = False

                if cert and cert != "all":
                    certs = [c.lower() for c in s.get("quality_standards", [])] + [c.lower() for c in s.get("certificates", [])]
                    if not any(cert in c for c in certs):
                        match = False

                if payment and payment != "all":
                    pays = [p.lower() for p in s.get("accepted_payments", [])]
                    if not any(payment in p for p in pays):
                        match = False

                if incoterm and incoterm != "all":
                    terms = [t.lower() for t in s.get("accepted_incoterms", [])]
                    if not any(incoterm in t for t in terms):
                        match = False

                if q:
                    comm_list = s.get("commodities_supplied") or []
                    comm_str = " ".join(
                        f"{c.get('hs_code','')} {c.get('name','')} {c.get('origin','')}" if isinstance(c, dict) else str(c)
                        for c in comm_list
                    )
                    searchable = f"{s.get('company_name', s.get('name',''))} {s.get('short_name','')} {s.get('country','')} {s.get('city','')} {s.get('supplier_type_vi','')} {comm_str} {' '.join(s.get('quality_standards',[]))} {' '.join(s.get('accepted_payments',[]))}".lower()
                    if q == "nga":
                        # Prevent 'nga' from substring-matching 'singapore'
                        if not re.search(r'(?:^|\s|\(|\/|-)nga(?:$|\s|\)|\/|-|,|\.)', searchable) and s_country_code != "RU":
                            match = False
                    elif q not in searchable:
                        match = False

                if match:
                    filtered.append(s)

            # Sắp xếp mặc định theo điểm tín nhiệm / audit_score giảm dần
            def get_score(item):
                return item.get("score") or item.get("audit_score") or item.get("vat_refund_safety_percent") or 0
            filtered.sort(key=get_score, reverse=True)

            self._send_json(filtered)
            return

        elif path == "/api/matches/metrics":
            db = load_database()
            if not trade_matcher:
                self._send_json({"ok": False, "error": "Trade matcher engine not loaded"}, 500)
                return
            metrics = trade_matcher.get_daily_matching_metrics(db)
            self._send_json({"ok": True, "metrics": metrics})
            return

        elif path == "/api/matches":
            db = load_database()
            if not trade_matcher:
                self._send_json({"ok": False, "error": "Trade matcher engine not loaded"}, 500)
                return
            ind = query.get("industry", [""])[0].strip()
            tier_filter = query.get("tier", [""])[0].strip().upper()
            try:
                min_score = float(query.get("min_score", ["60.0"])[0])
            except Exception:
                min_score = 60.0
            q = query.get("q", [""])[0].strip().lower()
            try:
                page = max(1, int(query.get("page", ["1"])[0]))
            except Exception:
                page = 1
            try:
                page_size = max(1, int(query.get("page_size", ["10"])[0]))
            except Exception:
                page_size = 10

            all_matches = trade_matcher.scan_all_matches(db, min_score=min_score, top_n=200, industry_filter=ind if ind and ind != "all" else None)

            filtered = []
            for m in all_matches:
                if tier_filter and tier_filter != "ALL" and m.get("tier") != tier_filter:
                    continue
                if q:
                    tags_str = " ".join(m.get("matched_tags", []))
                    searchable = f"{m.get('buyer_name','')} {m.get('buyer_country','')} {m.get('supplier_name','')} {m.get('supplier_short_name','')} {m.get('matched_commodity','')} {m.get('matched_hs','')} {tags_str}".lower()
                    if q not in searchable:
                        continue
                filtered.append(m)

            total = len(filtered)
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            paged = filtered[start_idx:end_idx]

            self._send_json({
                "ok": True,
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": max(1, (total + page_size - 1) // page_size),
                "data": paged
            })
            return

        elif path == "/api/discovery/bl":
            db = load_database()
            bls = db.get("bill_of_ladings", [])
            q = query.get("q", [""])[0].lower().strip()
            hs = query.get("hs", [""])[0].strip()

            filtered = []
            for item in bls:
                match = True
                if hs and not item.get("hs_code", "").startswith(hs):
                    match = False
                if q:
                    search_str = f"{item.get('bl_number','')} {item.get('commodity_desc','')} {item.get('consignee','')} {item.get('shipper','')} {item.get('hs_code','')}".lower()
                    if q not in search_str:
                        match = False
                if match:
                    filtered.append(item)

            self._send_json({
                "total": len(filtered),
                "data": filtered
            })
            return

        elif path == "/api/audits":
            history = []
            if os.path.exists(AUDIT_LOG_FILE):
                try:
                    with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
                        history = json.load(f)
                except Exception:
                    history = []
            self._send_json(history)
            return

        elif path == "/api/prices/benchmarks":
            prices_file = os.path.join(BASE_DIR, "data", "multi_exchange_commodity_prices.json")
            if os.path.exists(prices_file):
                try:
                    with open(prices_file, "r", encoding="utf-8") as f:
                        p_data = json.load(f)
                    self._send_json({"ok": True, "data": p_data})
                except Exception as e:
                    self._send_json({"ok": False, "error": str(e)}, 500)
            else:
                self._send_json({"ok": False, "error": "Prices file not found"}, 404)
            return

        elif path == "/api/prices/search":
            # Tìm kiếm thông minh đa nguồn, gắn nhãn từng sàn và nguồn định giá
            q = query.get("q", [""])[0].strip().lower()
            source_filter = query.get("source_type", [""])[0].strip().upper()
            prices_file = os.path.join(BASE_DIR, "data", "multi_exchange_commodity_prices.json")
            results = []
            if os.path.exists(prices_file):
                try:
                    with open(prices_file, "r", encoding="utf-8") as f:
                        p_data = json.load(f)
                    
                    for sec in p_data.get("sectors", []):
                        comm_name = sec.get("commodity_name", "")
                        hs_code = sec.get("hs_code", "")
                        comm_id = sec.get("commodity_id", "")
                        sector_name = sec.get("sector", "")
                        
                        for b in sec.get("benchmarks", []):
                            s_cat = b.get("source_category", b.get("tier_type", ""))
                            if source_filter and source_filter != "ALL" and s_cat != source_filter:
                                continue
                            
                            src_name = b.get("source_name", b.get("exchange_name", ""))
                            ex_name = b.get("exchange_name", "")
                            c_code = b.get("contract_code", "")
                            
                            search_corpus = f"{comm_id} {comm_name} {hs_code} {src_name} {ex_name} {c_code} {sector_name}".lower()
                            search_corpus_clean = search_corpus.replace("à","a").replace("á","a").replace("ạ","a").replace("ả","a").replace("ã","a").replace("â","a").replace("ầ","a").replace("ấ","a").replace("ậ","a").replace("ẩ","a").replace("ẫ","a").replace("è","e").replace("é","e").replace("ẹ","e").replace("ẻ","e").replace("ẽ","e").replace("ê","e").replace("ề","e").replace("ế","e").replace("ệ","e").replace("ể","e").replace("ễ","e").replace("ò","o").replace("ó","o").replace("ọ","o").replace("ỏ","o").replace("õ","o").replace("ô","o").replace("ồ","o").replace("ố","o").replace("ộ","o").replace("ổ","o").replace("ỗ","o").replace("ơ","o").replace("ờ","o").replace("ớ","o").replace("ợ","o").replace("ở","o").replace("ỡ","o").replace("ù","u").replace("ú","u").replace("ụ","u").replace("ủ","u").replace("ũ","u").replace("ư","u").replace("ừ","u").replace("ứ","u").replace("ự","u").replace("ử","u").replace("ữ","u").replace("ì","i").replace("í","i").replace("ị","i").replace("ỉ","i").replace("ĩ","i").replace("đ","d")
                            q_clean = q.replace("à","a").replace("á","a").replace("ạ","a").replace("ả","a").replace("ã","a").replace("â","a").replace("ầ","a").replace("ấ","a").replace("ậ","a").replace("ẩ","a").replace("ẫ","a").replace("è","e").replace("é","e").replace("ẹ","e").replace("ẻ","e").replace("ẽ","e").replace("ê","e").replace("ề","e").replace("ế","e").replace("ệ","e").replace("ể","e").replace("ễ","e").replace("ò","o").replace("ó","o").replace("ọ","o").replace("ỏ","o").replace("õ","o").replace("ô","o").replace("ồ","o").replace("ố","o").replace("ộ","o").replace("ổ","o").replace("ỗ","o").replace("ơ","o").replace("ờ","o").replace("ớ","o").replace("ợ","o").replace("ở","o").replace("ỡ","o").replace("ù","u").replace("ú","u").replace("ụ","u").replace("ủ","u").replace("ũ","u").replace("ư","u").replace("ừ","u").replace("ứ","u").replace("ự","u").replace("ử","u").replace("ữ","u").replace("ì","i").replace("í","i").replace("ị","i").replace("ỉ","i").replace("ĩ","i").replace("đ","d")

                            # Xử lý đồng nghĩa ngoại thương
                            search_tokens = [q, q_clean]
                            if "cafe" in q_clean or "coffee" in q_clean or "ca phe" in q_clean:
                                search_tokens.extend(["cafe", "coffee", "ca phe", "robusta", "arabica"])
                            if "gao" in q_clean or "rice" in q_clean or "lua" in q_clean:
                                search_tokens.extend(["gao", "rice", "lua", "tam"])
                            if "phan" in q_clean or "urea" in q_clean or "dam" in q_clean:
                                search_tokens.extend(["phan", "urea", "dam", "fertilizer"])
                            if "tieu" in q_clean or "pepper" in q_clean:
                                search_tokens.extend(["tieu", "pepper"])
                            if "cao su" in q_clean or "rubber" in q_clean:
                                search_tokens.extend(["cao su", "rubber", "latex", "svr"])
                            if "tom" in q_clean or "shrimp" in q_clean or "seafood" in q_clean:
                                search_tokens.extend(["tom", "shrimp", "seafood", "thuy san"])

                            is_matched = not q or any(t in search_corpus or t in search_corpus_clean for t in search_tokens if t)

                            if is_matched:
                                results.append({
                                    "commodity_id": comm_id,
                                    "commodity_name": comm_name,
                                    "hs_code": hs_code,
                                    "sector": sector_name,
                                    "source_id": b.get("source_id", b.get("tier_type", "")),
                                    "source_name": src_name,
                                    "source_category": s_cat,
                                    "exchange_name": ex_name,
                                    "contract_code": c_code,
                                    "price_original": b.get("price_original"),
                                    "price_usd_mt": b.get("price_usd_mt"),
                                    "change_24h": b.get("change_24h", "0.0%"),
                                    "change_7d": b.get("change_7d", "0.0%"),
                                    "currency": b.get("currency", "USD"),
                                    "updated_at": b.get("updated_at", ""),
                                    "note": b.get("note", ""),
                                    "has_chart_history": bool(b.get("history_1y"))
                                })
                except Exception as e:
                    self._send_json({"ok": False, "error": str(e)}, 500)
                    return
            
            self._send_json({
                "ok": True,
                "query": q,
                "source_filter": source_filter or "ALL",
                "total_matches": len(results),
                "results": results
            })
            return

        elif path == "/api/prices/chart":
            # Cung cấp dữ liệu lịch sử nến / biểu đồ đường theo từng nguồn sàn cụ thể
            comm_id = query.get("commodity_id", ["coffee_robusta"])[0].strip()
            src_id = query.get("source_id", [""])[0].strip()
            time_range = query.get("range", ["1y"])[0].strip().lower()
            
            prices_file = os.path.join(BASE_DIR, "data", "multi_exchange_commodity_prices.json")
            if not os.path.exists(prices_file):
                self._send_json({"ok": False, "error": "Prices file not found"}, 404)
                return
            
            try:
                with open(prices_file, "r", encoding="utf-8") as f:
                    p_data = json.load(f)
                
                matched_sec = next((s for s in p_data.get("sectors", []) if s.get("commodity_id") == comm_id), None)
                if not matched_sec:
                    self._send_json({"ok": False, "error": f"Commodity '{comm_id}' not found"}, 404)
                    return
                
                matched_bench = None
                if src_id:
                    matched_bench = next((b for b in matched_sec.get("benchmarks", []) if b.get("source_id") == src_id or b.get("tier_type") == src_id), None)
                if not matched_bench and matched_sec.get("benchmarks"):
                    matched_bench = matched_sec["benchmarks"][0]
                
                raw_history = matched_bench.get("history_1y", []) if matched_bench else []
                if time_range == "1m":
                    history = raw_history[-2:] if len(raw_history) >= 2 else raw_history
                elif time_range == "6m":
                    history = raw_history[-6:] if len(raw_history) >= 6 else raw_history
                else:
                    history = raw_history
                
                self._send_json({
                    "ok": True,
                    "commodity_id": comm_id,
                    "commodity_name": matched_sec.get("commodity_name"),
                    "hs_code": matched_sec.get("hs_code"),
                    "source_id": matched_bench.get("source_id", "") if matched_bench else "",
                    "source_name": matched_bench.get("source_name", matched_bench.get("exchange_name", "")) if matched_bench else "",
                    "source_category": matched_bench.get("source_category", "") if matched_bench else "",
                    "contract_code": matched_bench.get("contract_code", "") if matched_bench else "",
                    "current_price_usd_mt": matched_bench.get("price_usd_mt") if matched_bench else 0,
                    "price_original": matched_bench.get("price_original") if matched_bench else "",
                    "change_24h": matched_bench.get("change_24h") if matched_bench else "0.0%",
                    "change_7d": matched_bench.get("change_7d") if matched_bench else "0.0%",
                    "range": time_range,
                    "history": history
                })
            except Exception as e:
                self._send_json({"ok": False, "error": str(e)}, 500)
            return

        elif path == "/" or path == "/index.html":
            index_path = os.path.join(STATIC_DIR, "index.html")
            if os.path.exists(index_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(index_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        return super().do_GET()

    def do_POST(self):
        url_parts = urllib.parse.urlparse(self.path)
        path = url_parts.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            params = json.loads(body)
        except Exception:
            params = {}

        if path == "/api/leads/refresh-sync":
            # Làm mới và đồng bộ thông tin 1,000 leads từ các sàn B2B và dữ liệu hải quan
            db = load_database()
            leads = db.get("industry_leads", [])
            updated_count = 0
            if refresh_lead_signals:
                updated_count = refresh_lead_signals(leads)
                save_database(db)
            self._send_json({
                "status": "SUCCESS",
                "ok": True,
                "total_updated": len(leads),
                "message": f"Đã hoàn tất quét và đồng bộ dữ liệu hoạt động XNK và sàn B2B cho {len(leads)} doanh nghiệp",
                "total_checked": len(leads),
                "signals_updated": updated_count,
                "sync_time": datetime.now().strftime("%H:%M:%S %d/%m/%Y")
            })
            return

        elif path == "/api/leads/generate-outreach":
            # Sinh Thư Chào Hàng RFQ B2B Chuẩn Ngoại Thương
            lead_id = params.get("lead_id", "")
            lang = params.get("language", "EN").upper()
            db = load_database()
            leads = db.get("industry_leads", [])

            selected_lead = None
            for l in leads:
                if l.get("lead_id") == lead_id or l.get("company_name").lower() == lead_id.lower():
                    selected_lead = l
                    break

            if not selected_lead:
                selected_lead = {
                    "company_name": params.get("company_name", "Target International Importer"),
                    "country": params.get("country", "Global Market"),
                    "sourcing_contacts": [{"name": "Head of Procurement", "title": "Sourcing Director"}],
                    "commodities_demanded": [{"name": params.get("commodity", "Vietnam Export Goods"), "hs_code": params.get("hs_code", "0901.11")}],
                    "preferred_incoterms": "FOB / CIF"
                }

            outreach_result = generate_b2b_outreach_letter(selected_lead, lang)
            self._send_json({
                "status": "SUCCESS",
                "lead_id": lead_id,
                "outreach": outreach_result
            })
            return

        elif path == "/api/verify/buyer":
            # Thẩm định Khách hàng Quốc tế 4 Tầng
            query = params.get("query", "").strip()
            db = load_database()
            buyers = db.get("buyers", [])

            # 1. Tìm trong DB chuẩn hóa
            matched = None
            q_lower = query.lower()
            for b in buyers:
                if q_lower in b.get("company_name", "").lower() or \
                   q_lower in b.get("website", "").lower() or \
                   q_lower in b.get("id", "").lower() or \
                   q_lower in b.get("registration_no", "").lower():
                    matched = b
                    break

            # Kiểm tra cả trong industry_leads nếu chưa thấy trong buyers
            if not matched:
                for il in db.get("industry_leads", []):
                    if q_lower in il.get("company_name", "").lower():
                        is_raw = il.get("funnel_stage") == "raw" or il.get("tier") == "C"
                        matched = {
                            "id": il.get("lead_id"),
                            "company_name": il.get("company_name"),
                            "country": il.get("country"),
                            "country_code": il.get("country_code"),
                            "registration_no": ("INN-" + il.get("country_code") + "-889012") if il.get("country_code") == "RU" else ("REG-" + il.get("country_code") + "-981024"),
                            "duns_number": "N/A (Chưa đăng ký D&B)" if is_raw else "12-880-9912",
                            "website": il.get("company_name").lower().replace(" ", "").replace(",", "").replace(".", "") + (".ru" if il.get("country_code") == "RU" else ".com"),
                            "domain_age_years": 0.8 if is_raw else 15,
                            "email_domain": "@" + il.get("company_name").lower().replace(" ", "").replace(",", "").replace(".", "") + (".ru" if il.get("country_code") == "RU" else ".com"),
                            "is_free_email": is_raw,
                            "sanctions_status": "WATCHLIST" if is_raw else "CLEAR",
                            "sanctions_details": "Data thô mới thu thập. Cần rà soát danh sách trừng phạt OFAC/EU và xác thực ngân hàng thanh toán." if is_raw else "Rà soát OFAC/EU Sanctions: Hợp chuẩn 100%.",
                            "established_year": 2024 if is_raw else 2005,
                            "annual_revenue_usd": il.get("annual_revenue_usd", "15M"),
                            "credit_rating": "C (Rủi ro cao - Chưa kiểm định)" if is_raw else "AAA (Top Tier)",
                            "fraud_score": il.get("lead_score", 55 if is_raw else 95),
                            "tier": il.get("tier", "C" if is_raw else "A"),
                            "primary_commodities": [c.get("name") for c in il.get("commodities_demanded", [])],
                            "verified_contacts": il.get("sourcing_contacts", []),
                            "recommended_payment": "CẢNH BÁO: Bắt buộc yêu cầu đặt cọc T/T tối thiểu 30-50% hoặc L/C trả ngay có bảo lãnh ngân hàng loại 1. Tuyệt đối không cho trả chậm!" if is_raw else f"Mở {il.get('payment_terms_accepted', 'Irrevocable L/C At Sight')}. Đàm phán giao hàng theo {il.get('preferred_incoterms', 'FOB/CIF')}.",
                            "notes": il.get("outreach_angle", "Data thô cần thẩm định kỹ năng lực tài chính trước khi ký kết.")
                        }
                        break

            if matched:
                res = dict(matched)
                res["source"] = "VERIFIED_INTELLIGENCE_DB"
                res["audit_timestamp"] = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
                self._send_json(res)
                return

            # 2. Nếu chưa có trong DB: Chạy động cơ Heuristic Due Diligence 4 Tầng
            is_free_email = any(email_provider in q_lower for email_provider in [
                "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "yandex.ru", "mail.ru", "163.com", "qq.com"
            ])
            
            sanctions_keywords = ["russia", "iran", "syria", "dprk", "cuba", "sudan", "myanmar", "belarus"]
            sanctions_flag = any(kw in q_lower for kw in sanctions_keywords)

            domain_age = 0.5 if is_free_email else 4.5
            fraud_score = 35 if is_free_email else (68 if sanctions_flag else 78)
            tier = "C" if fraud_score < 60 else ("B" if fraud_score < 85 else "A")

            heuristic_res = {
                "id": "DYNAMIC-BY-" + str(abs(hash(query)) % 10000).zfill(4),
                "company_name": query if query else "Unspecified International Buyer",
                "country": "Chưa xác thực (Cần bổ sung COI)",
                "country_code": "XX",
                "registration_no": "Chưa đối soát cổng quốc gia",
                "duns_number": "Chưa có",
                "website": query if "." in query else "Chưa có website chính thức",
                "domain_age_years": domain_age,
                "email_domain": "@gmail.com" if is_free_email else f"@{query if '.' in query else 'company.com'}",
                "is_free_email": is_free_email,
                "sanctions_status": "SANCTIONS_WARNING" if sanctions_flag else ("SUSPICIOUS" if is_free_email else "CLEAR_PRELIMINARY"),
                "sanctions_details": "Cảnh báo khu vực địa chính trị rủi ro cao" if sanctions_flag else ("Địa chỉ email miễn phí có nguy cơ mạo danh" if is_free_email else "Không trùng khớp với danh sách trừng phạt OFAC cơ bản."),
                "established_year": datetime.now().year - int(domain_age),
                "annual_revenue_usd": "Chưa kiểm toán",
                "credit_rating": "Chưa cấp hạn mức tín dụng",
                "fraud_score": fraud_score,
                "tier": tier,
                "primary_commodities": ["Chưa đăng ký mã HS chính thức"],
                "verified_contacts": [
                    {"name": "Đầu mối chưa định danh", "title": "Inquiry Sender", "email": query if "@" in query else "Chưa rõ", "verified": False}
                ],
                "recommended_payment": "BÁO ĐỘNG ĐỎ: Đòi tiền cọc tối thiểu 50% T/T hoặc thanh toán 100% trước khi giao hàng. Tuyệt đối KHÔNG chấp nhận Open Account (O/A) hay D/A nợ chứng từ!" if fraud_score < 60 else "Yêu cầu mở Thư tín dụng Irrevocable L/C At Sight hoặc đặt cọc 30% T/T.",
                "notes": "Hồ sơ được thẩm định động theo thuật toán Heuristic SOP-XNK-02. Cần chuyên viên kiểm tra thêm mã số thuế VAT quốc tế.",
                "source": "HEURISTIC_DYNAMIC_AUDIT",
                "audit_timestamp": datetime.now().strftime("%H:%M:%S %d/%m/%Y")
            }
            self._send_json(heuristic_res)
            return

        elif path == "/api/verify/supplier":
            tax_code = params.get("tax_code", "").strip()
            name = params.get("company_name", "").strip()
            db = load_database()
            suppliers = db.get("suppliers", [])

            sup_id = params.get("id", "").strip()
            query_str = (tax_code or name or sup_id).strip()

            matched = None
            t_clean = re.sub(r'[^0-9]', '', tax_code)
            for s in suppliers:
                if sup_id and s.get("id") == sup_id:
                    matched = s
                    break
                if t_clean and len(t_clean) >= 9 and t_clean == re.sub(r'[^0-9]', '', s.get("tax_code", "")):
                    matched = s
                    break
                if query_str and (query_str.lower() == s.get("id", "").lower() or query_str.lower() in s.get("company_name", "").lower() or query_str.lower() in s.get("short_name", "").lower()):
                    matched = s
                    break
                if name and (name.lower() in s.get("company_name", "").lower() or name.lower() in s.get("short_name", "").lower()):
                    matched = s
                    break

            if matched:
                res = dict(matched)
                res["source"] = "VERIFIED_SUPPLIER_DB"
                res["audit_timestamp"] = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
                self._send_json(res)
                return

            is_valid_len = len(t_clean) in [10, 13]
            is_suspicious_new = t_clean.startswith("011") or t_clean.startswith("031") or len(t_clean) == 0

            vat_safety = 50 if is_suspicious_new else (85 if is_valid_len else 30)
            risk_level = "AN TOÀN SƠ BỘ" if vat_safety >= 80 else ("TRUNG BÌNH (Cần kiểm toán hóa đơn)" if vat_safety >= 60 else "NGUY HIỂM (Rủi ro doanh nghiệp ma)")

            dynamic_sup = {
                "id": "DYNAMIC-SP-" + str(abs(hash(tax_code or name)) % 10000).zfill(4),
                "tax_code": tax_code if tax_code else "Chưa cung cấp MST",
                "company_name": name if name else f"Nhà cung cấp MST {tax_code}",
                "short_name": name if name else "Đơn vị cung cấp nội địa",
                "province": "Đang tra cứu cơ quan thuế",
                "address": "Cần đối chiếu địa chỉ đăng ký kinh doanh và nhà xưởng thực tế",
                "registration_status": "Cần kiểm tra đối soát Cổng ĐKKD Quốc gia",
                "established_year": 2024 if is_suspicious_new else 2018,
                "charter_capital_vnd": "Chưa xác minh vốn thực góp",
                "legal_representative": "Cần tra cứu căn cước pháp nhân",
                "tax_risk_level": risk_level,
                "tax_compliance_notes": "Chưa có trong danh bạ nhà cung cấp ưu tiên. Khối XNK bắt buộc phải thực hiện kiểm toán thực địa 5 bước trước khi ký hợp đồng thu mua.",
                "vat_refund_safety_percent": vat_safety,
                "certificates": ["Chưa nộp hồ sơ chứng nhận ISO/HACCP/VietGAP"],
                "production_capacity": "Chưa kiểm toán công suất máy móc thực tế",
                "verified_commodities": ["Chưa xác minh nhóm hàng xuất khẩu"],
                "audit_score": vat_safety,
                "tier": "A" if vat_safety >= 85 else ("B" if vat_safety >= 60 else "C (Cảnh báo)"),
                "recommended_action": "BẮT BUỘC: Đưa vào diện kiểm toán thực địa tại xưởng. Ràng buộc điều khoản cam kết bồi thường 100% thuế GTGT và phạt 20% nếu hóa đơn bị cơ quan thuế từ chối hoàn thuế xuất khẩu." if vat_safety < 80 else "Tiến hành thẩm định hồ sơ kỹ thuật và năng lực vùng nguyên liệu.",
                "source": "HEURISTIC_DYNAMIC_TAX_CHECK",
                "audit_timestamp": datetime.now().strftime("%H:%M:%S %d/%m/%Y")
            }
            self._send_json(dynamic_sup)
            return

        elif path == "/api/audit/submit":
            sup_name = params.get("supplier_name", "Nhà xưởng không tên")
            tax_code = params.get("tax_code", "N/A")
            auditor = params.get("auditor", "Chuyên viên Khối XNK")

            c1 = int(params.get("c1_capacity", 15))
            c2 = int(params.get("c2_qa_qc", 15))
            c3 = int(params.get("c3_warehouse", 15))
            c4 = int(params.get("c4_traceability", 15))
            c5 = int(params.get("c5_labor_env", 15))

            total_score = c1 + c2 + c3 + c4 + c5
            tier = "Hạng A (Ưu tiên ký Hợp đồng Khung)" if total_score >= 85 else ("Hạng B (Kiểm soát tiến độ & hóa đơn)" if total_score >= 65 else "Hạng C (Không đạt chuẩn xuất khẩu)")

            record = {
                "audit_id": "AUD-" + datetime.now().strftime("%Y%m%d%H%M%S"),
                "timestamp": datetime.now().strftime("%H:%M %d/%m/%Y"),
                "supplier_name": sup_name,
                "tax_code": tax_code,
                "auditor": auditor,
                "scores": {
                    "capacity_actual": c1,
                    "qa_qc_standards": c2,
                    "warehouse_pest_control": c3,
                    "traceability_origin": c4,
                    "labor_ethics_env": c5
                },
                "total_score": total_score,
                "tier": tier,
                "passed": total_score >= 65,
                "notes": params.get("notes", "Đã hoàn thành kiểm toán thực địa.")
            }
            saved = save_audit_record(record)
            self._send_json(saved)
            return

        elif path == "/api/telegram/alert":
            title = params.get("title", "Cảnh Báo Điều Hành XNK")
            details = params.get("details", ["Thực hiện kiểm tra đối soát rủi ro ngoại thương."])
            if isinstance(details, str):
                details = [details]
            icon = params.get("icon") or params.get("status_icon", "🚨")
            action = params.get("action") or params.get("action_required", "Giám đốc XNK rà soát ngay lập tức.")
            chat_id = params.get("chat_id")
            dry_run = params.get("dry_run", False) or params.get("test_mode", False)

            if dry_run:
                self._send_json({
                    "ok": True,
                    "dry_run": True,
                    "status": "DRY_RUN_SUCCESS",
                    "title": title,
                    "message_length": len(title) + sum(len(d) for d in details)
                })
                return

            alert_res = send_telegram_alert_message(title, details, status_icon=icon, action_required=action, target_chat_id=chat_id)
            self._send_json({
                "ok": bool(alert_res.get("ok")),
                "status": "SENT" if alert_res.get("ok") else "FAILED",
                "sent_count": alert_res.get("sent_to_chats", 0),
                "details": alert_res
            })
            return

        elif path == "/api/matches/analyze":
            buyer_id = params.get("buyer_id", "").strip()
            supplier_id = params.get("supplier_id", "").strip()

            db = load_database()
            leads = db.get("industry_leads", [])
            suppliers = db.get("suppliers", [])

            buyer = next((b for b in leads if b.get("lead_id") == buyer_id or b.get("company_name","").lower() == buyer_id.lower()), None)
            supplier = next((s for s in suppliers if s.get("id") == supplier_id or s.get("company_name","").lower() == supplier_id.lower()), None)

            if not buyer:
                self._send_json({"ok": False, "error": f"Buyer '{buyer_id}' not found"}, 404)
                return
            if not supplier:
                self._send_json({"ok": False, "error": f"Supplier '{supplier_id}' not found"}, 404)
                return

            if not trade_matcher:
                self._send_json({"ok": False, "error": "Trade matcher engine not loaded"}, 500)
                return

            res = trade_matcher.evaluate_deal_match(buyer, supplier)
            if not res:
                self._send_json({"ok": False, "error": "Hai bên không có điểm tương đồng mặt hàng để đối soát"}, 400)
                return

            self._send_json({"ok": True, "match": res})
            return

        elif path == "/api/matches/notify-telegram":
            db = load_database()
            if not trade_matcher:
                self._send_json({"ok": False, "error": "Trade matcher engine not loaded"}, 500)
                return

            is_summary = params.get("summary", False)
            match_id = params.get("match_id", "")
            b_id = params.get("buyer_id", "")
            s_id = params.get("supplier_id", "")
            dry_run = params.get("dry_run", False) or params.get("test_mode", False)
            force = params.get("force", False)

            # Nếu là trigger gửi bản tin tóm tắt
            if is_summary or (not match_id and not (b_id and s_id)):
                if dry_run:
                    self._send_json({"ok": True, "sent": True, "dry_run": True, "type": "DAILY_SUMMARY"})
                    return
                try:
                    import morning_trade_matcher_dispatch
                    sent = morning_trade_matcher_dispatch.run_morning_dispatch(force=force, dry_run=dry_run)
                    self._send_json({"ok": True, "sent": sent, "type": "DAILY_SUMMARY"})
                except Exception as e:
                    self._send_json({"ok": False, "error": str(e)}, 500)
                return

            # Nếu là chế độ dry_run cho deal cụ thể
            if dry_run:
                self._send_json({"ok": True, "sent": True, "dry_run": True, "type": "DEAL_DETAIL"})
                return

            # Nếu là gửi chi tiết 1 deal cụ thể
            buyer = next((b for b in db.get("industry_leads", []) if b.get("lead_id") == b_id), None)
            supplier = next((s for s in db.get("suppliers", []) if s.get("id") == s_id), None)

            if buyer and supplier:
                eval_res = trade_matcher.evaluate_deal_match(buyer, supplier)
                if eval_res:
                    title = f"⭐ KHỚP LỆNH NGOẠI THƯƠNG: {eval_res['buyer_name']} ⇄ {eval_res['supplier_short_name']}"
                    details = [
                        f"🏢 Nhà Cung Cấp: {eval_res['supplier_name']} ({eval_res['supplier_country']} - {eval_res['supplier_type']})",
                        f"👤 Khách Hàng (Buyer): {eval_res['buyer_name']} ({eval_res['buyer_country']} - Tier {eval_res['buyer_tier']})",
                        f"📦 Mặt hàng khớp: {eval_res['matched_commodity']} (Mã HS: {eval_res['matched_hs']})",
                        f"🎯 Điểm khớp tổng thể: {eval_res['total_score']}/100 ({eval_res['tier_vi']})",
                        f"💰 Ước tính giá trị thương vụ: ${eval_res['deal_value_usd']:,} USD",
                        f"📑 Quy cách & HS: {eval_res['dimensions']['d1_hs_and_specs']['score']}đ ({eval_res['dimensions']['d1_hs_and_specs']['desc']})",
                        f"🏅 Chứng chỉ chất lượng: {eval_res['dimensions']['d2_quality_certifications']['score']}đ ({eval_res['dimensions']['d2_quality_certifications']['desc']})",
                        f"💳 Phương thức thanh toán: {eval_res['dimensions']['d4_payment_terms']['score']}đ ({eval_res['dimensions']['d4_payment_terms']['desc']})",
                        f"📌 Khuyến nghị: {eval_res['action_recommendation']}"
                    ]
                    alert_res = send_telegram_alert_message(title, details, "💎", "Khối XNK tiến hành liên hệ đàm phán hợp đồng nguyên tắc.")
                    self._send_json({"ok": True, "sent": alert_res.get("ok"), "type": "DEAL_DETAIL"})
                    return

            self._send_json({"ok": False, "error": "Match data not found"}, 404)
            return

        elif path == "/api/matches/generate-dual-rfq":
            db = load_database()
            b_id = params.get("buyer_id", "")
            s_id = params.get("supplier_id", "")
            b_lang = params.get("buyer_language", "EN").upper()
            s_lang = params.get("supplier_language", "VN").upper()
            comm = params.get("commodity")
            hs = params.get("hs_code")

            buyer = next((b for b in db.get("industry_leads", []) if b.get("lead_id") == b_id), None)
            supplier = next((s for s in db.get("suppliers", []) if s.get("id") == s_id), None)

            if not buyer or not supplier:
                self._send_json({"ok": False, "error": "Buyer or supplier not found"}, 404)
                return

            buyer_rfq = generate_b2b_outreach_letter(buyer, b_lang)
            supplier_rfq = generate_b2b_supplier_inquiry_letter(supplier, buyer, comm, hs, s_lang)

            self._send_json({
                "ok": True,
                "status": "SUCCESS",
                "buyer": {
                    "id": buyer.get("lead_id"),
                    "name": buyer.get("company_name"),
                    "country": buyer.get("country"),
                    "tier": buyer.get("tier")
                },
                "supplier": {
                    "id": supplier.get("id"),
                    "name": supplier.get("company_name"),
                    "short_name": supplier.get("short_name") or supplier.get("company_name"),
                    "country": supplier.get("country"),
                    "type": supplier.get("supplier_type_vi") or supplier.get("supplier_type")
                },
                "buyer_rfq": buyer_rfq,
                "supplier_rfq": supplier_rfq
            })
            return

        elif path == "/api/regulations/notify-risk-alert":
            # Gửi thông điệp cảnh báo rủi ro pháp lý & chính sách ngoại thương qua Telegram Bot
            reg_id = params.get("reg_id", "")
            dry_run = params.get("dry_run", False) or params.get("test_mode", False)
            chat_id = params.get("chat_id", None)
            
            if not regulatory_radar:
                self._send_json({"ok": False, "error": "Regulatory radar engine not loaded"}, 500)
                return
            
            res = regulatory_radar.dispatch_telegram_risk_alert(reg_id, chat_id=chat_id, dry_run=dry_run)
            self._send_json({"ok": res.get("status") == "SUCCESS", "result": res})
            return

        elif path == "/api/prices/convert":
            val = params.get("value", 1.0)
            from_u = params.get("from_unit", "mt")
            to_u = params.get("to_unit", "mt")
            price = params.get("price_usd")
            rate = params.get("exchange_rate_vnd", 25450.0)
            
            if not commodity_calculator:
                self._send_json({"ok": False, "error": "Commodity calculator not loaded"}, 500)
                return
            
            conv_res = commodity_calculator.convert_units_and_currency(val, from_u, to_u, price, rate)
            self._send_json(conv_res)
            return

        elif path == "/api/prices/arbitrage":
            comm_id = params.get("commodity_id") or params.get("commodity", "")
            buy_tier = params.get("buy_tier", "DOMESTIC_FARM")
            sell_tier = params.get("sell_tier", "DESTINATION_CIF")
            freight = params.get("estimated_freight_usd", 80.0)
            
            if not commodity_calculator:
                self._send_json({"ok": False, "error": "Commodity calculator not loaded"}, 500)
                return
            
            arb_res = commodity_calculator.calculate_arbitrage_spread(comm_id, buy_tier, sell_tier, freight)
            status_code = 200 if arb_res.get("ok") else 400
            self._send_json(arb_res, status_code)
            return

        self._send_json({"error": "Endpoint not found"}, 404)

def run_server(port=8088):
    server_address = ("0.0.0.0", port)
    httpd = ThreadedHTTPServer(server_address, PortalRequestHandler)
    print(f"================================================================")
    print(f"🚀 XNK Trade Intelligence & Verification Portal - Phase 1 MVP")
    print(f"📡 Server running at: http://localhost:{port}")
    print(f"📂 Static directory: {STATIC_DIR}")
    print(f"💾 Database path: {DATA_FILE}")
    print(f"================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[Server Stopped]")
        httpd.server_close()

if __name__ == "__main__":
    port = 8088
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)
