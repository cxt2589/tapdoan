# 🚢 CÔNG TY XUẤT NHẬP KHẨU & THƯƠNG MẠI QUỐC TẾ TẬP ĐOÀN (AGENCY GLOBAL LOGISTICS & TRADE - XNK)

---

## 🏛️ GIỚI THIỆU TỔNG QUAN
Công ty Xuất Nhập Khẩu & Thương Mại Quốc Tế (mã công ty thành viên: **`SUBSIDIARY-05`**) là đơn vị thành viên độc lập trực thuộc Tập đoàn, chịu trách nhiệm quản trị toàn bộ hoạt động ngoại thương, chuỗi cung ứng quốc tế, khai báo hải quan, áp mã HS, chứng từ ngoại thương và vận tải đa phương thức.

* **Trụ sở làm việc:** `D:\project antigravity\Project\XNK`
* **Cơ chế quản trị:** Chủ tịch Tập đoàn trực tiếp chỉ đạo ⇄ Giám đốc Xuất Nhập Khẩu (Managing Director of Global Trade & Logistics) điều hành cùng Thư ký riêng đi cùng.
* **Cổng kỹ năng chuyên môn:** Kích hoạt tự động [`import-export-specialist`](file:///D:/project%20antigravity/Project/XNK/.agents/skills/import-export-specialist/SKILL.md).

---

## 📂 CẤU TRÚC THƯ MỤC VẬN HÀNH

```
D:\project antigravity\Project\XNK\
├── .agents/
│   └── skills/
│       └── import-export-specialist/
│           └── SKILL.md                  <-- Kỹ năng cốt lõi toàn diện về XNK & Hải quan
├── 01_HS_Code_Va_Thue/                   <-- Tài liệu tra cứu mã HS, biểu thuế XNK, ghi chú WCO
├── 02_Bo_Chung_Tu_Mau/                   <-- Mẫu Sales Contract, CI, PL, B/L, C/O Form E/D/EUR.1
├── 03_Hai_Quan_VNACCS/                   <-- Hướng dẫn tờ khai IDA/IDC, xử lý luồng Vàng/Đỏ
├── 04_Logistics_Incoterms/               <-- Cẩm nang Incoterms 2020, biểu phí Local charges
├── 05_Lo_Hang_Thuc_Te/                   <-- Lưu trữ hồ sơ từng lô hàng (Shipment / PO)
├── scripts/
│   ├── calculate_landed_cost.py          <-- Tool tính chi phí cập kho (Landed Cost), thuế NK, VAT
│   ├── dem_det_tracker.py                <-- Tool giám sát hạn free time bến bãi & cảnh báo phạt DEM/DET
│   └── check_co_rules.py                 <-- Tool tra cứu nhanh FTA và tiêu chí C/O ưu đãi 0%
├── AGENTS.md                             <-- Quy tắc điều hành Chủ tịch ⇄ Giám đốc & Danh mục nhân sự
├── GEMINI.md                             <-- Chỉ dẫn vận hành AI Agent tại Khối XNK
├── SO_TAY_THU_KY.md                      <-- Sổ tay Thư ký theo dõi chỉ thị & đường ống lô hàng
├── QUY_TRINH_XUAT_NHAP_KHAU_CHUAN.md     <-- Cẩm nang quy trình 8 bước XNK thực chiến
└── README.md                             <-- Tài liệu giới thiệu Khối XNK
```

---

## ⚡ CÁC CÔNG CỤ TÍNH TOÁN ĐÃ ĐƯỢC TÍCH HỢP
1. **Tính Chi phí Cập kho (Landed Cost):**
   ```bash
   python scripts/calculate_landed_cost.py
   ```
2. **Cảnh báo Thời hạn Lưu bãi & Lưu Cont (DEM/DET):**
   ```bash
   python scripts/dem_det_tracker.py
   ```
3. **Tra cứu Quy tắc C/O & Ưu đãi Thuế quan FTA:**
   ```bash
   python scripts/check_co_rules.py "Trung Quoc"
   ```
