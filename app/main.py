from fastapi import FastAPI, Depends, HTTPException
from .dependencies import get_db
from sqlalchemy.orm import Session
from .crud.user import create_user, create_message, get_messages, authenticate_user
from .schema.user import UserCreate, MessageCreate, UserLogin
from .database import Base, engine


app = FastAPI()


# Create Tables
Base.metadata.create_all(bind=engine)

# API Endpoints
@app.post("/signup/")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Tables
Base.metadata.create_all(bind=engine)

@app.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    authenticated_user = authenticate_user(db, user.phone_no, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": authenticated_user.id}

@app.post("/messages/")
def create_message_endpoint(message: MessageCreate, db: Session = Depends(get_db)):
    return create_message(db, message)

@app.get("/messages/{user_id}")
def get_messages_endpoint(user_id: int, db: Session = Depends(get_db)):
    return get_messages(db, user_id)
