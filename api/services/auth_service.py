from passlib.contxt import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import random
from api.models import User
from api.schemas.auth_schemas import UserCreate, RegisterResponse, googleAuthRequest
from api.utils import success_response,fail_response,auth_response

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)




class AuthService:

    @staticmethod
    def hash_password(password: str) -> str:
       """Hash password using bcrypt"""
       salt = bcrypt.gensalt()
       hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
       return hashed.decode('utf-8')
    @staticmethod
    def generate_otp()-> int:
        """generate a 4 digits one time password"""
        return random.randint(1000,9999)
    

    @staticmethod
    def register_user(db: Session, user_request: UserCreate):
        existing_user = db.query(User).filter(User.email== user_request.email).first()
        if existing_user:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail =  "Email already exists, please use a different email"
            )
        
        hashed_password= AuthService.hash_password(user_request.password)
        new_user=User(
            email = user_request.email,
            password = hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    