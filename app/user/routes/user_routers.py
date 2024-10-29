from fastapi import APIRouter, Depends, Response, Form

from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPassword, ModelNotFoundException
from app.user.auth import get_hashed_password, create_access_token, authenticate_user
from app.user.dependencies import get_current_user
from app.user.models import User
from app.user.schemas import SUserRegister, SUserAuth, SRUser

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@router.post("/register")
async def register_user(user_data: SUserRegister, response: Response):
    """
    Поле name необязательно
    """
    existing_user = await User.find_one_or_none(User.email == user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_hashed_password(user_data.password)

    user_data_dict = user_data.dict(exclude_none=True, exclude={'password'})
    user_data_dict['hashed_password'] = hashed_password

    user = await User.create(**user_data_dict)

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return {
        "status": 201,
        "detail": "register is successful",
        'access_token': access_token,
        'user': {
            "id": user.id,
            "name": user.name if user.name else None,
            "email": user.email,
            "role": user.role
        }
    }


@router.post("/login")
async def login(response: Response, user_data: SUserAuth):
    """
    Вход пользователя по проверки email и password
    """
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPassword
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)

    return {
        "status": 200,
        "detail": "login is successful",
        'access_token': access_token,
        'data': {
            "id": user.id,
            "name": user.name if user.name else None,
            "email": user.email,
            "role": user.role
        }
    }


@router.post("/logout")
async def logout(response: Response):
    """
    Выход из аккаунта
    """
    response.delete_cookie("access_token")
    return {
        "status": 200,
        "detail": "logout is successful"
    }


@router.get("/current-user")
async def current_user(user: User = Depends(get_current_user)):
    """
    Получения текущего user; используется для проверки авторизованн ли пользователь или нет
    """
    return {
        "status": 200,
        "data": {
            "id": user.id,
            "name": user.name if user.name else None,
            "email": user.email,
            "role": user.role
        }
    }


@router.post('/change-password')
async def change_password(user: User = Depends(get_current_user), new_password: str = Form()):
    """
    Изменение пароля
    """
    hashed_password = get_hashed_password(new_password)
    await User.update(model_id=user.id, hashed_password=hashed_password)
    return {
        'status': 200,
        "detail": "password change is successful",
    }


@router.patch('/update')
async def update_user(
        name: str = None, email: str = None, role: str = None, user: User = Depends(get_current_user)):
    """
    Обновление информации пользователя; пароль не включен в этот запрос; обновление параметров опцианально
    """
    update_data = {}

    if name is not None:
        update_data['name'] = name
    if email is not None:
        update_data['email'] = email
    if role is not None:
        update_data['role'] = role

    if update_data:
        await User.update(model_id=user.id, **update_data)

    return {
        'status': 200,
        "detail": "changed user data",
    }


@router.delete("/delete")
async def delete_user(current_user: User = Depends(get_current_user)):
    """
    Автоматически удаляет текущего пользователя
    """
    await User.delete(User.id == current_user.id)
    return {
        "status": 200,
        "message": "Successfully deleted"
    }
