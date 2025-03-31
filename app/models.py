from typing import List, Dict

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from dataclasses import dataclass
from datetime import datetime, UTC

Base = declarative_base()

# File Checkout Model
class FileCheckout(Base):
    __tablename__ = "file_checkouts"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    checkout_time = Column(DateTime, default=datetime.now(UTC))


# File Checkout Data read from the Database
@dataclass
class FileCheckoutData:
    file_path: str
    user_id: int
    checkout_time: datetime


# Request Models
class StatusUpdateRequest(BaseModel):
    file_paths: List[str]  # Support multiple files
    user_id: int


class GetStatusRequest(BaseModel):
    file_paths: List[str] # Support multiple files


class StatusResponse(BaseModel):
    file_statuses: Dict[str, Dict[str, str]]  # File path → {user_id, status}
