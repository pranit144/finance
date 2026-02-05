from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .core.database import init_supabase, engine, Base
from .routers import auth, stocks, portfolio
from .models import user, portfolio as portfolio_model
import os
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("api")

app = FastAPI(
    title="Stock Analysis API",
    description="Real-time stock market data and analysis API",
    version="1.0.0"
)

# Request Timing Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    # Log less for health check to reduce noise
    is_health = request.url.path.endswith("/health")
    
    if not is_health:
        logger.info(f"➡️ Request Details: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        if not is_health or response.status_code != 200:
            logger.info(f"⬅️ Response Details: {response.status_code} (took {process_time:.4f}s)")
            
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"❌ Request Failed: {e} (took {process_time:.4f}s)")
        raise

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and Create Tables if not exist."""
    print("🔄 Initializing Database...")
    
    # 1. Supabase Client (if used)
    init_supabase()
    
    # 2. SQLAlchemy (SQLite/Postgres) - Create Tables
    try:
        print("🔨 Creating database tables...")
        # This will create tables for all models registered with Base (User, Portfolio)
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        # Don't crash if it fails (e.g. read-only fs + sqlite), but log it
        print(f"❌ Error creating tables: {e}")
    
    print("✅ App Startup Complete")

# Include routers
app.include_router(auth.router)
app.include_router(stocks.router)
app.include_router(portfolio.router)

# Mount frontend files (Adjust path relative to backend/app/main.py)
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))

if os.path.exists(frontend_path):
    # Mount specific assets explicitly to match HTML relative paths
    js_path = os.path.join(frontend_path, "js")
    css_path = os.path.join(frontend_path, "css")
    
    if os.path.exists(js_path):
        app.mount("/js", StaticFiles(directory=js_path), name="js")
    if os.path.exists(css_path):
        app.mount("/css", StaticFiles(directory=css_path), name="css")

    # Serve HTML pages explicitly
    @app.get("/")
    async def read_root():
        return FileResponse(os.path.join(frontend_path, "index.html"))

    @app.get("/index.html")
    async def read_index():
        return FileResponse(os.path.join(frontend_path, "index.html"))

    @app.get("/login.html")
    async def read_login():
        return FileResponse(os.path.join(frontend_path, "index.html"))

    @app.get("/dashboard.html")
    async def read_dashboard():
        return FileResponse(os.path.join(frontend_path, "dashboard.html"))

    @app.get("/portfolio.html")
    async def read_portfolio():
        return FileResponse(os.path.join(frontend_path, "portfolio.html"))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "api": "operational",
        "database": "supabase"
    }
