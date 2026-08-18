# Kiến trúc FlashMove

## 1. Authentication vs Authorization

Bài này tập trung vào Authorization. `X-Role-Identity` được xem là identity giả lập để mô phỏng role.

- Authentication: xác định ai đang gọi API.
- Authorization: xác định role đó được phép làm gì.

Production cần JWT/session; không tin trực tiếp role do client tự gửi.

## 2. RBAC tập trung

`RBACMiddleware` giữ một bảng policy:

```text
(method, path) -> set(roles)
```

Ví dụ:

```text
POST /api/v1/orders/assign
    -> DISPATCHER

PATCH /api/v1/orders/status
    -> DISPATCHER, DRIVER

GET /api/v1/orders/track
    -> DISPATCHER, DRIVER, CUSTOMER_SUPPORT
```

Điều này tránh việc lặp lại các đoạn `if role == ...` ở từng endpoint.

## 3. Dynamic Routes

Đường dẫn API được kiểm tra tập trung qua `request.method` và `request.url.path`, nên có thể mở rộng sang các route dynamic như:

```text
/api/v1/orders/{order_id}/status
```

bằng cách bổ sung cơ chế pattern matching hoặc route-policy registry.

## 4. CORS

CORS chỉ cho phép chính xác hai origin chính thức của doanh nghiệp. Browser sẽ không cho một trang có origin ngoài allowlist đọc response CORS.

CORS không thay thế RBAC. Hai lớp bảo vệ có mục đích khác nhau:

- CORS: kiểm soát browser cross-origin access.
- RBAC: kiểm soát quyền ở phía server.
