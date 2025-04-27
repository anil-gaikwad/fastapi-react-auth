import logging
import os
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from backend.routes.auth_router import auth_router
from backend.database import Base, engine
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from backend.middlewares.security_middleware import SecurityMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get allowed origins from environment variable or use default
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Starting up application")
        Base.metadata.create_all(bind=engine)
        yield
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    finally:
        logger.info("Shutting down application")

# Initialize FastAPI with the lifespan function
app = FastAPI(
    title="FastAPI Authentication",
    description="A secure authentication system built with FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception handler caught: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred"}
    )

# Include routes
app.include_router(auth_router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Add Security Middleware
app.add_middleware(SecurityMiddleware)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI Authentication System",
        version="1.0.0",
        description="""
        FastAPI Authentication System with the following features:
        - User registration and login
        - JWT token authentication
        - Email verification
        - Password reset functionality
        - Secure session management
        """,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    Returns a simple status message.
    """
    return {"status": "ok", "service": "FastAPI Authentication"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )