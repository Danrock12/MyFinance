from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import accounts, transactions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])

@app.get("/")
async def root():
    return {"message": "Hello from backend!"}

@app.get("/test-connection")
async def test_connection():
    return {"status": "Backend is reachable!"}

