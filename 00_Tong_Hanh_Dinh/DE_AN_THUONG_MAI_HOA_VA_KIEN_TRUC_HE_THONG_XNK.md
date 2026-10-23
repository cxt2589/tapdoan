# 🏛️ TÀI LIỆU TỔNG THỂ KIẾN TRÚC HỆ THỐNG & ĐỀ ÁN THƯƠNG MẠI HÓA
## NỀN TẢNG TÌNH BÁO, THẨM ĐỊNH & KHỚP LỆNH NGOẠI THƯƠNG B2B (XNK TRADE INTELLIGENCE PORTAL)

**Đơn vị ban hành:** Văn phòng Tổng Giám Đốc & Ban Chiến Lược — Tổng Hành Dinh Tập Đoàn  
**Trình phê duyệt:** Chủ tịch Tập đoàn Cao Xuân Trường  
**Phiên bản:** Enterprise Master v4.0  
**Hạ tầng vận hành:** Cụm Máy chủ Hải ngoại Singapore Node 1 (103.228.74.58 / Cloudflare SSL Edge)

---

## MỤC LỤC
1. **PHẦN I:** Tổng quan Hệ sinh thái & Kiến trúc Kỹ thuật Nền tảng
2. **PHẦN II:** Chi tiết 10 Phân hệ Chức năng Cốt lõi (Functional Architecture)
3. **PHẦN III:** Danh mục Toàn diện 34 Cổng Giao tiếp Dữ liệu (Web Views & RESTful APIs)
4. **PHẦN IV:** Đề án Thương mại hóa Đa phương (Sale Nhà Cung Cấp, Sale Bên Mua & Xúc Tiến Thương Mại)
5. **PHẦN V:** Kiến trúc Chuyển đổi SaaS Đa Khách hàng (Multi-Tenant RBAC & Broker Protection)
6. **PHẦN VI:** Mô hình Doanh thu, Bảng giá Thương mại & Hiệp lực Liên Công ty (Synergy)
7. **PHẦN VII:** Lộ trình Triển khai Thực chiến (Action Plan)

---

# PHẦN I. TỔNG QUAN HỆ SINH THÁI & KIẾN TRÚC KỸ THUẬT

### 1. Tầm nhìn & Định vị Hệ thống
Nền tảng Tình Báo, Thẩm Định & Khớp Lệnh Ngoại Thương B2B là hệ thống điều hành thương mại quốc tế tích hợp toàn diện đầu tiên kết hợp 4 trụ cột công nghệ ngoại thương đắt giá nhất thế giới vào trong một nền tảng duy nhất:
* Tình báo Hải quan & Vận đơn 2 chiều (Tương đương Panjiva / ImportGenius nhưng bóc tách sâu đến đơn giá hải quan, tần suất nhập hàng và chuỗi đối tác 2 đầu).
* Thẩm định Tín nhiệm 4 Tầng & Bức tường lửa Thuế (Tương đương Dun & Bradstreet / Dow Jones Risk kết hợp kiểm toán thực địa nhà máy chuẩn SOP-02 và an toàn hoàn thuế GTGT).
* Bàn Khớp Lệnh Giao Dịch AI 6 Chiều & Bộ Đôi RFQ Giáp Lưng (Tự động hóa hoàn toàn quy trình của một Sàn Môi giới Hàng hóa Quốc tế).
* Radar Pháp lý Toàn cầu & Đối soát Giá Đa Sàn (Tương đương Bloomberg Commodity & Thomson Reuters Regulatory cho các rào cản EUDR, CBAM, UFLPA, GACC).

### 2. Quy mô Cơ sở Dữ liệu Hiện hữu (Production Database)
* Khách mua Quốc tế (Global Buyers Pool): 1.000 tập đoàn nhập khẩu và phân phối lớn trên toàn cầu, phân bổ theo phễu 3 tầng:
  * Tầng 1 (Data thô / Raw Signals): 496 doanh nghiệp.
  * Tầng 2 (Hạng B / Qualified Buyers): 296 doanh nghiệp.
  * Tầng 3 (Hạng A & A+ / VIP Global Buyers): 208 tập đoàn đầu ngành.
