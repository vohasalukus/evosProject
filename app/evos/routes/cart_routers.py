from fastapi import APIRouter, Depends

from app.evos.models import Cart, Dish
from app.evos.schemas import SCart
from app.user.dependencies import get_current_user
from app.user.models import User

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


@router.post('/create', response_model=SCart)
async def create_cart(
        user: User = Depends(get_current_user)
):
    cart = await Cart.first_or_create(Cart.user_id == user.id, user_id=user.id, includes=['dishes'])
    return cart


@router.get('/')
async def get_cart(user: User = Depends(get_current_user)):
    cart = await Cart.find_one_or_fail(Cart.user_id == user.id, includes=['dishes'])
    total_quantity = len(cart.dishes)
    return SCart(
        id=cart.id,
        dishes=[dish.id for dish in cart.dishes],
        total_quantity=total_quantity if total_quantity else None
    )


@router.delete('/')
async def delete_cart(
        user: User = Depends(get_current_user)
):
    await Cart.delete(Cart.user_id == user.id)
    return {
        "status": 200,
        "message": "Successfully deleted"
    }


@router.post('/add_dish/{dish_id}', response_model=SCart)
async def add_dish_to_cart(dish_id: int, user: User = Depends(get_current_user)):
    # Используем методы репозитория для работы в контексте одной сессии
    cart = await Cart.find_one_or_fail(Cart.user_id == user.id, includes=["dishes"])
    dish = await Dish.find_one_or_fail(Dish.id == dish_id)

    # Обновляем список блюд в корзине и сохраняем изменения
    updated_dishes = cart.dishes + [dish]
    await Cart.update(cart.id, dishes=updated_dishes)

    # Возвращаем обновленную корзину
    updated_cart = await Cart.find_one_or_fail(Cart.user_id == user.id, includes=["dishes"])
    return updated_cart


@router.delete('/remove_dish/{dish_id}', response_model=SCart)
async def remove_dish_from_cart(dish_id: int, user: User = Depends(get_current_user)):
    cart = await Cart.find_one_or_fail(Cart.user_id == user.id, includes=["dishes"])
    dish_to_remove = next((dish for dish in cart.dishes if dish.id == dish_id), None)
    if dish_to_remove:
        cart.dishes.remove(dish_to_remove)
    await Cart.update(cart.id, dishes=cart.dishes, includes=["dishes"])
    return cart
