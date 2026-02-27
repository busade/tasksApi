from api.services.auth_service import AuthService
from api.utils import auth_response, fail_response, success_response
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.config.config import get_db
from api.schemas.auth_schemas import googleAuthRequest, UserCreate, RegisterResponse, loginRequest, PasswordResetRequest, PasswordResetVerify

router = APIRouter(prefix="/auth", tags=["Authentication"])
@router.post("/register", summary="User Registration")
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Handles user registration with email and password.
    Validates input, checks for existing users, and creates a new account.
    Returns a success message upon successful registration.
    """
    try:
        result = AuthService.register_user(db, user)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("/verify-email", summary="Email Verification")
def verify_email(email: str, otp: int, db: Session = Depends(get_db)):
    """
    Handles email verification using OTP.
    Validates the OTP and marks the user's email as verified.
    Returns a success message upon successful verification.
    """
    try:
        result = AuthService.verify_email(db, email, otp)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/google", summary="Google Sign-In/Sign-Up")
def google_auth(request: googleAuthRequest, db: Session = Depends(get_db)):
    """
    Handles Google Sign-In and Sign-Up.
    If the user doesn't exist, it creates a new account.
    If the user exists but doesn't have a Google ID, it links the account.
    Returns JWT tokens upon successful authentication.
    """
    try:
        token = AuthService.google_auth(request.token, db)
        return token
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("/login", summary="Email/Password Login")
def login(login_request: loginRequest, db: Session = Depends(get_db)):
    """
    Handles user login with email and password.
    Verifies credentials and returns JWT tokens upon successful authentication.
    """
    try:
        token = AuthService.login_user(db, login_request)
        return token
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/password-reset/request", summary="Request Password Reset")
def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """
    Initiates password reset process by sending a one-time OTP to the user's email.
    Response is intentionally vague for security.
    """
    print('hello')
    try:
        result = AuthService.request_password_reset(db, request.email)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/password-reset/verify", summary="Verify OTP and Reset Password")
def verify_reset_token(reset_request: PasswordResetVerify, db: Session = Depends(get_db)):
    """
    Verifies the OTP and resets the password.
    Requires email, OTP code, and new password.
    """
    try:
        result = AuthService.reset_password(db, reset_request)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/password-reset/check", summary="Check OTP Validity")
def check_reset_token(email: str, otp: str, db: Session = Depends(get_db)):
    """
    Checks if an OTP is valid without resetting the password.
    Useful for frontend validation.
    """
    try:
        result = AuthService.verify_reset_token(db, email, otp)
        return success_response(
            status_code=status.HTTP_200_OK,
            message="OTP is valid",
            data=result
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))