from pydantic import BaseModel, EmailStr, field_validator, model_validator, Field, ValidationInfo


def normalize_value(v):
    return v.lower() if isinstance(v, str) else v


class CleanBaseModel(BaseModel):

    @model_validator(mode="before")
    @classmethod
    def strip_all_strings(cls, values):
        if not isinstance(values, dict):
            return values
        return {
            k: v.strip() if isinstance(v, str) else v
            for k, v in values.items()
        }


class UserCreate(CleanBaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str

    @model_validator(mode="after")
    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class RegisterResponse(BaseModel):
    id: str
    email: str
    is_active: bool


class googleAuthRequest(BaseModel):
    id_token: str


class loginRequest(CleanBaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

class PasswordResetRequest(CleanBaseModel):
    """Schema for initiating password reset"""
    email: EmailStr


class PasswordResetVerify(CleanBaseModel):
    """Schema for verifying password reset OTP"""
    email: EmailStr
    otp: str
    new_password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str

    @model_validator(mode="after")
    def validate_passwords(self):
        if self.new_password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self