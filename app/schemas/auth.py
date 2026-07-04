from pydantic import Field
from pydantic import BaseModel
from uuid import UUID

class RegisterRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=10
    )
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class VerifyEmailRequest(BaseModel):
    email: str
    otp: str

class LogoutRequest(BaseModel):
    refresh_token: str
    user_id: UUID

class RefreshRequest(BaseModel):
    refresh_token: str

