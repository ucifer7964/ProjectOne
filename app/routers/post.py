from fastapi import FastAPI, HTTPException,status, Depends,Response, APIRouter
from .. import models, schemas, OAuth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import  List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)


@router.get("/", response_model = List[schemas.PostOut])
def post(db: Session = Depends(get_db), current_user:int = Depends(OAuth2.get_current_user), limit:int = 10, skip:int=0, search:Optional[str]=""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
                        models.Vote,models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(
                        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts
 
@router.post("/", response_model = schemas.Post)
def post(post: schemas.PostCreate,db: Session = Depends(get_db), current_user:int = Depends(OAuth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model = schemas.PostOut)
def get_post(id:int, db: Session = Depends(get_db), current_user:int = Depends(OAuth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
                        models.Vote,models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).first()
    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Resource not available")
    return post

@router.put("/update/{id}", response_model = schemas.Post)
def udpate_posts(id:int,post:schemas.PostBase, db:Session = Depends(get_db), current_user:int = Depends(OAuth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Resouce Not Found")
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, details = "Not Authorized for requested operation")
    post_query.update(post.dict(),synchronize_session = False)
    db.commit()
    return post_query.first()



@router.delete("/delete/{id}")
def delete_post(id:int, db: Session = Depends(get_db), current_user:int = Depends(OAuth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Resource not Found")
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not Authorized for requested operation")
    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)
