from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import  OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas, models, utils, OAuth2

router = APIRouter(
    prefix = "/login",
    tags = ['Auth']
)

@router.post("/", response_model = schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_FORBIDDEN, detail = "Credentials are incorrect")
    hashed_password = user.password
    if not utils.verify(user_credentials.password, hashed_password):
        raise HTTPException(status_code = status.HTTP_401_FORBIDDEN, detail = "Credentials are not correct")

    # create token and return with some data
    access_token = OAuth2.create_access_token(data = {"user_id":user.id})

    return {"access_token":access_token, "token_type" : 'bearer'}