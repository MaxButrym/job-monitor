from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database.db import get_db
from models.user import User
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = "supersecret"  # потом вынесем в env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    print("TOKEN:", token)  # 👈 ДОБАВЬ

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("PAYLOAD:", payload)  # 👈 ДОБАВЬ
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        print("JWT ERROR")  # 👈 ДОБАВЬ
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    print("USER:", user)  # 👈 ДОБАВЬ
    if user is None:
        raise credentials_exception

    return user