from sqlmodel import SQLModel, create_engine, Session
from pydantic_settings import BaseSettings

# 1. Environment Settings Schema definition
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"
        extra = "ignore"

# Settings ka instance create karein jo baqi files mein use hoga
settings = Settings()

# 2. Database Engine create karein dynamic URL k sath
engine = create_engine(settings.DATABASE_URL, echo=True)

# Tables banane ka function
def init_db():
    SQLModel.metadata.create_all(engine)

# Database Session local scope (FastAPI Dependency)
def get_session():
    with Session(engine) as session:
        yield session
