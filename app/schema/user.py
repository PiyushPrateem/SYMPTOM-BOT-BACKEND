from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    dob: str
    gender: str
    phone_no: str

class MessageCreate(BaseModel):
    user_id: int
    message: str
    is_bot: bool = False

class UserLogin(BaseModel):
    phone_no: str
    password: str