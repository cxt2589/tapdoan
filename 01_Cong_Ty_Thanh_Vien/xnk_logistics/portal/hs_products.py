# -*- coding: utf-8 -*-
"""
Hệ Thống Danh Mục Sản Phẩm Toàn Diện Theo Mã Ngành WCO (Master Products & HS Subheadings Catalog)
Khối Xuất Nhập Khẩu & Thương Mại Quốc Tế Tập Đoàn

Cung cấp tra cứu chi tiết đến cấp độ sản phẩm (HS 4 số và 6 số) cho toàn bộ 97 Chương HS
và các Ngành Hàng Chiến Lược Xuất Nhập Khẩu của Việt Nam và Quốc Tế.
"""

import os
import json
import re
import unicodedata

def remove_diacritics(text):
    """Chuyển đổi chuỗi tiếng Việt có dấu thành không dấu để tìm kiếm thông minh"""
    if not text:
        return ""
    text = unicodedata.normalize('NFD', text)
    text = re.sub(r'[\u0300-\u036f]', '', text)
    text = text.replace('đ', 'd').replace('Đ', 'D')
    return text.lower()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(CURRENT_DIR, "data", "hs_products_master.json")

def load_products_master():
    """Tải toàn bộ danh bạ sản phẩm từ JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[hs_products] Lỗi đọc {DATA_FILE}: {e}")
    return []

ALL_PRODUCTS_MASTER = load_products_master()

def search_products_master(query, limit=20):
    """
    Tìm kiếm thông minh sản phẩm cụ thể theo:
    - Tên sản phẩm tiếng Việt (có dấu hoặc không dấu)
    - Tên tiếng Anh
    - Mã HS 4 số hoặc 6 số (chính xác hoặc bắt đầu bằng)
    - Từ khóa nghiệp vụ, quy cách thương mại
    - Mã chương HS (ví dụ '09', '72', '85')
    """
    q_raw = (query or "").strip().lower()
    if not q_raw:
        return ALL_PRODUCTS_MASTER[:limit]
    
    q_norm = remove_diacritics(q_raw)
    q_digits = re.sub(r'[^0-9]', '', q_raw)

    matched = []
    for prod in ALL_PRODUCTS_MASTER:
        score = 0
        hs_clean = prod.get("hs", "").replace(".", "")
        name_vi_norm = remove_diacritics(prod.get("name_vi", ""))
        name_en_lower = prod.get("name_en", "").lower()
        keywords_norm = [remove_diacritics(k) for k in prod.get("keywords", [])]

        # 1. So khớp mã HS
        if q_digits and hs_clean.startswith(q_digits):
            score += 120
        elif q_raw in prod.get("hs", ""):
            score += 100

        # 2. So khớp tên tiếng Việt
        if q_norm == name_vi_norm:
            score += 100
        elif q_norm in name_vi_norm:
            score += 70

        # 3. So khớp từ khóa
        if any(q_norm == kw for kw in keywords_norm):
            score += 80
        elif any(q_norm in kw for kw in keywords_norm):
            score += 50

        # 4. So khớp tên tiếng Anh
        if q_raw in name_en_lower:
            score += 40

        # 5. So khớp mã chương
        if q_raw == prod.get("chapter_code", ""):
            score += 35

        if score > 0:
            item_copy = dict(prod)
            item_copy["search_relevance"] = score
            matched.append(item_copy)

    matched.sort(key=lambda x: x["search_relevance"], reverse=True)
    return matched[:limit]

def get_products_by_chapter(chapter_code):
    """Lấy danh sách tất cả sản phẩm thuộc về một Chương HS cụ thể"""
    code_str = str(chapter_code).strip().zfill(2)
    return [p for p in ALL_PRODUCTS_MASTER if p.get("chapter_code") == code_str]

def get_products_by_sector(sector_name):
    """Lấy danh sách tất cả sản phẩm thuộc một Ngành hàng"""
    sec_norm = remove_diacritics(sector_name)
    return [p for p in ALL_PRODUCTS_MASTER if sec_norm in remove_diacritics(p.get("sector", ""))]

def get_products_count():
    """Tổng số sản phẩm chuẩn hóa đã đăng ký trong danh bạ"""
    return len(ALL_PRODUCTS_MASTER)

def get_all_products():
    """Lấy toàn bộ danh bạ sản phẩm"""
    return ALL_PRODUCTS_MASTER
