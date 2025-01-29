from sqlalchemy.orm import Session
from ..model.user import User, Message
from ..schema.user import UserCreate, MessageCreate
from ..config import hash_password, verify_password

def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, dob=user.dob, gender=user.gender, phone_no=user.phone_no, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, phone_no: str, password: str):
    user = db.query(User).filter(User.phone_no == phone_no).first()
    if user and verify_password(password, user.password_hash):
        return user
    return None

def create_message(db: Session, message: MessageCreate):
    db_message = Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages(db: Session, user_id: int):
    return db.query(Message).filter(Message.user_id == user_id).all()
