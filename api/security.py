from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from api.config.config import get_db
from api.model.user_model import User
import jwt
import os
from datetime import datetime, timezone

# OAuth2 scheme for Swagger UI
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/auth/login",
    scheme_name="JWT",
    description="Enter your JWT access token"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> dict:
    """
    Dependency to extract and verify JWT token from Authorization header.
    This will be used for all protected endpoints.
    Works with Swagger UI authorization.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(
            token,
            os.getenv("JWT_SECRET_KEY"),
            algorithms=[os.getenv("JWT_ALGORITHM", "HS256")]
        )
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if email is None:
            raise credentials_exception
        
        # Ensure it's an access token
        if token_type != "access":
            raise credentials_exception
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception
    
    # Get user from database
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise credentials_exception
    
    return {"id": user.id, "email": user.email}
