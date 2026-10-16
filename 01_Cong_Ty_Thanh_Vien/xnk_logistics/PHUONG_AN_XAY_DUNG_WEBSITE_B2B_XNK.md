# 🔍 ĐỀ ÁN CHIẾN LƯỢC: HỆ THỐNG NỀN TẢNG TÌNH BÁO THƯƠNG MẠI & THẨM ĐỊNH ĐỐI TÁC XNK (TRADE INTELLIGENCE & VERIFICATION ENGINE)

---

## 🏛️ 1. ĐỊNH HƯỚNG CỐT LÕI TỪ CHỦ TỊCH TẬP ĐOÀN
* **Trọng tâm tối thượng:** Không xây dựng website quảng bá sản phẩm thông thường. Nền tảng tập trung 100% vào năng lực **TÌM KIẾM CHỦ ĐỘNG** và **XÁC MINH / THẨM ĐỊNH CHUYÊN SÂU (DUE DILIGENCE)** đối với Khách hàng quốc tế (Buyers) và Nhà cung cấp tại Việt Nam (Suppliers).
* **Mục tiêu chiến lược:**
  1. Chủ động săn tìm người mua thật toàn cầu qua dữ liệu vận đơn và mạng lưới thương mại quốc tế.
  2. Dựng "Bức tường lửa" 4 tầng triệt tiêu lừa đảo ngoại thương, nợ xấu và cấm vận quốc tế.
  3. Khảo sát nguồn cung nội địa và kiểm toán triệt để rủi ro hóa đơn "ma" / trốn thuế của nhà xưởng Việt Nam, bảo đảm an toàn tuyệt đối cho dòng tiền hoàn thuế GTGT xuất khẩu ($8\% - 10\%$).

---

## 🧭 2. KIẾN TRÚC NỀN TẢNG: HAI TRỤC TÌM KIẾM & XÁC MINH CHUYÊN SÂU

```
                 🔍 TRADE INTELLIGENCE & VERIFICATION PLATFORM
                                       │
        ┌──────────────────────────────┴──────────────────────────────┐
        ▼                                                             ▼
[TRỤC I: BUYER INTELLIGENCE & KYC]             [TRỤC II: SUPPLIER AUDIT & TAX SHIELD]
TÌM KIẾM & XÁC MINH KHÁCH HÀNG QUỐC TẾ          TÌM KIẾM & KIỂM TOÁN NHÀ CUNG CẤP VN
        │                                                             │
        ├─ 1. Khai thác Vận đơn Hải quan (B/L)                        ├─ 1. Danh bạ Nguồn cung & Vùng nguyên liệu
        │     (ImportYeti, Panjiva, Trademo API)                      │     (Hiệp hội ngành hàng, KCN, HTX)
        ├─ 2. Tìm kiếm Đầu mối Sourcing & Buyer                       ├─ 2. Đối soát Tức thì Trạng thái Pháp lý
        │     (LinkedIn B2B / Email Intelligence)                     │     (API Cổng ĐKKD Quốc gia)
        ├─ 3. Bức tường lửa Thẩm định 4 Tầng                          ├─ 3. Bức tường lửa Hóa đơn & Thuế GTGT
        │     • KYC Cổng DN (UK, EU, US, TQ)                          │     • Quét cảnh báo rủi ro thuế / bỏ trốn
        │     • Quét Cấm vận (OFAC, EU, UN)                           │     • Thẩm định năng lực xuất hóa đơn chuẩn
        │     • Soi Tên miền & Email giả mạo                          ├─ 4. Số hóa Checklist Kiểm toán Thực địa
        │     • Chấm điểm Tín dụng & Lừa đảo                          │     (5 tiêu chuẩn nhà xưởng SOP-XNK-02)
        └─ 4. Đề xuất Hạn mức & Điều kiện TT                          └─ 5. Phân hạng & Đánh giá KPI Nhà cung cấp
              (L/C Khắt khe vs T/T Cọc 30-50%)                              (Hạng A/B/C/Blacklist)
```

