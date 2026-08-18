from dataclasses import dataclass
from typing import Callable

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


@dataclass(frozen=True)
class RoutePolicy:
    methods: frozenset[str]
    roles: frozenset[str]


class RBACMiddleware(BaseHTTPMiddleware):
    """Centralized role-based access control for the assignment's dynamic API routes.

    The route policies are keyed by normalized HTTP method + path. This keeps all
    authorization decisions in one place rather than duplicating role checks in
    individual endpoint functions.
    """

    POLICIES: dict[tuple[str, str], RoutePolicy] = {
        ("POST", "/api/v1/orders/assign"): RoutePolicy(
            methods=frozenset({"POST"}),
            roles=frozenset({"DISPATCHER"}),
        ),
        ("PATCH", "/api/v1/orders/status"): RoutePolicy(
            methods=frozenset({"PATCH"}),
            roles=frozenset({"DISPATCHER", "DRIVER"}),
        ),
        ("GET", "/api/v1/orders/track"): RoutePolicy(
            methods=frozenset({"GET"}),
            roles=frozenset({"DISPATCHER", "DRIVER", "CUSTOMER_SUPPORT"}),
        ),
    }

    REJECTION = {
        "status": "Rejected",
        "reason": "Unauthorized action for this role",
    }

    async def dispatch(self, request: Request, call_next: Callable):
        # CORS preflight must be allowed to reach CORSMiddleware; preflight
        # requests do not carry the application role header in normal browser use.
        if request.method == "OPTIONS":
            return await call_next(request)

        policy = self.POLICIES.get((request.method, request.url.path))

        # Unprotected endpoints (e.g. /health) are allowed through.
        if policy is None:
            return await call_next(request)

        role = request.headers.get("X-Role-Identity", "").strip().upper()

        if role not in policy.roles:
            return JSONResponse(status_code=403, content=self.REJECTION)

        request.state.role = role
        return await call_next(request)
