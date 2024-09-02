from typing import Annotated
from fastapi import APIRouter, Depends , HTTPException, status, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from ..models import Users
from ..database import engine,SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session , Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

class UserVarification(BaseModel):
    current_password : str
    new_password: str = Field(min_length=6)

@router.get('/',status_code=status.HTTP_200_OK)
async def user(user:user_dependency ,db: db_dependency):
    if user is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    return db.query(Users).filter(Users.id == user.get("id")).first()

# @router.get('/user', status_code=status.HTTP_200_OK)
# async def user(user: user_dependency, db: db_dependency):
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
#     user_record = db.query(Users).filter(Users.id == user.get("id")).first()
#     if user_record is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
#     return user_record

    

@router.put("/password",status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency , db:db_dependency ,user_varification: UserVarification):
    if user is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if not bcrypt_context.verify(user_varification.current_password,user_model.hashed_password):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Error on password change")
    user_model.hashed_password = bcrypt_context.hash(user_varification.new_password)
    db.add(user_model)
    db.commit()

@router.put('/phone_number/{phone_number}',status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db:db_dependency,phone_number:str):
    if user is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
