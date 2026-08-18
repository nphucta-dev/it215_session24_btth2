from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from middleware.rbac_middleware import RBACMiddleware

app = FastAPI(title="FlashMove Delivery API", version="1.0.0")

# Exact multi-origin whitelist required by the assignment.
ALLOWED_ORIGINS = [
    "https://driver.flashmove.io",
    "https://hub.flashmove.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Content-Type", "X-Role-Identity"],
    allow_credentials=False,
)

# Centralized RBAC middleware.
app.add_middleware(RBACMiddleware)


class AssignOrderRequest(BaseModel):
    order_id: str
    driver_id: str


class OrderStatusRequest(BaseModel):
    order_id: str
    status: str


@app.post("/api/v1/orders/assign")
async def assign_order(payload: AssignOrderRequest, request: Request):
    return {
        "message": "Order assigned successfully",
        "order_id": payload.order_id,
        "driver_id": payload.driver_id,
        "role": request.state.role,
    }


@app.patch("/api/v1/orders/status")
async def update_order_status(payload: OrderStatusRequest, request: Request):
    return {
        "message": "Order status updated successfully",
        "order_id": payload.order_id,
        "status": payload.status,
        "role": request.state.role,
    }


@app.get("/api/v1/orders/track")
async def track_order(request: Request):
    return {
        "message": "Order tracking information",
        "order_id": "ORD-1001",
        "status": "OUT_FOR_DELIVERY",
        "role": request.state.role,
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
