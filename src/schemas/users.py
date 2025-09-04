from pydantic import BaseModel, EmailStr, constr


class UserReqAdd(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str

class User(BaseModel):
    id: int
    email: EmailStr

class UserLogin(UserReqAdd):
    password: str

class UserOut(User):
    id: int
    email: str