from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import timedelta
from typing import Optional

# Core aur Model imports
from src.core.database import get_session, settings  # <-- settings yahan import kiya
from src.core.security import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from src.models.user import User, UserCreate

# Router definition
router = APIRouter(prefix="/auth", tags=["Authentication"])

# ==========================================
# 🛠️ DATABASE HELPER FUNCTIONS (CRUD)
# ==========================================
def get_user_by_email(session: Session, email: str) -> Optional[User]:
    return session.exec(select(User).where(User.email == email)).first()

def get_user_by_username(session: Session, username: str) -> Optional[User]:
    return session.exec(select(User).where(User.username == username)).first()

def create_user(session: Session, user_data: UserCreate) -> User:
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# ==========================================
# 🚀 API ENDPOINTS (ROUTES)
# ==========================================

# 1. Signup / Register Route
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    if get_user_by_email(session, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if get_user_by_username(session, user_data.username):
        raise HTTPException(status_code=400, detail="Username already taken")
        
    return create_user(session, user_data)

# 2. Login / Token Route
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = get_user_by_username(session, form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
        
    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # <-- Yahan hardcoded key ki jagah dynamic settings.SECRET_KEY pass ki hai:
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

