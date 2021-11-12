from fastapi import Response
from passlib.context import CryptContext

def get_response(res: Response, msg: str, code: int, data: any):  
    res.status_code = code
    return {
            "message": msg,
            "status_code": str(code),
            "data": data
           }
def get_error(msg: str, code: int, data: any):  
    return {
            "message": msg,
            "status_code": str(code),
            "data": data
           }

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)