from datetime import datetime
from pydantic import BaseModel
from pydantic.networks import EmailStr
from typing import List, Optional


class Response(BaseModel):
    message: str
    status_code: str

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponseData(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserResponse(Response):
   data: Optional[UserResponseData]

class UserResponseList(Response):
   data: Optional[List[UserResponseData]]

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    pass

class PostResponseData(PostBase):
    id: int
    owner_id: str
    created_at: datetime
    published: bool
    owner: UserResponseData
    # likes: int

    class Config:
        orm_mode = True

class PostLikeResponseData(PostBase):
    Post: PostResponseData
    likes: int

    class Config:
        orm_mode = True

class PostResponse(Response):
   data: Optional[PostResponseData]

class PostResponseList(Response):
   data: Optional[List[PostResponseData]]

class PostLikeResponse(Response):
   data: Optional[PostLikeResponseData]

class PostLikeResponseList(Response):
   data: Optional[List[PostLikeResponseData]]

# class UserLoginResponseData():
#     email: EmailStr
#     password: str

# class UserLoginResponse(Response):
#     data: Optional[UserLoginResponseData]

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id: Optional[str]

class TokenResponse(Response):
   data: Optional[Token]

class Like(BaseModel):
    post_id: int
    like: bool

    class Config:
        orm_mode = True