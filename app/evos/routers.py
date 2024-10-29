from fastapi import APIRouter
from app.evos.routes.category_routers import router as category_router

router = APIRouter(
    prefix="/evos"
)

router.include_router(category_router)
