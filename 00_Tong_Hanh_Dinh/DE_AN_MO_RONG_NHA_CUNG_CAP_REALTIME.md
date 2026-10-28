# 🏛️ TẬP ĐOÀN HOLDING MASTER — ĐỀ ÁN CHIẾN LƯỢC
## ĐỀ ÁN: NÂNG CẤP ĐỘNG CƠ TÌNH BÁO & THẨM ĐỊNH NHÀ CUNG CẤP TOÀN CẦU THỜI GIAN THỰC
*(GLOBAL REAL-TIME VERIFIED SUPPLIER SOURCING & INTELLIGENCE ENGINE)*

---

### 1. BỐI CẢNH & NHU CẦU ĐIỀU HÀNH TỪ CHỦ TỊCH TẬP ĐOÀN
- **Thực trạng:** Danh mục Nhà Cung Cấp ban đầu lưu trữ 20 đối tác hạt nhân (mẫu thẩm định), chưa bao quát được các tập đoàn xuất khẩu khổng lồ của thế giới (Uralkali, EuroChem, Yara, Nutrien, ADM, Bunge, Wilmar...).
- **Chỉ đạo chiến lược của Chủ tịch:** Không sử dụng phương pháp "gom kho dữ liệu tĩnh để trích xuất", mà bắt buộc phải chuyển dịch sang mô hình **Cập nhật dữ liệu thực tế theo thời gian thực (Real-Time Live Data)** từ các nguồn chính thống và cơ quan quản lý quốc tế.

---

### 2. PHƯƠNG ÁN CÔNG NGHỆ: MÔ HÌNH LAI THỜI GIAN THỰC (HYBRID REAL-TIME ENGINE)
Kết hợp trọn vẹn sức mạnh của 2 trụ cột:
1. **Tính xác thực & Chiều sâu pháp lý (On-Demand Verification):** Khi người dùng tìm kiếm từ khóa, hệ thống kết nối trực tiếp đến các cổng API quốc tế để xác thực pháp nhân, người đại diện và tình trạng cấm vận ngay tại giây phút tra cứu.
2. **Độ phủ dữ liệu lớn & Vận hành tự động (Continuous Autonomous Pipeline):** Động cơ crawler chạy ngầm trên máy chủ VPS Singapore liên tục quét danh bạ các Hiệp hội ngành hàng thế giới, dữ liệu tờ khai hải quan và sàn đấu thầu công.

---

### 3. KIẾN TRÚC 5 TRỤ CỘT DỮ LIỆU CHÍNH THỐNG
1. **Trụ cột 1 - Hiệp hội Ngành hàng Quốc tế:** IFA (Phân bón), GAFTA & FOSFA (Ngũ cốc, Nông sản), ICO (Cà phê), INC (Hạt khô), WorldSteel (Thép), IRSG (Cao su).
2. **Trụ cột 2 - Cổng Định danh Pháp nhân Quốc gia:** GLEIF LEI (Toàn cầu), ĐKKD & Tổng cục Thuế (Việt Nam), EGRUL & SPARK (Nga), GSXT/SAMR (Trung Quốc), SEC EDGAR (Hoa Kỳ), VIES (Châu Âu).
3. **Trụ cột 3 - Dữ liệu Hải quan & Vận đơn (B/L) Thực tế:** US CBP ACE, GACC CIFER Trung Quốc, VNACCS Việt Nam, Eurostat Comext, AIS Live Vessel Tracking.
4. **Trụ cột 4 - Cổng Cấm vận & Rủi ro Đen:** OpenSanctions, OFAC SDN List (Hoa Kỳ), EU Sanctions Map, UN Sanctions, UFLPA Entity List.
5. **Trụ cột 5 - Cổng Chứng chỉ Chất lượng QA/QC:** IAF CertSearch (ISO/HACCP), ECHA REACH (Châu Âu), BRCGS, JAKIM/BPJPH Halal, Bản đồ số EUDR.

---

### 4. MA TRẬN CHẤM ĐIỂM TÍN NHIỆM NGOẠI THƯƠNG (360° AI SCORING)
- **Điểm Pháp lý & Tồn tại doanh nghiệp (20%):** Niên hạn hoạt động, vốn điều lệ thực góp.
- **Điểm Năng lực Cung ứng & Lịch sử Hải quan (30%):** Tần suất xuất nhập khẩu và số lượng cont thực tế.
- **Điểm Chứng chỉ Kỹ thuật QA/QC (20%):** Sở hữu chứng chỉ quốc tế còn hiệu lực.
- **Điểm Tín dụng Ngoại thương (15%):** Chấp nhận phương thức thanh toán an toàn (L/C At Sight, CAD).
- **Điểm An toàn Thuế & Hoàn thuế VAT (15%):** Lịch sử tuân thủ thuế và rà soát doanh nghiệp ma.

---

### 5. KẾ HOẠCH HÀNH ĐỘNG 3 GIAI ĐOẠN (SPRINT 7 NGÀY)

| Giai đoạn | Nội dung công việc | Đơn vị phụ trách | Thời hạn | Sản phẩm bàn giao |
| :--- | :--- | :--- | :---: | :--- |
| **Giai đoạn 1** | Tích hợp cổng API Pháp nhân Toàn cầu GLEIF và OpenSanctions Live trên VPS Singapore | Ban Công nghệ THD & Agency Digital | Ngày 1 - 2 | Module xác thực pháp nhân & quét cấm vận thời gian thực (<2s) |
| **Giai đoạn 2** | Xây dựng Pipeline tự động kết nối dữ liệu Hiệp hội (IFA, GAFTA, WorldSteel) & Luồng Vận đơn B/L | Ban Công nghệ THD & Khối XNK | Ngày 3 - 4 | 200+ Nhà cung cấp đầu ngành được nạp trực tiếp kèm dữ liệu thông quan |
| **Giai đoạn 3** | Tích hợp Động cơ Chấm điểm AI 5 Trọng số, hoàn thiện giao diện Sourcing và kiểm thử tự động | Ban Công nghệ THD & Ban Kiểm soát | Ngày 5 - 7 | Bản cập nhật live trên Cổng 8088 và Cổng 8099, sẵn sàng in PDF Dossier 360° |

---
*Ban hành tại Tổng Hành Dinh Tập Đoàn.*
