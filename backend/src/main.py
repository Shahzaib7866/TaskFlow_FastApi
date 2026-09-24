from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.core.database import init_db
# Naya path jahan se router import ho raha hai:
from src.crud.user_crud import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db() # App start hote hi database tables banenge
    yield

app = FastAPI(
    title="FastAPI SQLModel Combined Auth System",
    version="1.0.0",
    lifespan=lifespan
)

# Combined router ko include karein
app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "status": "backend is running",
        "database": "connected via SQLModel"
    }
