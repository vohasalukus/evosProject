from fastapi import APIRouter

from app.evos.models import Category
from app.evos.schemas import SCategory, SRCategory
from app.exceptions import ObjectAlreadyExistsException
from app.repository.schemas import SBaseListResponse
from app.repository.tools import get_list_data

router = APIRouter(
    prefix="/category",
    tags=["Category"],
)

@router.post('/create',response_model=SRCategory)
async def add_category(category_data: SCategory):

    existing_category = await Category.find_one_or_none(Category.name == category_data.name)
    if existing_category:
        raise ObjectAlreadyExistsException

    category = await Category.create(name=category_data.name)
    return category


# @router.get("/")
# async def get_categories(page: int = 1, limit: int = 15):
#     return await get_list_data(
#         model=Category,
#         page=page,
#         limit=limit
#     )
