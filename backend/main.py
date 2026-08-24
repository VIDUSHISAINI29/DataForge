
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware  # 1. Import the middleware
from src.routes.index import api_router

load_dotenv()

app = FastAPI()

# 2. Define your allowed origins (frontend URLs)
origins = os.getenv("FRONTEND_URL", "").split(",")

# 3. Add the CORS middleware configuration to your app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allows requests from these domains
    allow_credentials=True,           # Allows cookies / auth headers
    allow_methods=["*"],              # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],              # Allows all HTTP headers
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Windows 11!",
            "status": "OK!"}