* Nhà cung cấp & Đại lý Cấp 1 (Global Suppliers & Tier-1 Master Agents): 20 nhà cung cấp chiến lược (bao gồm 9 Đại lý Cấp 1 toàn cầu và hệ thống nhà máy sản xuất xuất khẩu chủ lực).
* Hệ thống Phân loại Hàng hóa Quốc tế: Đầy đủ 97 chương Mã HS theo chuẩn Tổ chức Hải quan Thế giới (WCO), đi sâu vào 213 dòng sản phẩm xuất nhập khẩu chiến lược thuộc 5 khối ngành trụ cột.
* Độ phủ Địa kinh tế: 8 đại khu vực (Châu Âu EU, Bắc Mỹ, Trung Đông GCC, Đông Á, Đông Nam Á ASEAN, Liên bang Nga & EAEU, Nam Mỹ, Châu Phi).

---

# PHẦN II. CHI TIẾT 10 PHÂN HỆ CHỨC NĂNG CỐT LÕI

### Phân hệ 1: Săn tìm & Sàng lọc Khách hàng Quốc tế (Global Buyer Prospecting Engine)
* Phễu sàng lọc 3 tầng: Tự động phân loại khách mua từ tín hiệu thô (Tầng 1) sang doanh nghiệp đã xác thực nhu cầu (Hạng B) và tập đoàn uy tín cao (Hạng A/A+).
* Bộ lọc đa chiều thông minh: Cho phép lọc kết hợp cùng lúc theo: Khối ngành (5 ngành), Chương HS (97 chương), Cụm ngành kinh tế (Clusters), Mã HS chi tiết, Khu vực địa lý (8 vùng), Quốc gia cụ thể và Từ khóa tìm kiếm.
* Trải nghiệm Mobile & Desktop tối ưu: Thanh tìm kiếm gợi ý thả nổi không làm xê dịch bố cục (Zero-Displacement), cố định thanh điều hướng (Sticky Menu) và trích xuất dữ liệu ra tệp CSV chuẩn CRM.

### Phân hệ 2: Hồ sơ Tình báo Doanh nghiệp 360° (360° Company Intelligence Dossier)
* Thông tin định danh & Quy mô tài chính: Cung cấp mã số thuế/EORI/LEI, quốc gia, phân hạng tín nhiệm, Doanh thu ước tính hàng năm bằng con số định lượng cụ thể và năng lực thanh toán.
* Mạng lưới Đối tác Ngoại thương Toàn cầu: Thống kê tổng số đối tác trên toàn thế giới, phân bổ chi tiết theo từng quốc gia (kèm bộ lọc nước linh hoạt) và cho phép bấm xem hồ sơ 360° của từng đối tác trong chuỗi cung ứng, tỷ lệ đơn hàng thành công và lịch sử hợp tác.
* Đánh giá Nhu cầu Mở rộng Nguồn cung Địa lý: Phân tích mức độ phụ thuộc của khách mua vào các nguồn cung hiện tại, tính toán Tỷ lệ khả thi kết nối (%) và đề xuất danh sách Nhà cung cấp đối ứng phù hợp nhất.
* Danh bạ Người Quyết định (Decision-Maker Contacts): Mở khóa thông tin liên lạc trực tiếp của Giám đốc Thu mua, Trưởng phòng XNK (Họ tên, Chức vụ, Email công vụ, Số điện thoại/WhatsApp/WeChat).

### Phân hệ 3: Tình báo Vận đơn Hải quan B/L 2 Chiều & Tín hiệu Sàn B2B
* Kho Vận đơn Hải quan Hợp nhất: Tích hợp đồng bộ vận đơn từ cả phía Khách hàng nhập khẩu và phía Nhà cung cấp xuất khẩu.
* Chỉ số Thống kê Chuyên sâu: Tự động tính tổng sản lượng và số lượng vận đơn trong 1 năm qua, tần suất giao dịch trung bình/tháng, cảng xếp hàng (POL), cảng dỡ hàng (POD), hãng tàu vận chuyển.
* Minh bạch Đơn giá & Đối tác: Hiển thị rõ Đơn giá Hải quan (Unit Price USD/MT), Tổng trị giá lô hàng, nhãn minh bạch hải quan và tên Nhà cung cấp đối ứng của từng vận đơn.
* Tín hiệu Sàn B2B Quốc tế: Theo dõi các gói thầu hỏi mua hàng (RFQ Signals) mới nhất trên các sàn B2B toàn cầu kèm thông tin đối tác nhà cung cấp đã chốt đơn.
* Liên kết Xuyên suốt: Mọi mã số vận đơn B/L trên toàn hệ thống đều có thể nhấp chuột trực tiếp để mở Hồ sơ Vận đơn Chi tiết và phát lệnh tạo Bộ Đôi RFQ.

