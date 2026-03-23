from sqlalchemy.orm import Session
from models.user import User
from core.security import hash_password, verify_password
from auth.utils import create_access_token
from sqlalchemy.exc import IntegrityError

def create_user(db: Session, email: str, password: str):
    user = User(
        email=email,
        hashed_password=hash_password(password)
    )
    db.add(user)
    
    try:
        db.commit()
    except:
        db.rollback()
        return None
    
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)

    if not user:
        return None

    token = create_access_token({"sub": str(user.email)})

    return token
