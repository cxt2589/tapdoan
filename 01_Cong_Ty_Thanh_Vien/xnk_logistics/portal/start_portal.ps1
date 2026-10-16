# Khởi chạy Cổng Trade Intelligence & Verification Portal (Phase 1)
# Khối Xuất Nhập Khẩu & Thương Mại Quốc Tế

$PORT = 8088
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "🚢 KHOI XUAT NHAP KHAU - TRADE INTELLIGENCE & VERIFICATION PORTAL" -ForegroundColor Green
Write-Host "📡 Khoi chay may chu tai: http://localhost:$PORT" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan

python server.py $PORT