### Phân hệ 4: Thẩm định Tín nhiệm 4 Tầng & Bức tường lửa Thuế (4-Tier Due Diligence Engine)
* Quy trình Thẩm định Khách mua 4 Tầng Chuyên sâu:
  * Tầng 1 (Pháp nhân & Định danh số): Kiểm tra trạng thái đăng ký kinh doanh, tuổi đời hoạt động, độ tin cậy của tên miền website và xác thực email doanh nghiệp (cảnh báo đỏ nếu dùng email miễn phí).
  * Tầng 2 (Rà soát Trừng phạt & Cấm vận Quốc tế): Đối chiếu tự động với danh sách OFAC (Mỹ), EU Sanctions (Châu Âu), UN Consolidated List.
  * Tầng 3 (Đối soát Giao dịch Ngoại thương Thực tế): Tự động đối chiếu chéo với kho vận đơn B/L và lịch sử đối tác để xác nhận năng lực nhập khẩu thực tế, loại bỏ hoàn toàn tình trạng sai lệch dữ liệu giữa hồ sơ và vận đơn.
  * Tầng 4 (Định lượng Doanh thu & Ma trận Đòn bẩy Vốn - Capital Leverage Matrix): Ước tính doanh thu bằng số liệu cụ thể, giải trình rõ hệ số đòn bẩy thương mại, hạn mức cấp tín dụng tối đa và khuyến nghị điều khoản thanh toán an toàn (L/C at sight, T/T đặt cọc, D/P).
* Bức tường lửa Thuế Nhà cung cấp & Kiểm toán Xưởng (SOP-02):
  * Đánh giá tỷ lệ An toàn hoàn thuế GTGT (%), phát hiện tức thì doanh nghiệp có rủi ro về hóa đơn hoặc doanh nghiệp ma.
  * Tích hợp biên bản và quy trình Kiểm toán Nhà máy / Xưởng sản xuất thực địa theo quy chuẩn SOP-02 (xác minh dây chuyền, công suất thực, kho bãi, nhân công và chứng chỉ ISO/HACCP).
* Biểu mẫu Thẩm định 360° Chuẩn Quốc tế (In ấn A4/PDF): Tự động kết xuất báo cáo thẩm định đầy đủ các bảng biểu, mạng lưới đối tác, vận đơn B/L và khung ký duyệt của Giám đốc Điều hành.

### Phân hệ 5: Nhà cung cấp Chiến lược & Đại lý Cấp 1 Toàn cầu (Suppliers & Tier-1 Master Agents)
* Quản lý hồ sơ chi tiết của 20 Nhà cung cấp chiến lược và 9 Đại lý Cấp 1 toàn cầu (Thụy Sĩ, Liên bang Nga, UAE, Singapore, Việt Nam...).
* Bộ lọc chính xác tuyệt đối theo phân loại đại lý và quốc gia sở tại.
* Cung cấp Hồ sơ Năng lực Nhà cung cấp (Supplier Dossier Modal) với định tuyến thẩm định tự động.

### Phân hệ 6: Bàn Khớp Lệnh Giao Dịch B2B Ma Trận 6 Chiều (6D Trade Matchmaker)
* Thuật toán Chấm điểm Khớp lệnh 6 Chiều (Thang điểm 100):
  1. Tương thích Hàng hóa & Mã HS (25 điểm): Khớp chính xác phân nhóm HS và chủng loại sản phẩm.
  2. Dung lượng & Sản lượng (15 điểm): Cân đối nhu cầu nhập khẩu của Buyer và công suất cung ứng của Supplier.
  3. Biên lợi nhuận & Giá trị thương vụ (20 điểm): Tính toán chênh lệch giá (Spread) giữa giá chào FOB của nhà máy và giá mục tiêu CIF/CFR của khách mua.
  4. Tuyến vận tải biển & Incoterms (15 điểm): Độ tương thích cảng đi – cảng đến và điều kiện giao hàng.
  5. Độ khớp Quy chuẩn Kỹ thuật - Trade Tags (15 điểm): Đối chiếu tự động các thẻ tiêu chuẩn và chỉ rõ Điểm vênh thương thảo (Negotiation Friction Points).
  6. Tín nhiệm & An toàn Thanh toán (10 điểm): Đánh giá rủi ro pháp lý và tài chính của cả hai đầu.
