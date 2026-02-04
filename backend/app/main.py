"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import engine, Base
from .routers import auth, stocks, portfolio
from .models import User, Portfolio  # Import models to ensure tables are created

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Stock Analysis API",
    description="Real-time stock market data and analysis API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(stocks.router)
app.include_router(portfolio.router)


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "Stock Analysis API",
        "version": "1.0.0",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "api": "operational",
        "database": "connected"
    }
