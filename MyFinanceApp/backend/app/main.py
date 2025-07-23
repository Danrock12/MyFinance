from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import accounts
from app.models import Base
from app.db import engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accounts.router, prefix="/accounts")

@app.on_event("startup")
def on_startup():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello from backend!"}

@app.get("/test-connection")
async def test_connection():
    return {"status": "Backend is reachable!"}

