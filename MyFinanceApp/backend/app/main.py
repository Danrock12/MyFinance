from fastapi import FastAPI
from app.routes import accounts

app = FastAPI()

app.include_router(accounts.router, prefix="/accounts")

@app.get("/")
async def root():
    return {"message": "Hello from backend!"}

@app.get("/test-connection")
async def test_connection():
    return {"status": "Backend is reachable!"}
