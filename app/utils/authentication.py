from fastapi.security import APIKeyHeader
from fastapi import Security, HTTPException

from app.config import SECRET_KEY

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def authenticate(api_key: str = Security(api_key_header)):
    if api_key != SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
