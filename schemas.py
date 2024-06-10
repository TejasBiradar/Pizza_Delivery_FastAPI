from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
    username : str
    email : str
    password : str
    is_staff : Optional[bool] = False
    is_active : Optional[bool] = False

    class Config:
        from_attributes = True
        
class SignUpModelRes(SignUpModel):
    id : int
    class Config:
        from_attributes = True

class Settings(BaseModel):
    authjwt_secret_key : str = "e3680d851c29291e2aa3199dd5d7d46da6176c01a980c23c3547c923c9759956"


class LoginModel(BaseModel):
    username : str
    password : str

    class Config:
        form_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username : str
    class Config:
        from_attributes = True


class OrderModel(BaseModel):
    quantity : int 
    order_status : Optional[str] = "PENDING"
    pizza_size : Optional[str] = "SMALL"


    class Config:
        form_attributes = True
        
class OrderModelUpdate(BaseModel):
    order_status : Optional[str] = "PENDING"

    class Config:
        form_attributes = True    
