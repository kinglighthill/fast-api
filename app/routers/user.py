from fastapi import Response, status, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("", response_model=schemas.UserResponse)
def create_user(res: Response, payload: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(payload.password)
    payload.password = hashed_password

    user = models.User(**payload.dict())
    db.add(user)
    db.commit()
    db.refresh(user)

    return utils.get_response(res, "user created successfully", status.HTTP_201_CREATED, user)

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(res: Response, id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        return utils.get_response(res, f"user with id: {id} was not found", status.HTTP_200_OK, None)

    return utils.get_response(res, "user retrieved successfully", status.HTTP_200_OK, user)
