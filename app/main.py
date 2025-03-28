import logging

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routes.auth_router import auth_router
from app.database import Base, engine
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from app.middlewares.security_middleware import SecurityMiddleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up")
    Base.metadata.create_all(bind=engine)
    yield  # This pauses here until the app shuts down

    logger.info("Shutting down")

# Initialize FastAPI with the lifespan function
app = FastAPI(title="FastAPI Authentication", lifespan=lifespan)

# Include routes
app.include_router(auth_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Security Middleware
app.add_middleware(SecurityMiddleware)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI Authentication System",
        version="1.0.0",
        description="FastAPI Authentication System",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )