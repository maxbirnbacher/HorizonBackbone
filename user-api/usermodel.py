from pydantic import BaseModel
from typing import Optional
import passlib.hash
from jose import jwt
from datetime import datetime, timedelta
import os

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class UserHashedPassword(BaseModel):
    username: str
    hashedPassword: str

class UserBase(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserInDB(UserBase):
    username: str
    hashed_password: str

    def verify_password(self, plain_password):
        return passlib.hash.bcrypt.verify(plain_password, self.hashed_password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    print(f"JWT_SECRET_KEY: {JWT_SECRET_KEY}")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, str(JWT_SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt