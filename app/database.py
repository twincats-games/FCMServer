from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL
from app.models import FileCheckout, FileCheckoutData

Base = declarative_base()

# Database Connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def checkout_file(db: Session, file_path: str, user_id: int) -> FileCheckoutData:
    """Checks out a file for a user."""
    new_checkout = FileCheckout(file_path=file_path, user_id=user_id)
    db.add(new_checkout)
    db.commit()
    db.refresh(new_checkout)
    return FileCheckoutData(
        file_path=new_checkout.file_path,
        user_id=new_checkout.user_id,
        checkout_time=new_checkout.checkout_time
    )

def get_checkout_status(db: Session, file_path: str) -> FileCheckoutData | None:
    """Fetches checkout status of a file."""
    checkout = db.query(FileCheckout).filter(file_path=file_path).first()
    if checkout:
        return FileCheckoutData(
            file_path=checkout.file_path,
            user_id=checkout.user_id,
            checkout_time=checkout.checkout_time
        )
    return None

def release_checkout(db: Session, file_path: str) -> bool:
    """Releases a file checkout."""
    checkout = db.query(FileCheckout).filter(file_path=file_path).first()
    if checkout:
        db.delete(checkout)
        db.commit()
        return True
    return False

