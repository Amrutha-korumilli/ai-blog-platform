from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.hash import bcrypt
from flask import request
import os
from .models import User, db

# Load secret key from .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Register a new user
def register_user(username, password):
    if User.query.filter_by(username=username).first():
        raise Exception("Username already taken")

    hashed_pw = bcrypt.hash(password)
    user = User(username=username)
    db.session.add(user)
    db.session.commit()

    return user

# Log in and return JWT
def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise Exception("Invalid username or password")

    # For now, password checking is skipped because we didn't store it
    # You can enhance this once you add a `password_hash` column

    token_data = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Decode the JWT from the request
def get_current_user():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header")

    token = auth_header.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        return User.query.get(user_id)
    except JWTError:
        raise Exception("Invalid or expired token")
