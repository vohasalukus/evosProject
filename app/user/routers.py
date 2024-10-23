from fastapi import APIRouter
from app.user.routes.user_routers import router as user_router


router = APIRouter(prefix="/app")

router.include_router(user_router)
