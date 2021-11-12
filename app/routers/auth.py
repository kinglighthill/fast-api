from fastapi import Response, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.TokenResponse)
def login(res: Response, payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.username).first()

    if not user:
        return utils.get_response(res, "Invalid Credentials", status.HTTP_403_FORBIDDEN, None)

    if not utils.verify(payload.password, user.password):
        return utils.get_response(res, "Invalid Credentials", status.HTTP_403_FORBIDDEN, None)

    access_token = oauth2.create_access_token(payload= {"user_id": user.id})
    data = {"access_token": access_token, "token_type": "bearer"}

    return utils.get_response(res, "login successful", status.HTTP_200_OK, data)
