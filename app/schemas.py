from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: str = "True"

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
        
class Post(PostBase):
    id :int
    created_at :datetime
    owner:UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post:Post
    votes:int

class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(UserCreate):
    pass


class Token(BaseModel):
    access_token:str
    token_type:str

    class Config:
        orm_mode = True
    
class TokenData(BaseModel):
    id:Optional[str] = None

class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)