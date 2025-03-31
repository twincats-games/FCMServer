from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import checkout_file, get_checkout_status, release_checkout
from app.utils.enums import CheckoutStatus

# 🔹 Utility: Perform Atomic Checkout
def atomic_checkout(db: Session, file_paths: List[str], user_id: int):
    results = {}

    for file_path in file_paths:
        status = get_checkout_status(db, file_path)
        if status and status.user_id != user_id:
            raise HTTPException(status_code=409, detail=f"File {file_path} is checked out by another user")

        results[file_path] = checkout_file(db, file_path, user_id)

    return results

# 🔹 Utility: Get Status for Multiple Files
def get_files_status(db: Session, file_paths: List[str]):
    file_statuses = {}

    for file_path in file_paths:
        status = get_checkout_status(db, file_path)
        file_statuses[file_path] = {
            "user_id": status.user_id if status else None,
            "status": CheckoutStatus.CHECKED_OUT.value if status else CheckoutStatus.AVAILABLE.value
        }

    return file_statuses

# 🔹 Utility: Atomic Release of Files
def atomic_release(db: Session, file_paths: List[str]):
    for file_path in file_paths:
        release_checkout(db, file_path)