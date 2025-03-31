from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.config import RATE_LIMIT_MAX_REQUESTS, RATE_LIMIT_WINDOW_SECONDS
from app.database import get_db
from app.models import StatusUpdateRequest, GetStatusRequest, StatusResponse
from app.utils.authentication import authenticate
from app.utils.routes import atomic_checkout, atomic_release, get_files_status


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)  # Rate limiting
allowed_requests_per_second = RATE_LIMIT_MAX_REQUESTS/RATE_LIMIT_WINDOW_SECONDS


# 🔹 CHECKOUT FILES (Single & Multiple)
@router.post("/checkout",
             response_model=StatusResponse,
             dependencies=[Depends(limiter.limit(f"{allowed_requests_per_second}/second")),
                           Depends(authenticate)])
def checkout_files(request: StatusUpdateRequest, db: Session = Depends(get_db)):
    if not request.file_paths:
        raise HTTPException(status_code=400, detail="File paths cannot be empty")

    _ = atomic_checkout(db, request.file_paths, request.user_id)
    return get_files_status(db, request.file_paths)


# 🔹 GET STATUS (Single & Multiple)
@router.get("/status",
            response_model=StatusResponse,
            dependencies=[Depends(limiter.limit(f"{allowed_requests_per_second}/second")),
                          Depends(authenticate)])
def check_files_status(request: GetStatusRequest, db: Session = Depends(get_db)):
    return get_files_status(db, request.file_paths)


# 🔹 RELEASE FILES (Single & Multiple)
@router.delete("/release",
               dependencies=[Depends(limiter.limit(f"{allowed_requests_per_second}/second")),
                             Depends(authenticate)])
def release_files(request: StatusUpdateRequest, db: Session = Depends(get_db)):
    try:
        # Fetch all checkout statuses for the requested files
        statuses = get_files_status(db, request.file_paths)
        user_id = request.user_id

        # Check if the user owns all checkouts
        for file_path, status in statuses.items():
            if status["user_id"] != user_id:
                raise HTTPException(status_code=403, detail=f"Unauthorized release: {file_path} is checked out by another user.")

        # Execute the atomic release operation
        atomic_release(db, request.file_paths)
    except HTTPException as e:
        raise e  # Preserve detailed error messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Catch unexpected errors