* Phân hạng Thương vụ: Tự động xếp hạng KIM CƯƠNG (Diamond ≥ 85 điểm), VÀNG (Gold 75–84 điểm), BẠC (Silver < 75 điểm).
* Cơ chế Luân chuyển Đa ngành (Daily Seed Rotation & Interleaved Diversity): Tự động phân bổ xen kẽ 5 khối ngành trụ cột trên bảng khớp lệnh và luân chuyển đối tác mỗi ngày.

### Phân hệ 7: Tự động hóa Chào hàng B2B & Động cơ Bộ Đôi RFQ (Dual-RFQ Engine)
* AI Sinh Thư Chào Hàng Đa Ngôn Ngữ: Tạo thư chào hàng chuẩn văn phong ngoại thương bằng 5 ngôn ngữ (Anh, Nga, Trung, Ả Rập, Việt) cá nhân hóa theo từng khách hàng.
* Bộ Đôi RFQ Đối Ứng (Dual-Side Back-to-Back RFQ): Tự động soạn thảo song song 2 văn bản:
  * Bản 1 (Gửi Khách mua Quốc tế): Báo giá xuất khẩu chuyên nghiệp (FOB/CFR/CIF) kèm thông số kỹ thuật và điều khoản thanh toán.
  * Bản 2 (Gửi Nhà cung cấp/Nhà máy): Thư hỏi mua hàng/đặt hàng sản xuất đối ứng để khóa nguồn cung và chốt biên lợi nhuận trung gian.

### Phân hệ 8: Đại Từ điển 97 Chương Mã HS WCO & 213 Sản phẩm Xuất nhập khẩu
* Tra cứu toàn bộ 97 chương thuộc Hệ thống Hài hòa Mô tả và Mã hóa Hàng hóa của WCO.
* Hỗ trợ 4 góc nhìn chiến lược: Theo quy mô kim ngạch, Theo cụm ngành liên kết, Theo bảng chữ cái, và Theo thứ tự chương WCO.
* Liên kết trực tiếp từ từng chương/sản phẩm HS sang danh sách Khách mua và Vận đơn B/L tương ứng.

### Phân hệ 9: Radar Pháp lý Ngoại thương & Từ điển Thẻ Tag Kỹ thuật
* Radar Pháp lý & Chân trời Chính sách (Regulatory Horizon): Giám sát các đạo luật thương mại khắt khe nhất: EUDR (EU), CBAM (EU), UFLPA (Mỹ), GACC Lệnh 248/249 (Trung Quốc), kèm lịch trình có hiệu lực, danh sách mã HS chịu ảnh hưởng và hướng dẫn bộ chứng từ tuân thủ.
* Động cơ Giải nghĩa Thẻ Tag Kỹ thuật (Trade Tags Tooltip Engine): Khi người dùng rê chuột hoặc nhấn vào bất kỳ thẻ kỹ thuật nào, hệ thống hiển thị ngay định nghĩa chuyên môn, tiêu chuẩn kiểm định và chiến thuật đàm phán.

### Phân hệ 10: Cơ sở dữ liệu Giá Hàng hóa Đa Sàn & Trợ lý Telegram 06:30 Sáng
* Bảng Giá Đa Sàn Chiến Lược (/prices): Cập nhật giá tham chiếu 6 mặt hàng chủ lực trên các sàn quốc tế kèm công cụ chuẩn hóa quy đổi đơn vị tự động.
* Bản tin Telegram Tự động 06:30 Sáng: Mỗi sáng tự động tuyển chọn 4 cặp giao dịch Kim Cương đại diện cho 4 ngành hàng khác nhau, đính kèm phân tích biên lợi nhuận và gửi trực tiếp về Telegram điều hành (có cơ chế khóa chống trùng lặp 1 lần/ngày).

---

# PHẦN III. DANH MỤC TOÀN DIỆN 34 CỔNG GIAO TIẾP (API ENDPOINTS)

Hệ thống cung cấp 34 cổng giao tiếp (gồm 2 cổng giao diện Web và 32 cổng RESTful API):

