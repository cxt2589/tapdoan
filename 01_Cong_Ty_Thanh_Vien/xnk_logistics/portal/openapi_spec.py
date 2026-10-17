#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAPI 3.1.0 Contract Specification Generator
Nền tảng Tình Báo Thương Mại & Thẩm Định Ngoại Thương B2B Tập Đoàn
Tuân thủ tiêu chuẩn kỹ thuật của agency-api-platform-engineer
"""

import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def get_openapi_spec(server_url="http://103.228.74.58"):
    spec = {
        "openapi": "3.1.0",
        "info": {
            "title": "Tập Đoàn Đa Ngành — Trade Intelligence & Verification Platform API",
            "version": "1.0.0",
            "description": (
                "Hệ thống API Nền tảng Tình Báo Ngoại Thương & Thẩm Định Đối Tác 360° "
                "thuộc Khối Xuất Nhập Khẩu & Thương Mại Quốc Tế Tập Đoàn. "
                "Cung cấp khả năng truy xuất kho 1,000 Leads khách hàng toàn cầu, thẩm định pháp lý 4 tầng, "
                "bức tường lửa thuế GTGT nội địa, động cơ khớp lệnh ma trận 6 chiều B2B, bảng giá đa sàn quốc tế, "
                "tra cứu 97 chương HS và radar chính sách ngoại thương (EUDR, CBAM, UFLPA, GACC)."
            ),
            "contact": {
                "name": "Ban Công nghệ & Điều phối Kỹ thuật Tổng Hành Dinh",
                "email": "tech@tapdoan.corp"
            },
            "license": {
                "name": "Proprietary - Tập Đoàn Đa Ngành (Holding Master)"
            }
        },
        "servers": [
            {"url": server_url, "description": "Production Node (VPS 1 - Singapore Hub)"},
            {"url": "http://127.0.0.1:8088", "description": "Local Development Server"}
        ],
        "tags": [
            {"name": "System & Platform", "description": "Trạng thái hệ thống, danh mục khu vực, ngành hàng và chỉ mục API"},
            {"name": "Leads & Prospecting", "description": "Khai thác kho 1,000 Leads khách hàng toàn cầu, lọc theo 97 chương HS, 6 cụm ngành & AI Outreach"},
            {"name": "Due Diligence & Verification", "description": "Thẩm định pháp lý đối tác 4 tầng (OFAC, Whois, FinHealth) & Bức tường lửa thuế GTGT nội địa"},
            {"name": "Suppliers & Counterparties", "description": "Danh bạ 20 Nhà cung cấp & Đại lý cấp 1 toàn cầu tại 12 quốc gia & Mạng lưới đối tác 360°"},
            {"name": "Trade Matchmaker & Dual RFQ", "description": "Động cơ khớp lệnh B2B ma trận 6 chiều, giải thích điểm vênh thương thảo & Sinh bộ đôi RFQ"},
            {"name": "Customs & Bill of Lading", "description": "Truy xuất vận đơn hải quan thực tế B/L, giá trị CIF/FOB, danh mục container và hãng tàu"},
            {"name": "Factory Audit (SOP-XNK-02)", "description": "Chấm điểm kiểm toán thực địa cơ sở nhà máy theo 5 tiêu chuẩn thực địa quốc tế"},
            {"name": "HS Catalog & Products", "description": "Tra cứu 97 chương HS theo 4 chế độ trực quan & 213 sản phẩm ngoại thương chiến lược"},
            {"name": "Regulatory Radar", "description": "Radar pháp lý & Chân trời chính sách mới toàn cầu (EUDR, CBAM, UFLPA, GACC) & Cảnh báo Telegram"},
            {"name": "Trade Tags & Terminology", "description": "Từ điển thẻ tag quy chuẩn ngoại thương (Specs, Certs, Incoterms, Payment) & Khuyến nghị chuyên gia"},
            {"name": "Multi-Exchange Price Board", "description": "Bảng giá 4 tầng đa sàn quốc tế (6 mặt hàng chiến lược), Bộ chuẩn hóa đơn vị & Radar chênh lệch giá (Arbitrage)"},
            {"name": "Telegram Alerts", "description": "Kênh phát thông báo và cảnh báo tác chiến tức thời về Telegram Bot @tapdoan_bot"}
        ],
        "paths": {
            "/api": {
                "get": {
                    "tags": ["System & Platform"],
                    "summary": "Chỉ mục danh mục API & Thông số phiên bản",
                    "operationId": "getApiIndex",
                    "responses": {
                        "200": {
                            "description": "Thành công",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ApiIndexResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/health": {
                "get": {
                    "tags": ["System & Platform"],
                    "summary": "Kiểm tra sức khỏe dịch vụ & Database",
                    "operationId": "getHealth",
                    "responses": {
                        "200": {
                            "description": "Dịch vụ hoạt động bình thường",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/HealthResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/regions": {
                "get": {
                    "tags": ["System & Platform"],
                    "summary": "Danh bạ các vùng thị trường giao thương trọng điểm",
                    "operationId": "getRegions",
                    "responses": {
                        "200": {
                            "description": "Danh sách vùng địa lý ngoại thương",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/MarketRegion"}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/industries": {
                "get": {
                    "tags": ["System & Platform"],
                    "summary": "Danh mục các ngành hàng ngoại thương",
                    "operationId": "getIndustries",
                    "responses": {
                        "200": {
                            "description": "Danh sách ngành hàng",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Industry"}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/leads/by-industry": {
                "get": {
                    "tags": ["Leads & Prospecting"],
                    "summary": "Săn tìm và lọc kho 1,000 Leads khách hàng toàn cầu",
                    "description": "Hỗ trợ lọc đa chiều theo ngành hàng, chương HS (01-97), cụm chuỗi giá trị (cluster), quốc gia, khu vực, tầng phễu (raw/tier_b/tier_a) và phân trang chuẩn 10 DN/trang.",
                    "operationId": "getLeadsByIndustry",
                    "parameters": [
                        {"name": "industry", "in": "query", "description": "Mã ngành hàng (hoặc 'all')", "schema": {"type": "string"}},
                        {"name": "chapter", "in": "query", "description": "Mã 2 chữ số chương HS (ví dụ '09' cho cà phê, '61' cho dệt may)", "schema": {"type": "string"}},
                        {"name": "cluster", "in": "query", "description": "Mã cụm chuỗi giá trị (ví dụ 'agri_food', 'tech_machinery')", "schema": {"type": "string"}},
                        {"name": "hs", "in": "query", "description": "Tiền tố mã HS cụ thể (ví dụ '0901', '3102')", "schema": {"type": "string"}},
                        {"name": "country", "in": "query", "description": "Tên hoặc mã quốc gia (ví dụ 'russia', 'ru', 'china', 'germany')", "schema": {"type": "string"}},
                        {"name": "region", "in": "query", "description": "Vùng thị trường (ví dụ 'russia_eaeu', 'north_america', 'europe')", "schema": {"type": "string"}},
                        {"name": "stage", "in": "query", "description": "Tầng phễu: 'raw', 'tier_b', 'tier_a'", "schema": {"type": "string"}},
                        {"name": "q", "in": "query", "description": "Từ khóa tìm kiếm tự do (tên doanh nghiệp, thành phố, sàn)", "schema": {"type": "string"}},
                        {"name": "page", "in": "query", "description": "Số trang (mặc định 1)", "schema": {"type": "integer", "default": 1}},
                        {"name": "page_size", "in": "query", "description": "Số bản ghi mỗi trang (mặc định 10)", "schema": {"type": "integer", "default": 10}},
                        {"name": "export", "in": "query", "description": "Đặt 'csv' để xuất danh sách đã lọc ra định dạng CSV", "schema": {"type": "string"}}
                    ],
                    "responses": {
                        "200": {
                            "description": "Danh sách khách hàng phân trang kèm thống kê phễu",
                            "content": {
                                "application/json": {"schema": {"$ref": "#/components/schemas/LeadsPageResponse"}},
                                "text/csv": {"schema": {"type": "string", "format": "binary"}}
                            }
                        }
                    }
                }
            },
            "/api/leads/detail": {
                "get": {
                    "tags": ["Leads & Prospecting"],
                    "summary": "Truy xuất chi tiết hồ sơ tình báo khách hàng tiềm năng",
                    "operationId": "getLeadDetail",
                    "parameters": [
                        {"name": "id", "in": "query", "required": True, "description": "Mã định danh Lead (ví dụ: LEAD-AGRI-001)", "schema": {"type": "string"}},
                        {"name": "name", "in": "query", "description": "Tìm theo tên doanh nghiệp nếu không nhớ ID", "schema": {"type": "string"}}
                    ],
                    "responses": {
                        "200": {
                            "description": "Chi tiết hồ sơ khách hàng",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/LeadDetailResponse"}}}
                        },
                        "404": {"$ref": "#/components/responses/NotFound"}
                    }
                }
            },
            "/api/leads/sourcing-evaluation": {
                "get": {
                    "tags": ["Leads & Prospecting"],
                    "summary": "Đánh giá nhu cầu mở rộng nguồn cung địa lý & Tỷ lệ khả thi kết nối",
                    "operationId": "getLeadSourcingEvaluation",
                    "parameters": [
                        {"name": "id", "in": "query", "required": True, "description": "Mã định danh Lead", "schema": {"type": "string"}}
                    ],
                    "responses": {
                        "200": {
                            "description": "Bản đánh giá khả thi nguồn cung và gợi ý đối tác",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/SourcingEvaluationResponse"}}}
                        },
                        "404": {"$ref": "#/components/responses/NotFound"}
                    }
                }
            },
            "/api/leads/export-csv": {
                "get": {
                    "tags": ["Leads & Prospecting"],
                    "summary": "Xuất toàn bộ kho 1,000 Leads khách hàng ngoại thương ra file CSV UTF-8",
                    "operationId": "exportLeadsCsv",
                    "responses": {
                        "200": {
                            "description": "File CSV danh sách 1,000 Leads",
                            "content": {"text/csv": {"schema": {"type": "string", "format": "binary"}}}
                        }
                    }
                }
            },
            "/api/leads/refresh-sync": {
                "post": {
                    "tags": ["Leads & Prospecting"],
                    "summary": "Đồng bộ và làm mới tín hiệu giao dịch của kho khách hàng",
                    "operationId": "refreshLeadSignals",
                    "responses": {
                        "200": {
                            "description": "Trạng thái làm mới dữ liệu",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/SyncResponse"}}}
                        }
                    }
                }
            },
            "/api/leads/generate-outreach": {
                "post": {
                    "tags": ["Leads & Prospecting"],
                    "summary": "Sinh thư chào hàng ngoại thương AI 3 ngôn ngữ (Anh, Nga, Trung)",
                    "description": "Soạn thảo thư chào hàng thương mại quốc tế chuẩn tập quán Incoterms 2020 và thanh toán L/C / T/T dựa trên mã HS và quy mô của khách hàng.",
                    "operationId": "generateOutreach",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/OutreachGenerateRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Thư chào hàng đa ngôn ngữ đã sinh",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/OutreachGenerateResponse"}}}
                        },
                        "400": {"$ref": "#/components/responses/BadRequest"}
                    }
                }
            },
            "/api/buyers": {
                "get": {
                    "tags": ["Due Diligence & Verification"],
                    "summary": "Danh sách các người mua đã qua thẩm định sơ bộ",
                    "operationId": "getBuyers",
                    "responses": {
                        "200": {
                            "description": "Danh sách người mua",
                            "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Buyer"}}}}
                        }
                    }
                }
            },
            "/api/verify/buyer": {
                "post": {
                    "tags": ["Due Diligence & Verification"],
                    "summary": "Thực thi quy trình thẩm định 4 tầng đối với Người mua quốc tế",
                    "description": "Rà soát 4 tầng: Tầng 1 - Pháp nhân sở tại; Tầng 2 - Tên miền email giao dịch (Domain Whois); Tầng 3 - Danh sách trừng phạt OFAC/EU/UN; Tầng 4 - Sức khỏe tài chính.",
                    "operationId": "verifyBuyer",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/BuyerVerifyRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Kết quả thẩm định 4 tầng",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/BuyerVerifyResponse"}}}
                        },
                        "400": {"$ref": "#/components/responses/BadRequest"}
                    }
                }
            },
            "/api/suppliers": {
                "get": {
                    "tags": ["Suppliers & Counterparties"],
                    "summary": "Danh bạ 20 Nhà cung cấp & Đại lý cấp 1 toàn cầu tại 12 quốc gia",
                    "description": "Hỗ trợ lọc theo loại hình đối tác (tier1_master_agent, manufacturer_direct, logistics_broker), quốc gia và tình trạng thẩm định.",
                    "operationId": "getSuppliers",
                    "parameters": [
                        {"name": "type", "in": "query", "description": "Loại hình: 'tier1_master_agent', 'manufacturer_direct', 'all'", "schema": {"type": "string"}},
                        {"name": "country", "in": "query", "description": "Mã quốc gia: 'ch', 'ru', 'de', 'us', 'vn', v.v.", "schema": {"type": "string"}},
                        {"name": "commodity", "in": "query", "description": "Tên mặt hàng cung ứng", "schema": {"type": "string"}},
                        {"name": "q", "in": "query", "description": "Từ khóa tìm kiếm", "schema": {"type": "string"}}
                    ],
                    "responses": {
                        "200": {
                            "description": "Danh bạ đối tác cung ứng",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/SuppliersResponse"}}}
                        }
                    }
                }
            },
            "/api/suppliers/detail": {
                "get": {
                    "tags": ["Suppliers & Counterparties"],
                    "summary": "Truy xuất hồ sơ chi tiết đối tác cung ứng & năng lực tín dụng L/C",
                    "operationId": "getSupplierDetail",
                    "parameters": [
                        {"name": "id", "in": "query", "required": True, "description": "Mã nhà cung cấp (ví dụ: SP-001, SUP-GLB-001)", "schema": {"type": "string"}}
                    ],
                    "responses": {
                        "200": {
                            "description": "Hồ sơ năng lực nhà cung cấp",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/SupplierDetailResponse"}}}
                        },
                        "404": {"$ref": "#/components/responses/NotFound"}
                    }
                }
            },
            "/api/verify/supplier": {
                "post": {
                    "tags": ["Due Diligence & Verification"],
                    "summary": "Vận hành Bức tường lửa thuế GTGT Nhà cung cấp nội địa Việt Nam",
                    "description": "Kiểm tra mã số thuế, rủi ro hóa đơn khống, tình trạng doanh nghiệp ma và dấu hiệu rủi ro cao nhằm bảo vệ hồ sơ hoàn thuế GTGT cho Tập đoàn.",
                    "operationId": "verifySupplierTaxFirewall",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SupplierTaxVerifyRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Kết quả rà soát bức tường lửa thuế",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/SupplierTaxVerifyResponse"}}}
                        },
                        "400": {"$ref": "#/components/responses/BadRequest"}
                    }
                }
            },
            "/api/contacts": {
                "get": {
                    "tags": ["Suppliers & Counterparties"],
                    "summary": "Tra cứu danh bạ đầu mối liên lạc trực tiếp của Khách hàng hoặc NCC",
                    "operationId": "getContacts",
                    "parameters": [
                        {"name": "id", "in": "query", "description": "Mã Lead (LEAD-...) hoặc Mã NCC (SP-..., SUP-...)", "schema": {"type": "string"}},
                        {"name": "type", "in": "query", "description": "Loại thực thể: 'lead' hoặc 'supplier'", "schema": {"type": "string"}},
                        {"name": "name", "in": "query", "description": "Tìm theo tên doanh nghiệp", "schema": {"type": "string"}}
                    ],
                    "responses": {
                        "200": {
                            "description": "Danh bạ nhân sự thu mua / xuất nhập khẩu",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ContactsResponse"}}}
                        },
                        "404": {"$ref": "#/components/responses/NotFound"}
                    }
                }
            },
            "/api/matches/metrics": {
                "get": {
                    "tags": ["Trade Matchmaker & Dual RFQ"],
                    "summary": "Thống kê chỉ số Bàn Khớp Lệnh Ma Trận 6 Chiều B2B",
                    "operationId": "getMatchMetrics",
                    "responses": {
                        "200": {
                            "description": "Chỉ số tổng hợp các cặp giao dịch khớp lệnh",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/MatchMetricsResponse"}}}
                        }
                    }
                }
            },
            "/api/matches": {
                "get": {
                    "tags": ["Trade Matchmaker & Dual RFQ"],
                    "summary": "Danh sách các cặp giao dịch khớp lệnh ma trận 6 chiều B2B",
                    "description": "Đối soát 6 chiều: (1) Mã HS & Quy cách, (2) Chứng chỉ quốc tế, (3) Điều kiện Incoterms, (4) Phương thức thanh toán L/C/TT, (5) Cụm cảng logistics, (6) Chênh lệch biên lợi nhuận.",
                    "operationId": "getMatches",
                    "parameters": [
                        {"name": "commodity", "in": "query", "description": "Lọc theo mặt hàng", "schema": {"type": "string"}},
                        {"name": "min_score", "in": "query", "description": "Điểm khớp tối thiểu (0-100)", "schema": {"type": "integer"}},
                        {"name": "status", "in": "query", "description": "Trạng thái: 'ready_to_close', 'negotiation_needed', 'high_discrepancy'", "schema": {"type": "string"}},
                        {"name": "page", "in": "query", "description": "Số trang", "schema": {"type": "integer", "default": 1}},
                        {"name": "page_size", "in": "query", "description": "Số bản ghi mỗi trang", "schema": {"type": "integer", "default": 10}}
                    ],
                    "responses": {
                        "200": {
                            "description": "Danh sách các cặp khớp lệnh",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/MatchesListResponse"}}}
                        }
                    }
                }
            },
            "/api/matches/analyze": {
                "post": {
                    "tags": ["Trade Matchmaker & Dual RFQ"],
                    "summary": "Phân tích đối soát chi tiết ma trận 6 chiều & Điểm vênh thương thảo",
                    "operationId": "analyzeMatch",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/MatchAnalyzeRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Bản đối soát 6 chiều chi tiết và khuyến nghị chốt deal",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/MatchAnalyzeResponse"}}}
                        },
                        "400": {"$ref": "#/components/responses/BadRequest"}
                    }
                }
            },
            "/api/matches/generate-dual-rfq": {
                "post": {
                    "tags": ["Trade Matchmaker & Dual RFQ"],
                    "summary": "Sinh bộ đôi RFQ B2B (Buyer Quotation + Supplier Inquiry)",
                    "operationId": "generateDualRfq",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/DualRfqRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Bộ đôi văn bản RFQ thương mại hoàn chỉnh",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/DualRfqResponse"}}}
                        },
                        "400": {"$ref": "#/components/responses/BadRequest"}
                    }
                }
            },
            "/api/matches/notify-telegram": {
                "post": {
                    "tags": ["Trade Matchmaker & Dual RFQ", "Telegram Alerts"],
                    "summary": "Gửi thông báo cặp khớp lệnh chiến lược tới Telegram Bot Chủ tịch",
                    "operationId": "notifyMatchTelegram",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/MatchTelegramNotifyRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Trạng thái gửi tin nhắn Telegram",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/TelegramAlertResponse"}}}
                        }
                    }
                }
            },
            "/api/discovery/bl": {
                "get": {
                    "tags": ["Customs & Bill of Lading"],
                    "summary": "Truy xuất và sàng lọc lịch sử Vận đơn Hải quan (Bill of Lading)",
                    "operationId": "getBillOfLadings",
                    "parameters": [
                        {"name": "commodity", "in": "query", "description": "Tên hàng hóa trên vận đơn", "schema": {"type": "string"}},
                        {"name": "container", "in": "query", "description": "Mã số Container", "schema": {"type": "string"}},
                        {"name": "carrier", "in": "query", "description": "Hãng tàu / Đơn vị vận chuyển", "schema": {"type": "string"}},
                        {"name": "shipper", "in": "query", "description": "Người gửi hàng (Shipper)", "schema": {"type": "string"}},
                        {"name": "consignee", "in": "query", "description": "Người nhận hàng (Consignee)", "schema": {"type": "string"}}
                    ],
                    "responses": {
                        "200": {
                            "description": "Danh sách vận đơn B/L thực tế",
                            "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/BillOfLading"}}}}
                        }
                    }
                }
            },
            "/api/audits": {
                "get": {
                    "tags": ["Factory Audit (SOP-XNK-02)"],
                    "summary": "Lịch sử biên bản kiểm toán thực địa cơ sở nhà máy SOP-XNK-02",
                    "operationId": "getAudits",
                    "responses": {
                        "200": {
                            "description": "Danh sách biên bản kiểm toán",
                            "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/FactoryAuditRecord"}}}}
                        }
                    }
                }
            },
            "/api/audit/submit": {
                "post": {
                    "tags": ["Factory Audit (SOP-XNK-02)"],
                    "summary": "Nộp biên bản đánh giá thực địa nhà máy theo 5 tiêu chuẩn",
                    "description": "Chấm điểm 5 tiêu chuẩn: (1) Cơ sở hạ tầng & Dây chuyền, (2) Quản lý chất lượng ISO/HACCP, (3) An toàn lao động, (4) Năng lực cung ứng, (5) Tuân thủ pháp lý môi trường.",
                    "operationId": "submitAudit",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/AuditSubmitRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Biên bản kiểm toán đã lưu",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/AuditSubmitResponse"}}}
                        },
                        "400": {"$ref": "#/components/responses/BadRequest"}
                    }
                }
            },
            "/api/hs/summary": {
                "get": {
                    "tags": ["HS Catalog & Products"],
                    "summary": "Chỉ số tổng quan danh mục Biểu thuế Hải quan HS",
                    "operationId": "getHsSummary",
                    "responses": {
                        "200": {
                            "description": "Tổng số 21 phần, 97 chương, 7 cụm ngành và 213 sản phẩm",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/HsSummaryResponse"}}}
                        }
                    }
                }
            },
            "/api/hs/catalog": {
                "get": {
                    "tags": ["HS Catalog & Products"],
                    "summary": "Duyệt danh bạ 97 Chương HS theo 4 chế độ hiển thị",
                    "operationId": "getHsCatalog",
                    "parameters": [
                        {"name": "mode", "in": "query", "description": "Chế độ xem: 'volume' (Kim ngạch), 'clusters' (6 Chuỗi giá trị), 'alphabet' (A-Z), 'wco' (Chuẩn WCO 01-97)", "schema": {"type": "string", "default": "volume"}}
                    ],
                    "responses": {
                        "200": {
                            "description": "Danh bạ phân nhóm theo chế độ",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/HsCatalogResponse"}}}
                        }
                    }
                }
            },
            "/api/hs/search": {
                "get": {
                    "tags": ["HS Catalog & Products"],
                    "summary": "Tìm kiếm thông minh toàn phần (Omni-Search) theo mã hoặc tên tiếng Việt",
                    "operationId": "searchHs",
                    "parameters": [
                        {"name": "q", "in": "query", "required": True, "description": "Từ khóa tìm kiếm (mã chương 09, mã sản phẩm 0901, hoặc 'cà phê', 'tiêu')", "schema": {"type": "string"}}
                    ],
                    "responses": {
                        "200": {
                            "description": "Kết quả tìm kiếm khớp mã và tên",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/HsSearchResponse"}}}
                        }
                    }
                }
            },
            "/api/hs/products": {
                "get": {
                    "tags": ["HS Catalog & Products"],
                    "summary": "Truy xuất danh bạ 213 sản phẩm ngoại thương chiến lược của Tập đoàn",
                    "operationId": "getHsProducts",
                    "parameters": [
                        {"name": "chapter", "in": "query", "description": "Lọc theo 2 chữ số chương HS (ví dụ: '09', '61')", "schema": {"type": "string"}},
                        {"name": "q", "in": "query", "description": "Tìm theo tên sản phẩm hoặc mã HS", "schema": {"type": "string"}},
                        {"name": "limit", "in": "query", "description": "Giới hạn số bản ghi trả về", "schema": {"type": "integer", "default": 20}}
                    ],
                    "responses": {
                        "200": {
                            "description": "Danh sách sản phẩm chiến lược",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/HsProductsResponse"}}}
                        }
                    }
                }
            },
            "/api/regulations/active": {
                "get": {
                    "tags": ["Regulatory Radar"],
                    "summary": "Danh sách các đạo luật & rào cản kỹ thuật ngoại thương quốc tế đang áp dụng",
                    "operationId": "getActiveRegulations",
                    "responses": {
                        "200": {
                            "description": "Danh sách quy định pháp lý (EUDR, CBAM, UFLPA, GACC, v.v.)",
                            "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Regulation"}}}}
                        }
                    }
                }
            },
            "/api/regulations/horizon-calendar": {
                "get": {
                    "tags": ["Regulatory Radar"],
                    "summary": "Lịch trình Chân trời Pháp lý & Mốc thời gian hiệu lực bắt buộc",
                    "operationId": "getRegulationHorizonCalendar",
                    "responses": {
                        "200": {
                            "description": "Biểu đồ mốc thời gian thi hành các đạo luật",
                            "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/RegulationMilestone"}}}}
                        }
                    }
                }
            },
            "/api/regulations/detail": {
                "get": {
                    "tags": ["Regulatory Radar"],
                    "summary": "Truy xuất chi tiết đạo luật & Cẩm nang tuân thủ pháp lý ngoại thương",
                    "operationId": "getRegulationDetail",
                    "parameters": [
                        {"name": "id", "in": "query", "required": True, "description": "Mã quy định (ví dụ: REG-EUDR-2024, REG-CBAM-2026)", "schema": {"type": "string"}}
                    ],
                    "responses": {
                        "200": {
                            "description": "Chi tiết đạo luật và hướng dẫn hành động bắt buộc",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/RegulationDetailResponse"}}}
                        },
                        "404": {"$ref": "#/components/responses/NotFound"}
                    }
                }
            },
            "/api/regulations/notify-risk-alert": {
                "post": {
                    "tags": ["Regulatory Radar", "Telegram Alerts"],
                    "summary": "Phát cảnh báo khẩn cấp rủi ro vi phạm đạo luật tới Telegram Bot",
                    "operationId": "notifyRegulationAlert",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/RegulationAlertRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Trạng thái phát cảnh báo",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/TelegramAlertResponse"}}}
                        }
                    }
                }
            },
            "/api/trade-tags/catalog": {
                "get": {
                    "tags": ["Trade Tags & Terminology"],
                    "summary": "Danh mục Từ điển Thẻ Tag Quy Chuẩn Ngoại Thương Toàn Diện",
                    "description": "Bao quát 4 nhóm tiêu chuẩn: (1) Quy cách kỹ thuật Specs, (2) Chứng chỉ chất lượng Certs, (3) Điều kiện Incoterms, (4) Điều khoản thanh toán quốc tế.",
                    "operationId": "getTradeTagsCatalog",
                    "responses": {
                        "200": {
                            "description": "Từ điển thẻ tag quy chuẩn",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/TradeTagsCatalogResponse"}}}
                        }
                    }
                }
            },
            "/api/trade-tags/explain": {
                "get": {
                    "tags": ["Trade Tags & Terminology"],
                    "summary": "Giải thích chi tiết ý nghĩa nghiệp vụ & Khuyến nghị chuyên gia theo Thẻ Tag",
                    "operationId": "explainTradeTag",
                    "parameters": [
                        {"name": "tag", "in": "query", "required": True, "description": "Tên thẻ tag (ví dụ: '#Moist_Max12.5%', '#Halal_JAKIM', '#LC_At_Sight')", "schema": {"type": "string"}}
                    ],
                    "responses": {
                        "200": {
                            "description": "Nội dung giải thích chi tiết và phân loại nghiệp vụ",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/TradeTagExplainResponse"}}}
                        },
                        "404": {"$ref": "#/components/responses/NotFound"}
                    }
                }
            },
            "/api/prices/benchmarks": {
                "get": {
                    "tags": ["Multi-Exchange Price Board"],
                    "summary": "Bảng Giá 4 Tầng Đa Sàn Quốc Tế (6 Mặt hàng ngoại thương chiến lược)",
                    "description": "Bảng giá 4 tầng: (1) Giá Sàn Thế Giới, (2) Giá FOB Cảng Cát Lái / Hải Phòng, (3) Giá CIF Cảng đến quốc tế, (4) Giá Cửa Vườn / Xuất Xưởng nội địa.",
                    "operationId": "getPriceBenchmarks",
                    "responses": {
                        "200": {
                            "description": "Bảng giá đa tầng các mặt hàng chiến lược",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PriceBenchmarksResponse"}}}
                        }
                    }
                }
            },
            "/api/prices/convert": {
                "post": {
                    "tags": ["Multi-Exchange Price Board"],
                    "summary": "Bộ chuẩn hóa quy đổi đơn vị đo lường & Tiền tệ ngoại thương tức thì",
                    "description": "Quy đổi giữa lbs (Pounds), MT (Tấn), Kg, Bao 60kg, Bao 50kg và chuyển đổi tỉ giá USD/VNĐ.",
                    "operationId": "convertPriceUnit",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/PriceConvertRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Kết quả quy đổi đơn vị và giá tương đương",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/PriceConvertResponse"}}}
                        },
                        "400": {"$ref": "#/components/responses/BadRequest"}
                    }
                }
            },
            "/api/prices/arbitrage": {
                "post": {
                    "tags": ["Multi-Exchange Price Board"],
                    "summary": "Radar tính toán chênh lệch giá & Biên lợi nhuận Arbitrage thương mại",
                    "operationId": "calculateArbitrage",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ArbitrageCalculateRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Phân tích chênh lệch giá sàn, chi phí logistics và biên lợi nhuận ròng",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ArbitrageCalculateResponse"}}}
                        },
                        "400": {"$ref": "#/components/responses/BadRequest"}
                    }
                }
            },
            "/api/telegram/alert": {
                "post": {
                    "tags": ["Telegram Alerts"],
                    "summary": "Bắn thông điệp chỉ đạo và cảnh báo tác chiến tức thời về Telegram Bot @tapdoan_bot",
                    "operationId": "sendTelegramAlert",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/TelegramDirectAlertRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Trạng thái gửi tin nhắn tới Telegram Chủ tịch",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/TelegramAlertResponse"}}}
                        },
                        "400": {"$ref": "#/components/responses/BadRequest"}
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "Error": {
                    "type": "object",
                    "required": ["code", "message"],
                    "properties": {
                        "code": {"type": "string", "example": "resource_not_found"},
                        "message": {"type": "string", "example": "Không tìm thấy dữ liệu yêu cầu"},
                        "details": {"type": "object"},
                        "request_id": {"type": "string"}
                    }
                },
                "ApiIndexResponse": {
                    "type": "object",
                    "properties": {
                        "ok": {"type": "boolean", "example": True},
                        "platform": {"type": "string", "example": "Trade Intelligence & Verification Platform"},
                        "version": {"type": "string", "example": "1.0.0"},
                        "docs_url": {"type": "string", "example": "/api/docs"},
                        "openapi_url": {"type": "string", "example": "/api/openapi.json"},
                        "total_endpoints": {"type": "integer", "example": 36},
                        "categories": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                },
                "HealthResponse": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "healthy"},
                        "version": {"type": "string", "example": "1.0.0"},
                        "time": {"type": "string"},
                        "database": {"type": "object"}
                    }
                },
                "MarketRegion": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "countries": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "Industry": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"}
                    }
                },
                "LeadsPageResponse": {
                    "type": "object",
                    "properties": {
                        "total": {"type": "integer"},
                        "page": {"type": "integer"},
                        "page_size": {"type": "integer"},
                        "total_pages": {"type": "integer"},
                        "funnel_stats": {"type": "object"},
                        "data": {"type": "array", "items": {"type": "object"}}
                    }
                },
                "LeadDetailResponse": {
                    "type": "object",
                    "properties": {
                        "ok": {"type": "boolean"},
                        "lead": {"type": "object"}
                    }
                },
                "SourcingEvaluationResponse": {
                    "type": "object",
                    "properties": {
                        "ok": {"type": "boolean"},
                        "evaluation": {"type": "object"}
                    }
                },
                "SyncResponse": {
                    "type": "object",
                    "properties": {
                        "ok": {"type": "boolean"},
                        "message": {"type": "string"},
                        "refreshed_at": {"type": "string"}
                    }
                },
                "OutreachGenerateRequest": {
                    "type": "object",
                    "required": ["lead_id"],
                    "properties": {
                        "lead_id": {"type": "string"},
                        "language": {"type": "string", "enum": ["en", "ru", "cn", "all"], "default": "all"}
                    }
                },
                "OutreachGenerateResponse": {
                    "type": "object",
                    "properties": {
                        "ok": {"type": "boolean"},
                        "lead_id": {"type": "string"},
                        "outreach_templates": {"type": "object"}
                    }
                },
                "Buyer": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "country": {"type": "string"},
                        "status": {"type": "string"}
                    }
                },
                "BuyerVerifyRequest": {
                    "type": "object",
                    "required": ["buyer_name"],
                    "properties": {
                        "buyer_name": {"type": "string"},
                        "domain": {"type": "string"},
                        "country": {"type": "string"}
                    }
                },
                "BuyerVerifyResponse": {
                    "type": "object",
                    "properties": {
                        "ok": {"type": "boolean"},
                        "verification_id": {"type": "string"},
                        "risk_score": {"type": "integer"},
                        "sanction_passed": {"type": "boolean"},
                        "tiers_result": {"type": "object"}
                    }
                },
                "SuppliersResponse": {
                    "type": "object",
                    "properties": {
                        "total": {"type": "integer"},
                        "suppliers": {"type": "array", "items": {"type": "object"}}
                    }
                },
                "SupplierDetailResponse": {
                    "type": "object",
                    "properties": {
                        "ok": {"type": "boolean"},
                        "supplier": {"type": "object"}
                    }
                },
                "SupplierTaxVerifyRequest": {
                    "type": "object",
                    "required": ["tax_code"],
                    "properties": {
                        "tax_code": {"type": "string"},
                        "supplier_name": {"type": "string"}
                    }
                },
                "SupplierTaxVerifyResponse": {
                    "type": "object",
                    "properties": {
                        "ok": {"type": "boolean"},
                        "tax_status": {"type": "string"},
                        "invoice_risk": {"type": "string"},
                        "firewall_passed": {"type": "boolean"}
                    }
                },
                "ContactsResponse": {
                    "type": "object",
                    "properties": {
                        "ok": {"type": "boolean"},
                        "id": {"type": "string"},
                        "type": {"type": "string"},
                        "company_name": {"type": "string"},
                        "contacts": {"type": "array", "items": {"type": "object"}}
                    }
                },
                "MatchMetricsResponse": {
                    "type": "object",
                    "properties": {
                        "total_pairs": {"type": "integer"},
                        "ready_to_close": {"type": "integer"},
                        "negotiation_needed": {"type": "integer"}
                    }
                },
                "MatchesListResponse": {
                    "type": "object",
                    "properties": {
                        "total": {"type": "integer"},
                        "page": {"type": "integer"},
                        "page_size": {"type": "integer"},
                        "data": {"type": "array", "items": {"type": "object"}}
                    }
                },
                "MatchAnalyzeRequest": {
                    "type": "object",
                    "required": ["lead_id", "supplier_id"],
                    "properties": {
                        "lead_id": {"type": "string"},
                        "supplier_id": {"type": "string"}
                    }
                },
                "MatchAnalyzeResponse": {
                    "type": "object",
                    "properties": {
                        "ok": {"type": "boolean"},
                        "match_score": {"type": "integer"},
                        "dimensions": {"type": "object"}
                    }
                },
                "DualRfqRequest": {
                    "type": "object",
                    "required": ["lead_id", "supplier_id"],
                    "properties": {
                        "lead_id": {"type": "string"},
                        "supplier_id": {"type": "string"}
                    }
                },
                "DualRfqResponse": {
                    "type": "object",
                    "properties": {
                        "ok": {"type": "boolean"},
                        "rfq_pair_id": {"type": "string"},
                        "buyer_quotation": {"type": "object"},
                        "supplier_inquiry": {"type": "object"}
                    }
                },
                "MatchTelegramNotifyRequest": {
                    "type": "object",
                    "required": ["lead_id", "supplier_id"],
                    "properties": {
                        "lead_id": {"type": "string"},
                        "supplier_id": {"type": "string"},
                        "note": {"type": "string"}
                    }
                },
                "TelegramAlertResponse": {
                    "type": "object",
                    "properties": {
                        "ok": {"type": "boolean"},
                        "sent_count": {"type": "integer"},
                        "timestamp": {"type": "string"}
                    }
                },
                "BillOfLading": {
                    "type": "object",
                    "properties": {
                        "bl_number": {"type": "string"},
                        "carrier": {"type": "string"},
                        "shipper": {"type": "string"},
                        "consignee": {"type": "string"},
                        "commodity": {"type": "string"},
                        "value_usd": {"type": "number"}
                    }
                },
                "FactoryAuditRecord": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "factory_name": {"type": "string"},
                        "score": {"type": "integer"},
                        "passed": {"type": "boolean"}
                    }
                },
                "AuditSubmitRequest": {
                    "type": "object",
                    "required": ["factory_name", "scores"],
                    "properties": {
                        "factory_name": {"type": "string"},
                        "inspector": {"type": "string"},
                        "scores": {"type": "object"}
                    }
                },
                "AuditSubmitResponse": {
                    "type": "object",
                    "properties": {
                        "ok": {"type": "boolean"},
                        "audit_id": {"type": "string"},
                        "total_score": {"type": "integer"}
                    }
                },
                "HsSummaryResponse": {
                    "type": "object",
                    "properties": {
                        "sections_count": {"type": "integer"},
                        "chapters_count": {"type": "integer"},
                        "clusters_count": {"type": "integer"},
                        "products_count": {"type": "integer"}
                    }
                },
                "HsCatalogResponse": {
                    "type": "object",
                    "properties": {
                        "mode": {"type": "string"},
                        "groups": {"type": "array", "items": {"type": "object"}}
                    }
                },
                "HsSearchResponse": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "results": {"type": "array", "items": {"type": "object"}}
                    }
                },
                "HsProductsResponse": {
                    "type": "object",
                    "properties": {
                        "total": {"type": "integer"},
                        "products": {"type": "array", "items": {"type": "object"}}
                    }
                },
                "Regulation": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "title": {"type": "string"},
                        "scope": {"type": "string"},
                        "effective_date": {"type": "string"},
                        "risk_level": {"type": "string"}
                    }
                },
                "RegulationMilestone": {
                    "type": "object",
                    "properties": {
                        "regulation_id": {"type": "string"},
                        "milestone": {"type": "string"},
                        "deadline": {"type": "string"}
                    }
                },
                "RegulationDetailResponse": {
                    "type": "object",
                    "properties": {
                        "ok": {"type": "boolean"},
                        "regulation": {"type": "object"}
                    }
                },
                "RegulationAlertRequest": {
                    "type": "object",
                    "required": ["regulation_id"],
                    "properties": {
                        "regulation_id": {"type": "string"},
                        "impact_assessment": {"type": "string"}
                    }
                },
                "TradeTagsCatalogResponse": {
                    "type": "object",
                    "properties": {
                        "total_tags": {"type": "integer"},
                        "categories": {"type": "object"}
                    }
                },
                "TradeTagExplainResponse": {
                    "type": "object",
                    "properties": {
                        "ok": {"type": "boolean"},
                        "tag": {"type": "string"},
                        "name": {"type": "string"},
                        "category": {"type": "string"},
                        "business_meaning": {"type": "string"},
                        "recommendation": {"type": "string"}
                    }
                },
                "PriceBenchmarksResponse": {
                    "type": "object",
                    "properties": {
                        "updated_at": {"type": "string"},
                        "commodities": {"type": "array", "items": {"type": "object"}}
                    }
                },
                "PriceConvertRequest": {
                    "type": "object",
                    "required": ["value", "from_unit", "to_unit"],
                    "properties": {
                        "value": {"type": "number", "example": 2.5},
                        "from_unit": {"type": "string", "enum": ["lbs", "mt", "kg", "bag_60kg", "bag_50kg"], "example": "lbs"},
                        "to_unit": {"type": "string", "enum": ["lbs", "mt", "kg", "bag_60kg", "bag_50kg"], "example": "mt"},
                        "price_usd": {"type": "number", "example": 245.5},
                        "exchange_rate_vnd": {"type": "number", "example": 25450}
                    }
                },
                "PriceConvertResponse": {
                    "type": "object",
                    "properties": {
                        "ok": {"type": "boolean"},
                        "converted_value": {"type": "number"},
                        "equivalent_usd_per_mt": {"type": "number"},
                        "equivalent_vnd_per_kg": {"type": "number"}
                    }
                },
                "ArbitrageCalculateRequest": {
                    "type": "object",
                    "required": ["commodity_id", "buy_tier", "sell_tier"],
                    "properties": {
                        "commodity_id": {"type": "string", "example": "COMM-COFFEE-01"},
                        "buy_tier": {"type": "string", "example": "farmgate_vnd"},
                        "sell_tier": {"type": "string", "example": "cif_destination_usd"},
                        "estimated_freight_usd": {"type": "number", "example": 80.0}
                    }
                },
                "ArbitrageCalculateResponse": {
                    "type": "object",
                    "properties": {
                        "ok": {"type": "boolean"},
                        "commodity_name": {"type": "string"},
                        "gross_spread_usd": {"type": "number"},
                        "net_margin_percent": {"type": "number"},
                        "recommendation": {"type": "string"}
                    }
                },
                "TelegramDirectAlertRequest": {
                    "type": "object",
                    "required": ["title", "details"],
                    "properties": {
                        "title": {"type": "string"},
                        "details": {"type": "array", "items": {"type": "string"}},
                        "status_icon": {"type": "string", "default": "🚨"},
                        "action_required": {"type": "string"}
                    }
                }
            },
            "responses": {
                "NotFound": {
                    "description": "Không tìm thấy thực thể",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Error"}
                        }
                    }
                },
                "BadRequest": {
                    "description": "Dữ liệu yêu cầu không hợp lệ",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Error"}
                        }
                    }
                }
            }
        }
    }
    return spec

def get_swagger_ui_html(openapi_url="/api/openapi.json"):
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>API Documentation — Trade Intelligence & Verification Platform</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
  <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
  <style>
    body {{
      margin: 0;
      background: #0b1329;
      color: #f8fafc;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    .top-bar-branding {{
      background: #0f172a;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .top-bar-branding .title {{
      font-weight: 800;
      color: #38bdf8;
      font-size: 16px;
      letter-spacing: -0.02em;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .top-bar-branding .back-link {{
      color: #94a3b8;
      text-decoration: none;
      font-size: 13px;
      padding: 6px 14px;
      border-radius: 9999px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      transition: all 0.2s;
    }}
    .top-bar-branding .back-link:hover {{
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      border-color: rgba(56, 189, 248, 0.3);
    }}
    /* Dark Theme Customization for Swagger UI */
    .swagger-ui {{
      filter: invert(88%) hue-rotate(180deg);
    }}
    .swagger-ui .topbar {{
      display: none;
    }}
  </style>
</head>
<body>
  <div class="top-bar-branding">
    <div class="title">
      <span>🏛️ TẬP ĐOÀN ĐA NGÀNH</span>
      <span style="color: #64748b;">|</span>
      <span>TRADE INTELLIGENCE & VERIFICATION API SUITE</span>
      <span style="font-size: 10px; background: rgba(56, 189, 248, 0.2); color: #38bdf8; padding: 2px 8px; border-radius: 9999px; font-family: monospace;">v1.0.0</span>
    </div>
    <a href="/" class="back-link">← Quay lại Cổng XNK Portal</a>
  </div>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = function() {{
      window.ui = SwaggerUIBundle({{
        url: "{openapi_url}",
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout",
        defaultModelsExpandDepth: 1,
        defaultModelExpandDepth: 1,
        docExpansion: "list",
        filter: true
      }});
    }};
  </script>
</body>
</html>
"""

if __name__ == "__main__":
    spec = get_openapi_spec()
    print(f"✅ Generated OpenAPI Spec successfully! Total Paths: {len(spec['paths'])}, Total Schemas: {len(spec['components']['schemas'])}")
    with open("openapi.json", "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
    print("Saved to openapi.json")
