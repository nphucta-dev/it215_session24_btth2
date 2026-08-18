# FlashMove RBAC + Multi-Origin CORS

## Mục tiêu

Bài thực hành hiện thực hóa:

- RBAC tập trung bằng Custom Middleware.
- Vai trò `DISPATCHER`, `DRIVER`, `CUSTOMER_SUPPORT`.
- Authorization dựa trên Header giả lập `X-Role-Identity`.
- CORS whitelist chính xác cho `https://driver.flashmove.io` và `https://hub.flashmove.io`.
- Chỉ cho phép `GET`, `POST`, `PATCH`.
- Chỉ cho phép `Content-Type`, `X-Role-Identity`.

## Quyền

| Endpoint | DISPATCHER | DRIVER | CUSTOMER_SUPPORT |
|---|---:|---:|---:|
| `POST /api/v1/orders/assign` | ✅ | ❌ | ❌ |
| `PATCH /api/v1/orders/status` | ✅ | ✅ | ❌ |
| `GET /api/v1/orders/track` | ✅ | ✅ | ✅ |

Role sai hoặc không có role sẽ nhận `403`:

```json
{
  "status": "Rejected",
  "reason": "Unauthorized action for this role"
}
```

## Cài đặt

```bash
python -m venv .venv
```

Windows:

```bash
.venv\\Scripts\\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Swagger: `http://127.0.0.1:8000/docs`

## Ví dụ

### Dispatcher gán đơn

```bash
curl -X POST http://127.0.0.1:8000/api/v1/orders/assign \
  -H "Content-Type: application/json" \
  -H "X-Role-Identity: DISPATCHER" \
  -d '{"order_id":"ORD-1001","driver_id":"DRV-001"}'
```

### Driver không thể gán đơn

```bash
curl -X POST http://127.0.0.1:8000/api/v1/orders/assign \
  -H "Content-Type: application/json" \
  -H "X-Role-Identity: DRIVER" \
  -d '{"order_id":"ORD-1001","driver_id":"DRV-001"}'
```

Sẽ nhận `403 Forbidden`.

## CORS

Allowlist:

- `https://driver.flashmove.io`
- `https://hub.flashmove.io`

Methods:

- `GET`
- `POST`
- `PATCH`

Headers:

- `Content-Type`
- `X-Role-Identity`

Không sử dụng `allow_origins=["*"]`.

## Chạy test

```bash
pytest -q
```

## Kiến trúc

```text
Browser / Driver App
        |
        v
CORS Middleware
        |
        v
Custom RBAC Middleware
        |
        +--> route + method -> required roles
        |
        +--> X-Role-Identity
        |
        +--> 403 nếu không đủ quyền
        |
        v
FastAPI Endpoint
        |
        v
Response
```

> Lưu ý: `X-Role-Identity` chỉ được dùng để giả lập dữ liệu User/Role theo đề bài. Trong production, client không được tự quyết định role. Cần dùng cơ chế Authentication (ví dụ JWT/session) rồi lấy role từ identity đã được xác thực.
