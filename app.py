"""
Hugging Face Spaces entry point for Stock Analysis Application.
This file serves both the FastAPI backend and static frontend files.
"""
import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.main import app as backend_app

# Mount static files
backend_app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve index.html at root
@backend_app.get("/app")
async def serve_app():
    """Serve the main application page."""
    return FileResponse("frontend/index.html")

@backend_app.get("/dashboard")
async def serve_dashboard():
    """Serve the dashboard page."""
    return FileResponse("frontend/dashboard.html")

@backend_app.get("/portfolio")
async def serve_portfolio():
    """Serve the portfolio page."""
    return FileResponse("frontend/portfolio.html")

# Helper for uvicorn to find the app
app = backend_app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
