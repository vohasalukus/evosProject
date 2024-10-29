from fastapi import APIRouter, Depends

from app.evos.models import Dish
from app.evos.schemas import SRDish, SDish, SUDish
from app.exceptions import ObjectAlreadyExistsException, ModelNotFoundException
from app.repository.tools import get_list_data
from app.user.dependencies import get_current_user
from app.user.models import User

router = APIRouter(
    prefix="/dish",
    tags=["Dish"],
)


@router.post('/create', response_model=SRDish)
async def create_dish(
        dish_data: SDish,
        user: User = Depends(get_current_user),
):
    existing_dish = await Dish.find_one_or_none(Dish.name == dish_data.name)
    if existing_dish:
        raise ObjectAlreadyExistsException

    dish_data_dict = dish_data.dict(exclude_none=True)
    dish = await Dish.create(**dish_data_dict)
    return dish


@router.get('/')
async def get_dishes(page: int = 1, limit: int = 15):
    return await get_list_data(
        model=Dish,
        page=page,
        limit=limit,
    )


@router.patch('/{dish_id}', response_model=SRDish)
async def update_dish(
        dish_id: int,
        dish_data: SUDish,
        user: User = Depends(get_current_user)
):

    dish_data_dict = dish_data.dict(exclude_none=True)
    dish = await Dish.update(dish_id, **dish_data_dict)
    return dish


@router.delete('/{dish_id}')
async def delete_dish(
        dish_id: int,
        user: User = Depends(get_current_user)
):
    await Dish.delete(Dish.id == dish_id)
    return {
        "status": 200,
        "message": "Successfully deleted"
    }
