from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.utils import get_current_user 
from database.db import get_db
from auth.schemas import UserCreate, UserLogin, Token, UserResponse
from auth.service import create_user, login_user
from fastapi.security import OAuth2PasswordRequestForm
from auth.utils import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/protected")
def protected_route(current_user = Depends(get_current_user)):
    return {"message": f"Hello user {current_user.id}"}


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user.email, user.password)

    if not new_user:
        raise HTTPException(status_code=400, detail="Email already registred")
    return new_user

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):   
    return login_user(db, form_data.username, form_data.password)