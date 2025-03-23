from fastapi import FastAPI
from app.routes.auth_router import router as auth_router
from app.routes.user_router import router as user_router
from app.database import Base, engine

app = FastAPI(title="FastAPI Authentication System")

# Create tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI Authentication System!"}
