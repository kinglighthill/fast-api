from fastapi import Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, utils

from app.database import get_db
from app.oauth2 import get_current_user
from app.schemas import Like

router = APIRouter(
    prefix='/like',
    tags=['Like']
) 

@router.post("/")
def like(res: Response, payload: Like, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == payload.post_id).first()

    if not post:
        return utils.get_response(res, f"post with id {payload.post_id} does not exist", status.HTTP_404_NOT_FOUND, None)
    
    like_query = db.query(models.Like).filter(models.Like.post_id == payload.post_id, models.Like.user_id == current_user.id)
    like = like_query.first()
    
    if payload.like:
        if like:
            return utils.get_response(res, f"user with id {current_user.id} has already voted on post with id {like.post_id}", status.HTTP_409_CONFLICT, None)
        
        new_like = models.Like(post_id = payload.post_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
        
        return utils.get_response(res, "successfully liked post", status.HTTP_201_CREATED, None)

    else:
        if not like:
            return utils.get_response(res, "like does not exist", status.HTTP_404_NOT_FOUND, None)
        
        like_query.delete(synchronize_session=False)
        db.commit()

        return utils.get_response(res, "successfully unliked post", status.HTTP_201_CREATED, None)