| STT | Phương thức | Đường dẫn Endpoint | Tham số Truy vấn / Payload Chính | Mô tả Chức năng Chi tiết |
| :---: | :---: | :--- | :--- | :--- |
| **01** | `GET` | `/` | Không | Tải giao diện Bàn điều hành chính (Single-Page Application, hỗ trợ Light/Dark Mode) |
| **02** | `GET` | `/prices` | Không | Tải chuyên trang Bảng Giá Hàng Hóa Đa Sàn & Công cụ Chuẩn hóa Đơn vị |
| **03** | `GET` | `/api/health` | Không | Kiểm tra sức khỏe máy chủ, trạng thái ONLINE, số lượng ngành và tổng số Leads |
| **04** | `GET` | `/api/industries` | Không | Danh mục 5 khối ngành trụ cột, biểu tượng và danh sách mặt hàng con |
| **05** | `GET` | `/api/regions` | Không | Danh mục 8 khu vực thị trường địa kinh tế toàn cầu |
| **06** | `GET` | `/api/leads/by-industry` | `industry`, `chapter`, `cluster`, `hs`, `region`, `country`, `stage`, `q`, `page`, `page_size` | Động cơ săn tìm và lọc danh sách khách mua quốc tế đa tiêu chí |
| **07** | `GET` | `/api/leads/detail` | `id` (Mã khách hàng) | Truy xuất Hồ sơ Tình báo Doanh nghiệp 360°, lịch sử B/L, sàn B2B và mạng lưới đối tác |
| **08** | `GET` | `/api/leads/sourcing-evaluation` | `id` (Mã khách hàng) | Đánh giá nhu cầu mở rộng nguồn cung địa lý, tỷ lệ khả thi kết nối & đề xuất NCC |
| **09** | `POST` | `/api/leads/generate-outreach` | `lead_id`, `lang`, `sender_info` | AI sinh thư chào hàng B2B đa ngôn ngữ cá nhân hóa theo lịch sử nhập khẩu |
| **10** | `GET` | `/api/leads/export-csv` | `industry`, `region`, `stage`, `q` | Xuất danh sách khách hàng tiềm năng ra tệp CSV phục vụ bộ phận Sales |
| **11** | `POST` | `/api/leads/refresh-sync` | Không | Đồng bộ và làm mới dữ liệu tín hiệu thị trường, vận đơn và RFQ |
| **12** | `POST` | `/api/verify/buyer` | `company_name`, `country`, `email`, `website`, `tax_id` | Thẩm định tín nhiệm Khách mua 4 tầng, rà soát cấm vận, doanh thu & đòn bẩy vốn |
| **13** | `POST` | `/api/verify/supplier` | `company_name`, `tax_code`, `country`, `id` | Bức tường lửa Thuế thẩm định Nhà cung cấp, an toàn hoàn thuế & SOP-02 |
| **14** | `GET` | `/api/suppliers` | `type`, `country`, `industry`, `q` | Truy vấn danh sách 20 Nhà cung cấp chiến lược & 9 Đại lý Cấp 1 toàn cầu |
| **15** | `GET` | `/api/suppliers/detail` | `id` (Mã nhà cung cấp) | Hồ sơ năng lực 360° của Nhà cung cấp, công suất, chứng chỉ & vận đơn xuất khẩu |
| **16** | `GET` | `/api/discovery/bl` | `hs`, `q`, `time_filter`, `route`, `page`, `page_size` | Tra cứu kho Vận đơn Hải quan B/L toàn cầu theo mã HS, tuyến biển và thời gian |
| **17** | `GET` | `/api/discovery/bl/detail` | `bl_number` (Số vận đơn) | Hồ sơ chi tiết Vận đơn B/L, đơn giá hải quan, lịch sử cặp đối tác & kích hoạt RFQ |
| **18** | `GET` | `/api/contacts` | `type`, `id` | Truy xuất danh bạ Người quyết định (Giám đốc thu mua, Trưởng phòng XNK) |
| **19** | `GET` | `/api/matches/metrics` | Không | Thống kê chỉ số Bàn Khớp Lệnh: Tổng giá trị Pipeline, số cặp Kim Cương/Vàng/Bạc |
| **20** | `GET` | `/api/matches` | `tier`, `industry`, `min_score`, `q`, `page`, `page_size` | Săn tìm & xếp hạng các cặp Khớp lệnh Ma trận 6 Chiều (phân bổ so le đa ngành) |
| **21** | `POST` | `/api/matches/analyze` | `buyer_id`, `supplier_id` | Đối soát chuyên sâu Ma trận 6 Chiều, bài toán biên lợi nhuận & điểm vênh thương thảo |
| **22** | `POST` | `/api/matches/generate-dual-rfq` | `buyer_id`, `supplier_id`, `commodity`, `hs_code` | Sinh đồng thời Bộ Đôi RFQ: Báo giá gửi Buyer & Thư hỏi hàng gửi Supplier |
| **23** | `POST` | `/api/matches/notify-telegram` | `force`, `dry_run`, `date` | Tuyển chọn 4 thương vụ Kim Cương đa ngành và bắn bản tin Telegram 06:30 sáng |
| **24** | `GET` | `/api/hs/catalog` | `mode` | Duyệt Đại Từ điển 97 Chương Mã HS WCO theo 4 chế độ trực quan |
| **25** | `GET` | `/api/hs/search` | `q` | Tìm kiếm thông minh chương HS và phân nhóm hàng hóa |
| **26** | `GET` | `/api/hs/summary` | Không | Thống kê tổng quan 97 chương HS, cụm ngành và tổng số sản phẩm |
| **27** | `GET` | `/api/hs/products` | `chapter`, `q`, `limit` | Truy vấn chi tiết 213 dòng sản phẩm xuất nhập khẩu thuộc các chương HS |
| **28** | `GET` | `/api/regulations/active` | `region`, `industry` | Danh sách các quy định pháp lý ngoại thương đang hiệu lực (EUDR, CBAM, UFLPA, GACC) |
| **29** | `GET` | `/api/regulations/horizon-calendar` | Không | Lịch trình Chân trời Chính sách cảnh báo sớm các mốc áp dụng luật mới |
| **30** | `GET` | `/api/regulations/detail` | `id` | Hồ sơ chi tiết quy định pháp lý, mã HS chịu tác động và bộ chứng từ tuân thủ |
| **31** | `POST` | `/api/regulations/notify-risk-alert` | `regulation_id`, `dry_run` | Phát bản tin cảnh báo khẩn cấp rủi ro pháp lý ngoại thương qua Telegram |
| **32** | `GET` | `/api/trade-tags/catalog` | `category` | Danh mục toàn bộ Thẻ Tag quy chuẩn kỹ thuật, chất lượng và thanh toán quốc tế |
| **33** | `GET` | `/api/trade-tags/explain` | `tag` | Giải nghĩa kỹ thuật chuyên sâu và khuyến nghị đàm phán cho từng Thẻ Tag |
| **34** | `GET` | `/api/prices/benchmarks` | `commodity`, `unit` | Cơ sở dữ liệu giá hàng hóa đa sàn quốc tế và quy đổi chuẩn hóa đơn vị đo lường |

