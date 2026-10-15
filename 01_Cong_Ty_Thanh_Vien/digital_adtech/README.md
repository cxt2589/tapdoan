# 🏢 Agency Agent Hub (AdTech & Digital Marketing)

> **Tổng hành dinh Multi-Agent AI cho Công ty AdTech & Digital Marketing**  
> Dựa trên hệ sinh thái mã nguồn mở `msitarzewski/agency-agents`, tối ưu hóa đặc biệt cho Antigravity.

---

## 📂 Cấu trúc Thư mục Dự án

```text
D:\project antigravity\Agency Agent\
├── .agents/
│   └── skills/                       # 283 Agent Skills đã chuyển đổi cho Antigravity
│       ├── agency-paid-media-ppc-campaign-strategist/
│       ├── agency-tracking-measurement-specialist/
│       ├── agency-brand-guardian/
│       ├── agency-frontend-developer/
│       ├── agency-bookkeeper-controller/
│       └── ... (toàn bộ 280+ agents)
├── strategy/                         # Runbooks & Playbooks điều phối chiến lược (NEXUS)
│   ├── runbooks.json                 # Kịch bản mẫu (startup-mvp, marketing-campaign, ...)
│   ├── runbooks/                     # Quy trình từng bước chi tiết
│   └── EXECUTIVE-BRIEF.md            # Nguyên tắc điều phối tránh đứt gãy handoff
├── examples/                         # Ví dụ quy trình làm việc mẫu
├── AGENTS.md                         # Chỉ dẫn vận hành phòng ban cho Antigravity
└── README.md                         # Tài liệu hướng dẫn sử dụng dự án
```

---

## 🚀 Hướng Dẫn Sử Dụng Nhanh

### 1. Kích hoạt trong Antigravity
1. Mở Antigravity.
2. Mở thư mục dự án: `D:\project antigravity\Agency Agent`.
3. Bắt đầu trò chuyện! Antigravity sẽ tự động nhận diện tất cả 280+ Agent Skills trong `.agents/skills/`.

### 2. Ví dụ Prompt theo từng Tình huống

#### 🎯 Tình huống 1: Khách hàng yêu cầu Tăng Chuyển Đổi (Performance)
```text
Khách hàng là thương hiệu thời trang local brand muốn đẩy mạnh doanh số tháng tới. 
Hãy đóng vai:
1. agency-growth-hacker: Phân tích phễu và chọn kênh ra đơn tối ưu (Meta Ads vs TikTok Ads vs Google).
2. agency-offer-lead-gen-strategist: Thiết kế gói ưu đãi chuyển đổi cao (Flash Sale / Combo).
3. agency-ppc-campaign-strategist & agency-paid-social-strategist: Lên kế hoạch ngân sách và cấu trúc chiến dịch.
4. agency-reality-checker: Thẩm định xem mục tiêu ROAS 5.0 có khả thi không và rủi ro ở đâu.
```

#### 👑 Tình huống 2: Khách hàng yêu cầu Làm Thương Hiệu (Branding)
```text
Một công ty B2B SaaS về quản trị nhân sự muốn làm chiến dịch nhận diện thương hiệu quý này.
Hãy đóng vai:
1. agency-brand-guardian: Xác lập thông điệp cốt lõi và Tone of Voice.
2. agency-visual-storyteller: Xây dựng kịch bản câu chuyện thương hiệu và định hướng hình ảnh.
3. agency-pr-communications-manager: Lập danh sách góc độ báo chí (PR angles) và bài thought leadership cho CEO.
4. agency-programmatic-display-buyer: Lên kế hoạch phủ sóng video/banner trên LinkedIn và GDN.
```

#### 💻 Tình huống 3: Kỹ thuật Web, HTML & Tracking Script
```text
Chúng ta cần triển khai Landing Page cho sự kiện ra mắt.
Hãy đóng vai:
1. agency-ui-designer: Đề xuất cấu trúc wireframe và thành phần giao diện.
2. agency-frontend-developer: Viết mã nguồn HTML/CSS responsive chuẩn tối ưu tải trang.
3. agency-tracking-measurement-specialist: Soạn thảo mã Custom JavaScript để bắt sự kiện click CTA và đẩy vào dataLayer cho GTM.
```

#### 📒 Tình huống 4: Đối Soát Kế Toán
```text
Hãy đóng vai agency-bookkeeper-controller và agency-accounts-payable-agent:
Dưới đây là chi phí tiêu hao tháng qua trên Google Ads ($12,500) và Meta Ads ($8,400) cho dự án Client X. 
Hợp đồng tạm ứng ban đầu là $20,000. Hãy lập bảng đối soát chi phí, số tiền cần truy thu thêm và tính toán biên lợi nhuận phí quản lý 15%.
```

---

## ⏰ Cài đặt Lịch Tự Động Hóa (Automation)

Bạn có thể gõ `/automation` trong Antigravity để lên lịch chạy ngầm cho các Agent:
* **8:00 AM hàng ngày:** `agency-search-query-analyst` quét báo cáo tìm kiếm và cập nhật Negative Keywords.
* **17:00 PM thứ Sáu:** `agency-bookkeeper-controller` tổng hợp đối soát ngân sách quảng cáo tuần.
