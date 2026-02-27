import bcrypt, os, jwt
import random
from typing import Optional

from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from google.oauth2 import id_token
from google.auth.transport import requests

from api.model.user_model import User, VerificationToken, PasswordReset
from api.schemas.auth_schemas import UserCreate, RegisterResponse, googleAuthRequest, loginRequest, TokenResponse, PasswordResetRequest, PasswordResetVerify
from api.utils import success_response,fail_response,auth_response,send_otp_email,send_password_reset_email

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
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30))
            )
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGORITHM"))
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_MINUTES", 60))
            )
        
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGORITHM"))
        return encoded_jwt
    

    @staticmethod
    def register_user(db: Session, user_request: UserCreate):
        existing_user = db.query(User).filter(User.email== user_request.email).first()
        if existing_user:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail =  "Email already exists, please use a different email"
            )
        otp_code = AuthService.generate_otp()

        send_otp_email(user_request.email, otp_code)    
        
        hashed_password= AuthService.hash_password(user_request.password)

        new_user=User(

            email = user_request.email,
            password = hashed_password,
            is_verified = False,
            is_google_user = False
        )
        print(new_user)
        db.add(new_user)
        db.commit()

        
        verification = VerificationToken(
            user_id=new_user.id,
            otp=str(otp_code),
            expires_at=datetime.utcnow() + timedelta(minutes=10),
        )
        db.add(verification)
        db.commit()
        db.refresh(new_user)
        

        return success_response(
            status_code=status.HTTP_201_CREATED,
            message="User registered successfully. Please verify your email.",
            data={"email": new_user.email}
        )
    @staticmethod
    def verify_email(db: Session, email: str, otp: str):

        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        token = db.query(VerificationToken).filter(
            VerificationToken.user_id == user.id,
            VerificationToken.otp == otp,
        ).first()

        if not token:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        if token.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="OTP expired")

        user.is_verified = True

        db.commit()

        return success_response(
            status_code=status.HTTP_200_OK,
            message="Email verified successfully"
        )
    
    @staticmethod
    def google_auth(db: Session, request: googleAuthRequest):

        try:
            idinfo = id_token.verify_oauth2_token(
                request.id_token,
                requests.Request(),
                os.getenv("GOOGLE_CLIENT_ID")
            )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Google token"
            )

        email = idinfo["email"]
        google_id = idinfo["sub"]

        user = db.query(User).filter(User.email == email).first()

        if not user:
            user = User(
                email=email,
                google_id=google_id,
                is_google_account=True,
                is_verified=True  
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        
        else:
            if not user.google_id:
                user.google_id = google_id
                user.is_google_account = True
                db.commit()

        token = auth_response(user)

        return token
    
    @staticmethod
    def login_user(db: Session, login_request: loginRequest):

        email = login_request.email
        password = login_request.password

        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=404, detail="Invalid credentials")

        if not AuthService.verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not user.is_verified:
            raise HTTPException(
                status_code=403,
                detail="Please verify your email before logging in"
            )
        
        access_token = AuthService.create_access_token({"sub": user.email})
        refresh_token = AuthService.create_refresh_token({"sub": user.email})

       
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    def request_password_reset(db: Session, email: str):
        """Request password reset by sending an OTP to the user's email"""
        print('request_password_reset called with email:', email)  # Debug statement
        user = db.query(User).filter(User.email == email).first()

        if not user:
            return success_response(
                status_code=status.HTTP_200_OK,
                message="If the email exists, a password reset OTP has been sent"
            )

        db.query(PasswordReset).filter(
            PasswordReset.user_id == user.id,
            PasswordReset.is_used == False
        ).update({"is_used": True})
        db.commit()

        otp_code = AuthService.generate_otp()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

        password_reset = PasswordReset(
            user_id=user.id,
            otp=str(otp_code),
            expires_at=expires_at
        )
        db.add(password_reset)
        db.commit()

        # Send OTP via email
        send_password_reset_email(email, otp_code)

        return success_response(
            status_code=status.HTTP_200_OK,
            message="If the email exists, a password reset OTP has been sent"
        )

    @staticmethod
    def reset_password(db: Session, reset_request: PasswordResetVerify):
        """Reset password using OTP"""
        user = db.query(User).filter(User.email == reset_request.email).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Find the OTP record
        otp_record = db.query(PasswordReset).filter(
            PasswordReset.user_id == user.id,
            PasswordReset.otp == reset_request.otp,
            PasswordReset.is_used == False
        ).first()

        if not otp_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP"
            )

        # Check expiration
        if otp_record.expires_at < datetime.now(timezone.utc):
            otp_record.is_used = True
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP has expired"
            )

        # Update password
        hashed_password = AuthService.hash_password(reset_request.new_password)
        user.password = hashed_password

        # Mark OTP as used
        otp_record.is_used = True

        db.commit()

        return success_response(
            status_code=status.HTTP_200_OK,
            message="Password reset successfully. You can now login with your new password"
        )

    @staticmethod
    def verify_reset_token(db: Session, email: str, otp: str) -> dict:
        """Verify whether provided OTP for password reset is valid"""
        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        record = db.query(PasswordReset).filter(
            PasswordReset.user_id == user.id,
            PasswordReset.otp == otp,
            PasswordReset.is_used == False
        ).first()

        if not record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP"
            )

        if record.expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP has expired"
            )

        return {"valid": True, "email": user.email}