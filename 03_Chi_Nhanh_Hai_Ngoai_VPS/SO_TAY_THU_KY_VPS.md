# 📋 SỔ TAY THƯ KÝ CHI NHÁNH HẢI NGOẠI (VPS-01)
**Cập nhật lần cuối:** 15/10/2026 13:00  
**Thư ký trưởng AI:** Antigravity (Gemini 3.8 Flash High)

## 🏛️ CHỈ THỊ TỪ CHỦ TỊCH TẬP ĐOÀN
- [15/10/2026] Phê duyệt kế hoạch giao dịch XAU/USD `PLAN-1792040284` (SELL 4148.11).
- [15/10/2026] Kích hoạt chế độ Chat Tự Nhiên 100% không cần `/task`.
- [15/10/2026] Thiết lập cơ chế quét ngầm 60s bắt SL/TP không spam.
- [15/10/2026] Phê duyệt đề án thiết lập Chi nhánh Hải ngoại và kho tri thức Git `tapdoan`.
- [15/10/2026 13:05] Kho tri thuc Holding Vault da ket noi thanh cong den VPS-01.
- [15/10/2026 13:15] Chu tich phe duyet Kich hoat He Thong Don Tin Kinh Te 3 Moc (19h00 Trinh sat -> 19h15 Khoa phong thu -> 19h35 Bat song M5).
- [15/10/2026 13:22] Chu tich phe duyet Che Do Im Lang Tuyet Doi (Silent Guard): Chi thong bao khi Khop lenh, Cham SL, Dat TP, hoac cac moc Tin Do.
- [15/10/2026 13:38] Nâng cấp Typing Heartbeat: Duy trì trạng thái Thư ký đang soạn tin/làm việc liên tục khi Chủ tịch nhắn tin.
- [15/10/2026 13:40] Ban hành Chuẩn mực Báo cáo Cấp cao (Executive Briefing Protocol): Triệt tiêu văn phong kịch bản sân khấu, bỏ toàn bộ ngoặc đơn miêu tả hành động *(...)*, định dạng tóm tắt tinh gọn tối ưu cho Telegram di động.
- [15/10/2026 13:50] Cấm triệt để trích nguồn, link file (file://...) và tên file .md trong tin nhắn báo cáo Telegram gửi Chủ tịch.
- [15/10/2026 13:55] Chuẩn hóa danh xưng cơ quan thường trực: Đổi toàn bộ "Văn phòng Tổng Hành Dinh" thành "Văn phòng Thư ký Tập đoàn".
- [15/10/2026 14:00] Chính thức thành lập Khối Trading Agent độc lập tại `01_Cong_Ty_Thanh_Vien/trading_agent` và `Project/Trading Agent`.
- [15/10/2026 14:02] Giao Văn phòng Thư ký Tập đoàn độc quyền phụ trách soạn thảo & kiểm soát phát ngôn, thông báo, quyết định và tin nhắn Telegram điều hành; bắt buộc áp dụng kỹ năng `executive-admin-telegram-drafter` trước khi phát ngôn.
- [15/10/2026 14:24] Khắc phục triệt để lỗi hiển thị '**nội dung**' trên Telegram: Tích hợp bộ chuyển đổi Markdown sang Telegram HTML chuẩn (tự động chuyển **text** thành <b>text</b>, escape an toàn các ký tự đặc biệt & < >).








---

### [NHIỆM VỤ HOÀN TẤT - 2026-10-15 14:48:58] CƠ CHẾ TỰ ĐỘNG XÓA TIN NHẮN 24 GIỜ (AUTO-DELETE 24H)
* **Chỉ thị từ Chủ tịch:** Thiết lập chế độ tự động xóa tin nhắn sau 1 ngày (24 giờ).
* **Đơn vị thực thi:** Khối Trading Hải ngoại VPS-01 & Văn phòng Thư ký Tập đoàn.
* **Giải pháp kỹ thuật đã triển khai:**
  1. Xây dựng module `auto_delete.py` tích hợp cơ chế khóa tiến trình `fcntl.flock` chống xung đột đa tiến trình (PM2).
  2. Bổ sung cơ chế ghi nhận mốc thời gian (timestamp) tự động cho 100% tin nhắn đến và đi trong `telegram_bot_listener.py` và `trading_agent_core.py`.
  3. Thiết lập Background Worker Daemon quét định kỳ mỗi 60 giây, tự động kích hoạt API `deleteMessage` tiêu hủy các tin nhắn có thời gian lưu trữ từ 86.400 giây (24 giờ / 1 ngày).
  4. Bổ sung lệnh tra cứu điều hành `/autodelete` để theo dõi hàng đợi và thời điểm tiêu hủy kế tiếp.
* **Trạng thái:** HOÀN TẤT & ĐANG VẬN HÀNH 24/7 (Đã kiểm thử thực tế và xác nhận hoạt động chuẩn xác).
