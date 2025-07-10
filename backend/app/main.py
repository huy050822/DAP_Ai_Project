from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import asyncio
from .routers import forecast
from .services.mongodb import MongoDBService
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="DAP AI Project API")

# Initialize MongoDB service
mongodb_service = MongoDBService()

# Dependency to get MongoDB service
def get_mongodb():
    return mongodb_service

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the absolute path to the frontend directory
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))

# Verify frontend directory exists
if not os.path.exists(frontend_dir):
    raise Exception(f"Frontend directory not found: {frontend_dir}")

# Include routers
app.include_router(
    forecast.router,
    prefix="/api/forecast",
    tags=["forecast"]
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": str(exc.detail)}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": str(exc)}
    )

# Mount static files with verified paths
try:
    # First mount the src directory for css/js/images
    src_path = os.path.join(frontend_dir, "src")
    if os.path.exists(src_path):
        app.mount("/src", StaticFiles(directory=src_path), name="static")
    else:
        print(f"Warning: src directory not found at {src_path}")

    # Then mount the root for HTML files
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
except Exception as e:
    print(f"Error mounting static files: {str(e)}")
    raise

@app.on_event("startup")
async def startup_event():
    # Tự động load dữ liệu từ CSV vào MongoDB nếu collection orders trống
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data_augmented.csv"))
    await mongodb_service.init_data(csv_path)