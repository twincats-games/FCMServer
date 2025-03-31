from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import API_PREFIX, ALLOWED_HOSTS
from app.routes import router
from app.database import engine
from app.models import Base
from app.utils.log import logger

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization"],
)

Base.metadata.create_all(bind=engine)

# 🔹 Register Routes
app.include_router(router, prefix=API_PREFIX)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logger.info(f"{request.method} {request.url} - {response.status_code}")
    return response

@app.get("/")
def home():
    logger.info("Home endpoint accessed")
    return {"message": "File Checkout Manager API is running!"}
