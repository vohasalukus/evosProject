from fastapi import APIRouter
from app.evos.routes.category_routers import router as category_router
from app.evos.routes.dish_routers import router as dish_router

router = APIRouter(
    prefix="/evos"
)

router.include_router(category_router)
router.include_router(dish_router)