---

## 🌐 3. CHI TIẾT CÁC TÍNH NĂNG NGHIỆP VỤ

### 3.1. Trục I: Tìm Kiếm & Xác Minh Khách Hàng Quốc Tế (Buyers)
1. **Công cụ Khai thác Dữ liệu Vận đơn Toàn cầu (Customs Manifest Scraper/API):**
   * Tích hợp tìm kiếm theo Mã HS, ngành hàng hoặc quốc gia:
     * Tự động lọc danh sách nhà nhập khẩu đang mua hàng từ Châu Á.
     * Thống kê sản lượng nhập khẩu thực tế (số container/tháng), cảng dỡ hàng (POD), nhà xuất khẩu hiện tại.
2. **Công cụ Khai thác Đầu mối Thu mua (Procurement Lead Extraction):**
   * Truy vết chức danh chuyên trách: *Head of Sourcing, Category Buyer, Supply Chain VP* của doanh nghiệp mục tiêu.
   * Xác thực email doanh nghiệp hợp lệ (loại trừ email chết, bounce).
3. **Bộ Công Cụ Thẩm Định Pháp Nhân & Gian Lận 4 Tầng (Automated Fraud Audit):**
   * **Tầng 1 - Tra cứu Pháp lý Quốc gia:** Kết nối dữ liệu kiểm tra mã số doanh nghiệp/mã VAT trực tiếp từ Cổng đăng ký doanh nghiệp các nước (Companies House Anh, VIES EU, Secretary of State Mỹ, Tianyancha Trung Quốc).
   * **Tầng 2 - Quét Danh sách Đen & Trừng phạt Toàn cầu (Sanctions Screening):** Tự động đối chiếu tên công ty, cá nhân quản lý trên danh sách trừng phạt quốc tế (OFAC Hoa Kỳ, EU Sanctions List, UN Consolidated List). Cảnh báo đỏ ngay lập tức nếu có liên quan đến các thực thể bị cấm vận tài chính.
   * **Tầng 3 - Soi Tên miền & Chống Phishing (Domain Forensics):** Phân tích tên miền email đối tác (Whois age, ngày đăng ký, DNS records). Tự động chặn và báo động nếu tên miền đăng ký dưới 12 tháng hoặc dùng đuôi email giả danh các tập đoàn lớn.
   * **Tầng 4 - Chấm điểm Rủi ro Tín dụng (Buyer Credit Scoring Engine):**
     * Tự động tổng hợp dữ liệu chấm điểm theo thang 100 điểm.
     * Khuyến nghị phương án thanh toán an toàn: Khách Hạng A (L/C không hủy ngang), Khách Hạng B (Đặt cọc $30\% - 50\%$ T/T), Khách Hạng C (Thu tiền trước 100%).

---

### 3.2. Trục II: Tìm Kiếm & Kiểm Toán Nhà Cung Cấp Nội Địa (Vietnam Suppliers)
1. **Kho Dữ liệu Mạng lưới Nguồn cung Việt Nam:**
   * Tập hợp dữ liệu nhà xưởng, hợp tác xã, cơ sở sơ chế theo ngành hàng thế mạnh: Nông sản, phân bón, hóa chất, vật tư, máy móc.
   * Phân loại theo vùng nguyên liệu, khu công nghiệp và chứng chỉ chất lượng sở hữu (HACCP, ISO, FDA, FSC, GlobalGAP).
2. **Bức Tường Lửa Thẩm Định Thuế & Pháp Lý (Tax Compliance Gate):**
   * **Xác thực ĐKKD tức thì:** Tự động kết nối cơ sở dữ liệu đăng ký kinh doanh quốc gia (dangkykinhdoanh.gov.vn) để kiểm tra tình trạng doanh nghiệp ("Đang hoạt động", vốn điều lệ, thâm niên).
   * **Bộ lọc Chống Rủi ro Hóa đơn "Ma" & Bỏ trốn:**
     * Quét tự động danh sách doanh nghiệp có rủi ro cao về thuế do Tổng cục Thuế công bố.
     * Cảnh báo nghiêm ngặt các công ty mới thành lập dưới 1 năm nhưng xuất hóa đơn quy mô lớn.
     * Ràng buộc ký cam kết chịu phạt 20% và hoàn trả 100% tiền thuế nếu hóa đơn bị cơ quan thuế bác bỏ khi xét hoàn thuế xuất khẩu.