---

# PHẦN IV. ĐỀ ÁN THƯƠNG MẠI HÓA ĐA PHƯƠNG

### 1. Phân khu Dành cho Sale Xuất khẩu của Nhà Cung Cấp (Supplier Sales Hub)
* Giá trị cốt lõi: Săn khách mua thực chiến theo mã HS, soi vận đơn B/L và đơn giá hải quan của đối thủ, lấy danh bạ VIP của Giám đốc thu mua, AI soạn thư chào hàng 5 thứ tiếng, và thẩm định tín nhiệm khách mua 4 tầng phòng chống lừa đảo.

### 2. Phân khu Dành cho Bộ phận Thu mua của Bên Mua (Buyer Procurement Hub)
* Giá trị cốt lõi: Tìm nhà máy sản xuất gốc và Đại lý Cấp 1 toàn cầu, sử dụng Bức tường lửa Thuế và Kiểm toán Xưởng thực địa SOP-02 để loại bỏ doanh nghiệp ma, đối soát giá chào với 6 sàn quốc tế và kiểm tra tuân thủ các rào cản EUDR, CBAM, GACC.

### 3. Phân khu Dành cho Đơn vị Xúc tiến Thương mại, Hiệp hội & Môi giới B2B (Trade Promotion & Broker Hub)
* Giá trị cốt lõi: Khớp lệnh tự động Ma trận 6 Chiều theo ngành, xuất Bộ Đôi RFQ giáp lưng có Chế độ Ẩn danh (Blind Mode) chống cắt cầu cho Broker, và cung cấp hệ thống Bot Telegram tự động phát bản tin tình báo thương hiệu riêng mỗi sáng cho hàng nghìn doanh nghiệp hội viên.

---

# PHẦN V. KIẾN TRÚC CHUYỂN ĐỔI SAAS & BẢO VỆ MÔI GIỚI

