from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from ..model.user import User, Message
from ..schema.user import UserCreate, MessageCreate
from ..config import hash_password, verify_password
from sqlalchemy.exc import IntegrityError

def create_user(db: Session, user: UserCreate):
    try:
        hashed_password = hash_password(user.password)
        db_user = User(username=user.username, dob=user.dob, gender=user.gender, phone_no=user.phone_no, password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return JSONResponse(
            status_code=201,
            content={"status": "success", "message": "User created", "user_id": db_user.id, "username": db_user.usernamename },
        )
    except IntegrityError as e:
        db.rollback()
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": " User already exists or invalid data"},
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "An unexpected error occurred"},
        )


from fastapi import HTTPException

def authenticate_user(db: Session, phone_no: str, password: str)-> JSONResponse:
    user = db.query(User).filter(User.phone_no == phone_no).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")  # 404 Not Found

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")  # 401 Unauthorized

    return {"status": "success", "message": "Authentication successful", "user_id": user.id}  # 200 OK


def create_message(db: Session, message: MessageCreate):
    db_message = Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages(db: Session, user_id: int):
    return db.query(Message).filter(Message.user_id == user_id).all()
