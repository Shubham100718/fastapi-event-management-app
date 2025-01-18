from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import User
from app.schemas.auth_schema import UserRegisterSchema, UserLoginSchema
from app.utils.auth_utils import create_access_token


auth_router = APIRouter()

@auth_router.post("/signup")
async def signup(user_data: UserRegisterSchema, 
                db: AsyncSession = Depends(get_db)
    ):
    result = await db.execute(select(User).filter(User.email==user_data.email))
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="User already exists"
        )
    new_user = User(email=user_data.email)
    new_user.set_password(user_data.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {
        "status_code": status.HTTP_201_CREATED, 
        "message": "User created successfully"
    }

@auth_router.post("/login")
async def login(user_data: UserLoginSchema, 
                db: AsyncSession = Depends(get_db)
    ):
    result = await db.execute(select(User).filter(User.email==user_data.email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found"
        )
    if not user.check_password(user_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid password"
        )
    access_token = create_access_token({"user_id": user.id})
    return {
        "status_code": status.HTTP_200_OK, 
        "message": "User logged in successfully",
        'access_token' : access_token
    }

