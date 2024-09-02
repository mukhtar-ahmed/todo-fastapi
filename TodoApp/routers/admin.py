from typing import Annotated
from fastapi import APIRouter, Depends , HTTPException, status, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from ..models import Todos
from ..database import engine,SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=['admin']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session , Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/todos",status_code=status.HTTP_200_OK)
async def all_todos(user: user_dependency , db: db_dependency):
    if user is None or user.get("role") != 'admin':
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    return db.query(Todos).all()

@router.delete("/todos/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todos(user:user_dependency, db:db_dependency, todo_id:int= Path(gt=0)):
    if user is None or user.get("role") != 'admin':
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    deleted_todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if deleted_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()

