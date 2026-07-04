from app.schemas.auth import RefreshRequest
from app.core.security import get_current_user
from app.schemas.auth import LogoutRequest
from app.schemas.auth import VerifyEmailRequest
from app.database import get_db
from app.services.auth import AuthService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Request
from app.core.limiter import limiter
from app.schemas.auth import RegisterRequest, LoginRequest
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
@limiter.limit("1/minute")
async def Register(
    request: Request,
    body: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    return await AuthService(db).register(
        body=body,
        ip=request.state.ip,
        user_agent=request.state.user_agent,
        request_id=request.state.request_id,
    )

@router.post("/verify")
async def Verify(request: Request, body: VerifyEmailRequest, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).verify_email(
        body=body,
        ip=request.state.ip,
        user_agent=request.state.user_agent,
        request_id=request.state.request_id,
    )

@router.post("/login")
async def Login(request: Request, body: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).login(
        body=body,
        ip=request.state.ip,
        user_agent=request.state.user_agent,
        request_id=request.state.request_id,
    )

@router.post("/refresh")
async def Refresh(
    request: Request,
    body: RefreshRequest,
    db: AsyncSession = Depends(get_db)
):
    return await AuthService(db).refresh(
        body=body,
        ip=request.state.ip,
        user_agent=request.state.user_agent,
        request_id=request.state.request_id,
    )

@router.post("/logout")
async def Logout(request: Request, body: LogoutRequest, db: AsyncSession = Depends(get_db)):
    return await AuthService(db).logout(
        body=body,
        ip=request.state.ip,
        user_agent=request.state.user_agent,
        request_id=request.state.request_id,
    )

@router.get("/me")
async def Me(request: Request, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):

    return current_user

@router.delete("/sessions/{session_id}")
async def Delete_Session(
    request: Request,
    session_id: str, 
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(get_current_user)
):

    await AuthService(db).revoke_session(
        session_id, 
        current_user["sub"],
        request.state.request_id,
        request.state.ip,
        request.state.user_agent,
    )

    return {
        "session_id": session_id,
        "revoked": True
    }
