from fastapi import FastAPI, HTTPException,status, Depends,Response, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import  List

router = APIRouter(
    prefix = "/users",
    tags = ['Users']
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):

    user_password = utils.hash(user.password)
    user.password = user_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model = schemas.UserOut)
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Resource Not Found")
    return user