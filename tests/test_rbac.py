from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_dispatcher_can_assign_order():
    response = client.post(
        "/api/v1/orders/assign",
        headers={"X-Role-Identity": "DISPATCHER"},
        json={"order_id": "ORD-1", "driver_id": "DRV-1"},
    )
    assert response.status_code == 200
    assert response.json()["role"] == "DISPATCHER"


def test_driver_cannot_assign_order():
    response = client.post(
        "/api/v1/orders/assign",
        headers={"X-Role-Identity": "DRIVER"},
        json={"order_id": "ORD-1", "driver_id": "DRV-1"},
    )
    assert response.status_code == 403
    assert response.json() == {
        "status": "Rejected",
        "reason": "Unauthorized action for this role",
    }


def test_driver_can_update_status():
    response = client.patch(
        "/api/v1/orders/status",
        headers={"X-Role-Identity": "DRIVER"},
        json={"order_id": "ORD-1", "status": "DELIVERED"},
    )
    assert response.status_code == 200


def test_customer_support_cannot_update_status():
    response = client.patch(
        "/api/v1/orders/status",
        headers={"X-Role-Identity": "CUSTOMER_SUPPORT"},
        json={"order_id": "ORD-1", "status": "DELIVERED"},
    )
    assert response.status_code == 403


def test_all_roles_can_track():
    for role in ("DISPATCHER", "DRIVER", "CUSTOMER_SUPPORT"):
        response = client.get(
            "/api/v1/orders/track",
            headers={"X-Role-Identity": role},
        )
        assert response.status_code == 200
        assert response.json()["role"] == role


def test_missing_role_is_rejected():
    response = client.get("/api/v1/orders/track")
    assert response.status_code == 403


def test_role_check_is_case_insensitive():
    response = client.get(
        "/api/v1/orders/track",
        headers={"X-Role-Identity": "driver"},
    )
    assert response.status_code == 200


def test_health_is_public():
    response = client.get("/health")
    assert response.status_code == 200


def test_allowed_origin_get():
    response = client.get(
        "/api/v1/orders/track",
        headers={
            "Origin": "https://driver.flashmove.io",
            "X-Role-Identity": "DRIVER",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "https://driver.flashmove.io"


def test_second_allowed_origin_post():
    response = client.options(
        "/api/v1/orders/assign",
        headers={
            "Origin": "https://hub.flashmove.io",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "X-Role-Identity,Content-Type",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "https://hub.flashmove.io"


def test_disallowed_origin_is_not_whitelisted():
    response = client.get(
        "/api/v1/orders/track",
        headers={
            "Origin": "https://evil.example",
            "X-Role-Identity": "DRIVER",
        },
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers


def test_cors_exposes_only_allowed_methods_on_preflight():
    response = client.options(
        "/api/v1/orders/status",
        headers={
            "Origin": "https://driver.flashmove.io",
            "Access-Control-Request-Method": "DELETE",
        },
    )
    assert response.status_code == 400
