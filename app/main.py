from fastapi import FastAPI
from app.user.routers import router as user_router
from app.evos.routers import router as evos_router

app = FastAPI()

app.include_router(user_router)
app.include_router(evos_router)