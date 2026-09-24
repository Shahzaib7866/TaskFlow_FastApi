
from typing import Optional
from sqlmodel import SQLModel, Field

# Database Table Configuration
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, nullable=False)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)

# API Request ke liye validation schema (Jab user register kare ga)
class UserCreate(SQLModel):
    username: str
    email: str
    password: str



