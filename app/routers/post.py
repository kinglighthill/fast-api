from typing import Optional
from fastapi import Response, status, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.post("", response_model=schemas.PostResponse)
def create_post(res: Response, payload: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = models.Post(owner_id=current_user.id, **payload.dict())
    db.add(post)
    db.commit()
    db.refresh(post)

    return utils.get_response(res, "post created successfully", status.HTTP_201_CREATED, post)


# , response_model=schemas.PostLikeResponseList
@router.get("")
def get_posts(res: Response, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(posts)
    return utils.get_response(res, "posts retrieved successfully", status.HTTP_200_OK, posts)



@router.get("/{id}")
def get_post(res: Response, id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    # response: schemas.PostResponse = schemas.PostResponse()
    # print("Post: ", response)

    if not post: 
        return utils.get_response(res, f"post with id: {id} was not found", status.HTTP_404_NOT_FOUND, None) 

    return utils.get_response(res,"post retrieved successfully", status.HTTP_200_OK, post.Post)



@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(res: Response, id: int, payload: schemas.PostUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post: 
        return utils.get_response(res, f"post with id: {id} was not found", status.HTTP_404_NOT_FOUND, None) 

    if post.owner_id != current_user.id:
        return utils.get_response(res, "not authorized", status.HTTP_403_FORBIDDEN, None)

    post_query.update(payload.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)

    return utils.get_response(res, "post updated successfully", status.HTTP_205_RESET_CONTENT, post)


# , response_model=schemas.PostResponse
@router.delete("/{id}")
def delete_post(res: Response, id: int,  db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        return utils.get_response(res, f"post with id: {id} does not exist", status.HTTP_404_NOT_FOUND, None)
    
    if post.owner_id != current_user.id:
        return utils.get_response(res, "not authorized", status.HTTP_403_FORBIDDEN, None)

    post_query.delete(synchronize_session='fetch')
    db.commit()

    return utils.get_response(res, "post deleted successfully", status.HTTP_204_NO_CONTENT, post)

