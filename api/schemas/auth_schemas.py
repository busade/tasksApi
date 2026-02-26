from pydantic import BaseModel, EmailStr, field_validator, model_validator,Field


def normalize_value(v):
    return v.lower() if isinstance(v, str) else v

class CleanBaseModel(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def strip_all_strings(cls, values):
        return {
            k: v.strip() if isinstance(v, str) else v
            for k, v in values.items()
        }


class UserCreate(CleanBaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128, description="User's password")
    confirm_password: str = Field(..., description="Password confirmation")

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, values):
        if values.data.get('password') and v != values.data['password']:
            raise ValueError('Passwords do not match')
        return v

     # Normalize role to lowercase
    @field_validator('role', mode='before')
    @classmethod
    def normalize_role(cls, v):
        return normalize_value(v)

class RegisterResponse(BaseModel):
    """Schema for successful registration response"""
    id: str
    email: str
    is_active: bool
    
  
class googleAuthRequest(BaseModel):
    id_token: str
