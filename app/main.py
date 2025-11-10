"""
Hello World API - FastAPI Application
A simple REST API demonstrating CI/CD pipeline with security scanning
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import os
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="Hello World API",
    description="A simple API demonstrating CI/CD best practices",
    version="1.0.0",
)


# Pydantic models for request/response validation
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    environment: str
    version: str


class HelloResponse(BaseModel):
    message: str
    timestamp: str


class GreetingRequest(BaseModel):
    name: str


class GreetingResponse(BaseModel):
    greeting: str
    timestamp: str


# Root endpoint
@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint returning welcome message"""
    return {
        "message": "Welcome to Hello World API",
        "docs": "/docs",
        "health": "/health",
    }


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint for monitoring"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        environment=os.getenv("ENVIRONMENT", "development"),
        version="1.0.0",
    )


# Simple hello endpoint
@app.get("/hello", response_model=HelloResponse)
async def hello() -> HelloResponse:
    """Simple hello world endpoint"""
    return HelloResponse(
        message="Hello, World!", timestamp=datetime.utcnow().isoformat()
    )


# Personalized greeting endpoint
@app.post("/greet", response_model=GreetingResponse)
async def greet(request: GreetingRequest) -> GreetingResponse:
    """Personalized greeting endpoint"""
    if not request.name or not request.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    return GreetingResponse(
        greeting=f"Hello, {request.name}!", timestamp=datetime.utcnow().isoformat()
    )


# Info endpoint
@app.get("/info")
async def info() -> Dict[str, any]:
    """Application information endpoint"""
    return {
        "name": "Hello World API",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Root endpoint"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/hello", "method": "GET", "description": "Simple hello"},
            {
                "path": "/greet",
                "method": "POST",
                "description": "Personalized greeting",
            },
            {"path": "/info", "method": "GET", "description": "API information"},
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
