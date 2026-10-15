# 🧭 HƯỚNG DẪN VẬN HÀNH KHỐI TRADING AGENT (TRADINGAGENTS SYSTEM)
*Đơn vị quản lý: Khối Phân Tích & Giao Dịch Tài Chính — Trading Desk*  
*Thư mục Dự án:* `D:\project antigravity\Project\Trading Agent`

---

## 🏛️ 1. TỔNG QUAN HỆ THỐNG VÀ BỘ 4 CHUYÊN GIA (AGENTS)

Hệ thống kết hợp giữa **TradingAgents Multi-Agent Graph (TauricResearch v0.4.0)** và **Bộ 4 Kỹ năng Chuyên gia Antigravity**:

1. **`trading-analyst` (Chuyên gia Phân tích Toàn diện):**
   - Phân tích Kỹ thuật (SMC, Wyckoff, Price Action, RSI, MACD, Volume Profile).
   - Phân tích Dữ liệu Vĩ mô & Thị trường liên đới (DXY, US 10Y Yield, Lãi suất Fed, CPI, NFP).
   - Phân tích Tin tức và Tâm lý (Sentiment Flow).
2. **`trading-researcher` (Chuyên gia Tranh biện & Thẩm định):**
   - Tổ chức tranh luận đối kháng **Bull vs. Bear**.
   - Bóc tách điểm mù nhận thức và thiên kiến xác nhận (Confirmation Bias).
   - Stress-test các kịch bản bất lợi (Black Swan, Flash Crash).
3. **`trading-risk-manager` (Giám đốc Quản trị Rủi ro - CRO):**
   - Thực thi kỷ luật thép: Rủi ro tối đa 1-2% vốn tài khoản trên mỗi vị thế.
   - Bắt buộc Stop-Loss (SL) cứng, tỷ lệ R:R $\ge$ 1:2.
   - Tính toán Lot Size chính xác theo công thức quản trị vốn.
   - Khống chế Max Drawdown (giới hạn lỗ ngày -3%, tuần -6%).
4. **`trading-execution-trader` (Chuyên viên Khớp lệnh & Vận hành):**
   - Thực thi lệnh (Limit/Market), quản lý trailing stop bảo toàn lợi nhuận.
   - Ghi chép nhật ký giao dịch (Trade Journaling).
   - Vận hành Dashboard trực quan theo dõi lệnh theo thời gian thực.

---

## ⚡ 2. CÁC LỆNH VẬN HÀNH NHANH (QUICK START)

Mở terminal tại thư mục `D:\project antigravity\Project\Trading Agent`:

### A. Kiểm tra nhanh giá Vàng thế giới và các chỉ số vĩ mô (XAU/USD, DXY, Yield):
```powershell
.\.venv\Scripts\python.exe check_current_gold.py
```
*Kết quả trả về giá giao ngay (`GC=F`), quỹ GLD ETF, chỉ số sức mạnh USD (DXY) và Lợi suất Trái phiếu Mỹ 10 năm (`^TNX`).*

### B. Kiểm tra vi phạm Stop-Loss hoặc trạng thái vị thế:
```powershell
.\.venv\Scripts\python.exe check_sl_breach.py
```

### C. Khởi chạy Web Dashboard trực quan (Trading & Indicators Dashboard):
```powershell
.\.venv\Scripts\python.exe serve_dashboard.py
```
*Truy cập trình duyệt tại: `http://localhost:8000/gold_dashboard.html` hoặc `http://localhost:8000/dashboard.html` để xem biểu đồ và vị thế trực quan.*

### D. Chạy bộ phân tích Multi-Agent cho cổ phiếu hoặc tài sản tài chính:
```powershell
.\.venv\Scripts\python.exe main.py
```

---

## 🔑 3. CẤU HÌNH API KEYS (.ENV)

File cấu hình nằm tại: `D:\project antigravity\Project\Trading Agent\.env`.  
Hệ thống hỗ trợ đa dạng LLM provider:
- **Google Gemini:** `GOOGLE_API_KEY=AIza...` *(Khuyên dùng)*
- **OpenAI:** `OPENAI_API_KEY=sk-...`
- **Anthropic Claude:** `ANTHROPIC_API_KEY=sk-ant-...`
- **Dữ liệu Vĩ mô FRED:** `FRED_API_KEY=...` *(Miễn phí lấy tại stlouisfed.org)*

---

## 💬 4. MẪU CÂU LỆNH YÊU CẦU TRONG ANTIGRAVITY

Khi làm việc với trợ lý Antigravity, Chủ tịch có thể yêu cầu trực tiếp bằng tiếng Việt:

- **Phân tích Vàng hôm nay:**
  > *"Nhờ `trading-analyst` lấy dữ liệu Vàng mới nhất, kết hợp DXY và Trái phiếu 10 năm để đánh giá xu hướng ngắn hạn của XAU/USD."*
- **Tranh luận đa chiều trước khi vào lệnh:**
  > *"Tôi dự định mở vị thế Long cổ phiếu NVDA tại vùng giá này. Mời `trading-researcher` tổ chức màn phản biện Bull vs Bear xem điểm vào có an toàn không."*
- **Tính toán quản trị rủi ro:**
  > *"Tài khoản 10.000 USD, muốn vào lệnh Mua Vàng tại 4.170 USD, cắt lỗ 4.150 USD. Nhờ `trading-risk-manager` tính toán kích thước lot chuẩn theo quy tắc 1% vốn."*
