# API Test Cases

## Authorization

| # | Request | Role | Expected |
|---|---|---|---|
| 1 | POST `/api/v1/orders/assign` | DISPATCHER | 200 |
| 2 | POST `/api/v1/orders/assign` | DRIVER | 403 |
| 3 | POST `/api/v1/orders/assign` | CUSTOMER_SUPPORT | 403 |
| 4 | PATCH `/api/v1/orders/status` | DISPATCHER | 200 |
| 5 | PATCH `/api/v1/orders/status` | DRIVER | 200 |
| 6 | PATCH `/api/v1/orders/status` | CUSTOMER_SUPPORT | 403 |
| 7 | GET `/api/v1/orders/track` | DISPATCHER | 200 |
| 8 | GET `/api/v1/orders/track` | DRIVER | 200 |
| 9 | GET `/api/v1/orders/track` | CUSTOMER_SUPPORT | 200 |
| 10 | GET `/api/v1/orders/track` | Missing | 403 |

## CORS

| Origin | Expected |
|---|---|
| `https://driver.flashmove.io` | Allowed |
| `https://hub.flashmove.io` | Allowed |
| `https://evil.example` | Not whitelisted |
| `http://localhost:3000` | Not whitelisted |