1. Bộ Chuyển đổi 4 Chế độ Vai trò (Role Switcher): Phân quyền tài khoản theo Tổng Hành Dinh, Sale Nhà Cung Cấp, Sale Bên Mua, và Xúc Tiến Thương Mại.
2. Ví Tín dụng Thông minh (Credit Metering): Miễn phí tra cứu cơ bản (Freemium), thu phí tín dụng khi mở khóa danh bạ VIP, xem chi tiết đơn giá vận đơn B/L, xuất báo cáo thẩm định A4 hoặc chạy phân tích khớp lệnh.
3. Chế độ Bảo vệ Môi giới (Blind Mode): Cho phép ẩn tên và thông tin liên hệ của đối tác trên báo cáo thẩm định và thư chào giá cho đến khi các bên ký thỏa thuận hoa hồng.
4. Bảo mật Bản quyền: Tự động đóng dấu mờ (Watermark) trên báo cáo xuất bản và giới hạn tần suất gọi API (Rate Limit).

---

# PHẦN VI. MÔ HÌNH DOANH THU & HIỆP LỰC TẬP ĐOÀN

### 1. Bảng Giá Thuê Bao Định Kỳ (SaaS Matrix)
* Gói 1 - Export/Sourcing Pro (Sale cá nhân): 1.990.000 VNĐ/tháng ($79/tháng) — 50 Credits/tháng, 10 lượt thẩm định 4 tầng.
* Gói 2 - Factory & Trading Team (Phòng XNK/Thu mua 5 người): 6.900.000 VNĐ/tháng ($279/tháng) — 300 Credits/tháng, 50 lượt thẩm định 4 tầng & xuất A4.
* Gói 3 - Trade Promotion & Broker Hub (Hiệp hội/Broker 20 người): 24.900.000 VNĐ/tháng ($999/tháng) — Toàn quyền Bàn Khớp Lệnh 6 Chiều, Bộ Đôi RFQ Ẩn danh, 1.500 Credits và Bot Telegram riêng.
* Gói 4 - Enterprise API & White-Label: Theo hợp đồng từ 60.000.000 VNĐ/tháng kết nối ERP/Core Banking.

### 2. Dịch vụ Giá trị Gia tăng & Hoa hồng Thành công
* Mua thêm Tín dụng lẻ: 50.000 VNĐ/Credit mở danh bạ; 250.000 VNĐ/Hồ sơ thẩm định A4.
* Dịch vụ Kiểm toán Nhà máy Thực địa (SOP-02): 12.000.000 – 25.000.000 VNĐ/ca kiểm toán.
* Hoa hồng Môi giới Khớp lệnh Thành công: Thu từ 0,5% – 2,0% giá trị hợp đồng đối với các thương vụ chốt qua Bàn Khớp Lệnh.

### 3. Hiệp lực Toàn Tập đoàn (Synergy)
* Hãng Luật Tập đoàn: Bán chéo hợp đồng ngoại thương, xử lý tranh chấp L/C và tư vấn EUDR/CBAM/GACC ngay trên nền tảng.
* Công ty Kế toán & Kiểm toán: Thực hiện kiểm toán nhà máy SOP-02 và dịch vụ hoàn thuế GTGT xuất khẩu.
* Công ty Digital Marketing: Triển khai chiến dịch tìm kiếm khách hàng B2B toàn cầu cho các nhà máy.
* Dự án Nông nghiệp: Ưu tiên bao tiêu và xuất khẩu các đơn hàng nông sản Kim Cương trên Bàn Khớp Lệnh.

---

# PHẦN VII. LỘ TRÌNH THỰC HIỆN 3 GIAI ĐOẠN

* Giai đoạn 1 (3–5 ngày): Tích hợp Bộ chuyển đổi 4 Vai trò, Chế độ Ẩn danh (Blind Mode) và hiển thị thanh Ví Tín dụng Demo trên giao diện.
* Giai đoạn 2 (1–2 tuần): Hoàn thiện hệ thống quản lý tài khoản Multi-Tenant, cổng thanh toán VietQR/Quốc tế và đóng dấu bản quyền.
* Giai đoạn 3 (Từ Tháng 1): Triển khai chiến dịch thu hút 500 doanh nghiệp dùng thử, ký kết hợp tác chiến lược với các Hiệp hội ngành hàng và kích hoạt bán chéo dịch vụ hệ sinh thái.

---
Kính trình Chủ tịch Tập đoàn xem xét và phê duyệt.
