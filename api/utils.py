from typing import Any, Dict, Optional
import smtplib, os
from dotenv import load_dotenv

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

load_dotenv()
def success_response(status_code: int, message: str, data: Optional[dict] = None):
    """Returns a JSON response for success responses"""

    response_data = {
        "status": "success",
        "status_code": status_code,
        "message": message,
        "data": data or {},  # Ensure data is always a dictionary
    }

    return JSONResponse(
        status_code=status_code, content=jsonable_encoder(response_data)
    )


def auth_response(
    status_code: int, message: str, access_token: str, refresh_token: str, data: Optional[dict] = None
):
    """Returns a JSON response for successful auth responses"""

    response_data = {
        "status": "success",
        "status_code": status_code,
        "message": message,
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            **(data or {}),  # Merge additional data if provided
        },
    }

    return JSONResponse(
        status_code=status_code, content=jsonable_encoder(response_data)
    )


def fail_response(status_code: int, message: str, data: Optional[dict] = None):
    """Returns a JSON response for failure responses"""

    response_data = {
        "status": "failure",
        "status_code": status_code,
        "message": message,
        "data": data or {},  # Ensure data is always a dictionary
    }

    return JSONResponse(
        status_code=status_code, content=jsonable_encoder(response_data)
    )


def send_otp_email(email: str, otp: str):
        """Send OTP to user's email (basic SMTP example)"""
        # NOTE: Replace with your SMTP server / provider
        smtp_host = os.getenv("EMAIL_HOST", "smtp.example.com")
        smtp_port = 587
        smtp_user = os.getenv("EMAIL_USERNAME")
        smtp_password = os.getenv("EMAIL_PASSWORD")

        subject = "Your Verification OTP"
        body = f"Hello,\n\nYour OTP code is: {otp}\nIt will expire in 10 minutes.\n\nThank you."
        msg = f"From: {smtp_user}\nTo: {email}\nSubject: {subject}\n\n{body}"
        try:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(smtp_user, email, msg)
        except Exception as e:
            print("Failed to send OTP email:", e)

def send_password_reset_email(email: str, otp: str):
        """Send password reset OTP to user's email"""
        smtp_host = os.getenv("EMAIL_HOST", "smtp.example.com")
        smtp_port = 587
        smtp_user = os.getenv("EMAIL_USERNAME")
        smtp_password = os.getenv("EMAIL_PASSWORD")

        subject = "Password Reset OTP"
        body = f"Hello,\n\nYour password reset code is: {otp}\nIt will expire in 10 minutes.\n\nIf you did not request this, please ignore this email.\n\nThank you."
        msg = f"From: {smtp_user}\nTo: {email}\nSubject: {subject}\n\n{body}"
        try:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(smtp_user, email, msg)
        except Exception as e:
            print("Failed to send password reset email:", e)



            