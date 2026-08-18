# Hồ sơ sản phẩm FlashMove

## Nỗi đau

Driver có thể gọi trực tiếp endpoint nhạy cảm của Dispatcher; cấu hình CORS `*` làm tăng rủi ro cross-origin browser access.

## Nhóm người dùng

- DISPATCHER
- DRIVER
- CUSTOMER_SUPPORT

## Quy tắc nghiệp vụ

1. Dispatcher được phân bổ đơn.
2. Dispatcher và Driver được cập nhật trạng thái đơn.
3. Cả ba role được xem tracking.
4. Role không hợp lệ nhận 403.
5. CORS chỉ chấp nhận hai origin chính thức.
6. Chỉ GET/POST/PATCH và hai header được yêu cầu.
