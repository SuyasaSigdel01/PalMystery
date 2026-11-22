from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import Base, User, engine, get_db

SECRET_KEY = "dev-secret-change-me"
ALGORITHM = "HS256"
TOKEN_HOURS = 24

Base.metadata.create_all(bind=engine)

app = FastAPI()


class Credentials(BaseModel):
    email: str
    password: str


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def make_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_HOURS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/signup")
def signup(creds: Credentials, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == creds.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=creds.email, password_hash=hash_password(creds.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"token": make_token(user.id)}


@app.post("/login")
def login(creds: Credentials, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == creds.email).first()
    if not user or not check_password(creds.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Wrong email or password")

    return {"token": make_token(user.id)}