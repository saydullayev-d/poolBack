from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UsersResponse
from app.services.user import UsersService
from app.auth import Token, authenticate_user, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.models.user import User
from app.api.dependencies import get_users_service, get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UsersResponse)
async def create_user(user: UserCreate, service: UsersService = Depends(get_users_service)):
   return await service.create_user(user)
    

@router.get("/{user_id}", response_model=UsersResponse)
async def get_user_by_id(user_id: int, service: UsersService = Depends(get_users_service), current_user: User = Depends(get_current_user)):
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else: 
        return user
    
@router.get("/", response_model=list[UsersResponse])
async def list_users(service: UsersService = Depends(get_users_service), current_user: User = Depends(get_current_user)):
    return await service.get_users()

@router.put("/update/{user_id}", response_model=UsersResponse)
async def update_user(user_id: int, user: UserCreate, service: UsersService = Depends(get_users_service)):
    db_user = await service.update_user(user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}")
async def delete_user(user_id: int, service: UsersService = Depends(get_users_service), current_user: User = Depends(get_current_user)):
    try:
        result = await service.delete_user(user_id)
        if result:
            return {"message": f"Deleted user with ID {user_id}"}
        raise HTTPException(status_code=404, detail="Menu item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.name}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