3. **Ứng Dụng Số Hóa Kiểm Toán Thực Địa Nhà Xưởng (On-site Audit App/Tool):**
   * Số hóa Checklist 5 tiêu chuẩn thực địa của SOP-XNK-02:
     1. Công suất sản xuất thực tế/ngày (đếm máy móc, công nhân).
     2. Quy trình QA/QC & phòng đo lường chất lượng.
     3. Điều kiện bảo quản kho bãi & PCCC.
     4. Hồ sơ truy xuất nguồn gốc nguyên liệu (phục vụ cấp C/O thuần túy WO).
     5. Tiêu chuẩn lao động và bảo vệ môi trường.
   * Chuyên viên XNK đi kiểm tra cơ sở có thể chụp ảnh, chấm điểm trực tiếp từ thiết bị di động, đồng bộ ngay về Tổng Hành Dinh.

---

## 💻 4. KIẾN TRÚC CÔNG NGHỆ & HỆ THỐNG ĐIỀU HÀNH (KHỐI CNTT)

### 4.1. Giao diện Dashboard Tình báo Nội bộ (Private Trade Intelligence Dashboard)
* Màn hình tra cứu tập trung chuẩn "Search & Verify":
  * Nhập Tên đối tác / Mã HS / Mã số thuế / Tên miền email -> Xuất ngay **Báo cáo Thẩm định Độc lập 360 độ (Due Diligence Report)** trong 30 giây.
* Hệ thống phân cấp bảo mật dữ liệu nguồn cung và dữ liệu khách hàng theo chuẩn quản trị tập đoàn.

### 4.2. Cổng Tự Khai Báo Dành Cho Đối Tác (External Self-KYC Portal)
* Dành cho đối tác muốn giao thương với Tập đoàn: Tự động tải lên ĐKKD, chứng chỉ, hồ sơ năng lực. Hệ thống tự động kích hoạt bot thẩm định ngầm trước khi chuyên viên can thiệp.

### 4.3. Hệ Thống Cảnh Báo Rủi Ro Tức Thì (Telegram Risk Alert Bot)
* Bắn thông báo khẩn cấp vào nhóm điều hành Khối XNK khi phát hiện:
  * Khách quốc tế nằm trong diện cảnh báo trừng phạt OFAC/EU hoặc tên miền mới tạo dưới 6 tháng.
  * Nhà cung cấp Việt Nam có dấu hiệu nợ thuế, đổi trụ sở bất thường hoặc nằm trong danh sách rủi ro hóa đơn.

---

## ⏱️ 5. LỘ TRÌNH TRIỂN KHAI 3 GIAI ĐOẠN (5 TUẦN)

* **Giai đoạn 1 (Tuần 1 - 2):** Xây dựng lõi cơ sở dữ liệu xác minh (Database Schema), kết nối các nguồn API tra cứu pháp lý/thuế/cấm vận; thiết kế giao diện Dashboard "Search & Verify".
* **Giai đoạn 2 (Tuần 3 - 4):** Lập trình các bộ công cụ thẩm định 4 tầng cho Buyer và bức tường lửa thuế cho Supplier; số hóa checklist kiểm toán thực địa trên di động; tích hợp Telegram Bot cảnh báo.
* **Giai đoạn 3 (Tuần 5):** Thử nghiệm xác minh trên 50 hồ sơ khách hàng quốc tế và nhà cung cấp nội địa thực tế; đánh giá độ chính xác, bảo mật dữ liệu và bàn giao vận hành.

---
*Kính trình Chủ tịch Tập đoàn phê duyệt chủ trương triển khai.*
