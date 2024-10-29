from fastapi import APIRouter, Depends
from app.evos.models import Category
from app.evos.schemas import SCategory, SRCategory
from app.exceptions import ObjectAlreadyExistsException, ModelNotFoundException
from app.repository.tools import get_list_data
from app.user.dependencies import get_current_user
from app.user.models import User

router = APIRouter(
    prefix="/category",
    tags=["Category"],
)


@router.post('/create', response_model=SRCategory)
async def add_category(category_data: SCategory, user: User = Depends(get_current_user)):

    existing_category = await Category.find_one_or_none(Category.name == category_data.name)
    if existing_category:
        raise ObjectAlreadyExistsException

    category = await Category.create(name=category_data.name)
    return category


@router.get("/")
async def get_categories(page: int = 1, limit: int = 15):
    return await get_list_data(
        model=Category,
        page=page,
        limit=limit
    )


@router.put('/{category_id}', response_model=SRCategory)
async def update_category(category_id: int, category_data: SCategory, user: User = Depends(get_current_user)):
    updated_category = await Category.update(category_id, name=category_data.name)
    if not updated_category:
        raise ModelNotFoundException
    return updated_category


@router.delete('/{category_id}')
async def delete_category(category_id: int, user: User = Depends(get_current_user)):
    await Category.delete(Category.id == category_id)
    return {
        "status": 200,
        "message": "Successfully deleted"
    }

