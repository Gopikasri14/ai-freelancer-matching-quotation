from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Verify GET /api/v1/health returns 200 OK and expected JSON structure."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "ai-freelancer-system"
    assert "version" in data
    assert "environment" in data


def test_root_endpoint(client: TestClient):
    """Verify GET / returns 200 OK and discovery links."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["docs"] == "/docs"
    assert data["health"] == "/api/v1/health"


def test_swagger_docs_accessible(client: TestClient):
    """Verify /docs returns 200 OK."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema(client: TestClient):
    """Verify /openapi.json returns valid OpenAPI specification."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "/api/v1/health" in schema["paths"]
