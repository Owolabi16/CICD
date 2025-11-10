"""
Unit Tests for Hello World API
Using pytest and FastAPI TestClient
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
import json


# Create test client
client = TestClient(app)


class TestRootEndpoint:
    """Test cases for root endpoint"""
    
    def test_root_returns_200(self):
        """Test root endpoint returns 200 OK"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_returns_json(self):
        """Test root endpoint returns JSON"""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"
    
    def test_root_contains_message(self):
        """Test root endpoint contains welcome message"""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert "Welcome" in data["message"]
    
    def test_root_contains_docs_link(self):
        """Test root endpoint contains docs link"""
        response = client.get("/")
        data = response.json()
        assert "docs" in data


class TestHealthEndpoint:
    """Test cases for health check endpoint"""
    
    def test_health_returns_200(self):
        """Test health endpoint returns 200 OK"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_returns_healthy_status(self):
        """Test health endpoint returns healthy status"""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_health_contains_timestamp(self):
        """Test health endpoint contains timestamp"""
        response = client.get("/health")
        data = response.json()
        assert "timestamp" in data
        assert data["timestamp"] is not None
    
    def test_health_contains_environment(self):
        """Test health endpoint contains environment"""
        response = client.get("/health")
        data = response.json()
        assert "environment" in data
    
    def test_health_contains_version(self):
        """Test health endpoint contains version"""
        response = client.get("/health")
        data = response.json()
        assert "version" in data
        assert data["version"] == "1.0.0"


class TestHelloEndpoint:
    """Test cases for hello endpoint"""
    
    def test_hello_returns_200(self):
        """Test hello endpoint returns 200 OK"""
        response = client.get("/hello")
        assert response.status_code == 200
    
    def test_hello_returns_message(self):
        """Test hello endpoint returns hello message"""
        response = client.get("/hello")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello, World!"
    
    def test_hello_contains_timestamp(self):
        """Test hello endpoint contains timestamp"""
        response = client.get("/hello")
        data = response.json()
        assert "timestamp" in data


class TestGreetEndpoint:
    """Test cases for greet endpoint"""
    
    def test_greet_returns_200_with_valid_name(self):
        """Test greet endpoint returns 200 with valid name"""
        response = client.post(
            "/greet",
            json={"name": "Alice"}
        )
        assert response.status_code == 200
    
    def test_greet_returns_personalized_greeting(self):
        """Test greet endpoint returns personalized greeting"""
        response = client.post(
            "/greet",
            json={"name": "Alice"}
        )
        data = response.json()
        assert data["greeting"] == "Hello, Alice!"
    
    def test_greet_handles_different_names(self):
        """Test greet endpoint handles different names"""
        names = ["Bob", "Charlie", "Diana"]
        for name in names:
            response = client.post(
                "/greet",
                json={"name": name}
            )
            data = response.json()
            assert data["greeting"] == f"Hello, {name}!"
    
    def test_greet_returns_400_for_empty_name(self):
        """Test greet endpoint returns 400 for empty name"""
        response = client.post(
            "/greet",
            json={"name": ""}
        )
        assert response.status_code == 400
    
    def test_greet_returns_400_for_whitespace_name(self):
        """Test greet endpoint returns 400 for whitespace name"""
        response = client.post(
            "/greet",
            json={"name": "   "}
        )
        assert response.status_code == 400
    
    def test_greet_returns_422_for_missing_name(self):
        """Test greet endpoint returns 422 for missing name field"""
        response = client.post(
            "/greet",
            json={}
        )
        assert response.status_code == 422
    
    def test_greet_contains_timestamp(self):
        """Test greet endpoint contains timestamp"""
        response = client.post(
            "/greet",
            json={"name": "Test"}
        )
        data = response.json()
        assert "timestamp" in data


class TestInfoEndpoint:
    """Test cases for info endpoint"""
    
    def test_info_returns_200(self):
        """Test info endpoint returns 200 OK"""
        response = client.get("/info")
        assert response.status_code == 200
    
    def test_info_contains_name(self):
        """Test info endpoint contains application name"""
        response = client.get("/info")
        data = response.json()
        assert "name" in data
    
    def test_info_contains_version(self):
        """Test info endpoint contains version"""
        response = client.get("/info")
        data = response.json()
        assert "version" in data
    
    def test_info_contains_endpoints(self):
        """Test info endpoint contains endpoints list"""
        response = client.get("/info")
        data = response.json()
        assert "endpoints" in data
        assert isinstance(data["endpoints"], list)
        assert len(data["endpoints"]) > 0


class TestAPIDocumentation:
    """Test cases for API documentation"""
    
    def test_openapi_json_accessible(self):
        """Test OpenAPI JSON is accessible"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
    
    def test_docs_accessible(self):
        """Test Swagger docs are accessible"""
        response = client.get("/docs")
        assert response.status_code == 200


class TestErrorHandling:
    """Test cases for error handling"""
    
    def test_404_for_nonexistent_endpoint(self):
        """Test 404 is returned for non-existent endpoints"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_405_for_wrong_method(self):
        """Test 405 is returned for wrong HTTP method"""
        response = client.post("/hello")
        assert response.status_code == 405


# Fixtures for test data
@pytest.fixture
def sample_names():
    """Fixture providing sample names for testing"""
    return ["Alice", "Bob", "Charlie", "Diana", "Eve"]


@pytest.fixture
def invalid_names():
    """Fixture providing invalid names for testing"""
    return ["", "   ", "\t", "\n"]


# Parametrized tests
@pytest.mark.parametrize("name", ["Alice", "Bob", "Charlie"])
def test_greet_with_multiple_names(name):
    """Parametrized test for multiple names"""
    response = client.post("/greet", json={"name": name})
    assert response.status_code == 200
    assert response.json()["greeting"] == f"Hello, {name}!"


@pytest.mark.parametrize("invalid_name", ["", "   ", "\t"])
def test_greet_with_invalid_names(invalid_name):
    """Parametrized test for invalid names"""
    response = client.post("/greet", json={"name": invalid_name})
    assert response.status_code == 400
