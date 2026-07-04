from app.schemas.auth import RefreshRequest
from uuid import UUID
from app.middlewares.error_handler import SessionNotFound
from app.schemas.auth import LogoutRequest
from app.middlewares.error_handler import RefreshTokenInvalid
from app.middlewares.error_handler import OtpAttempLimitReached
from app.middlewares.error_handler import OTPInvalid
from app.middlewares.error_handler import OTPExpired
from app.middlewares.error_handler import OTPNotFound
from app.repositories.otp_repository import OTPRepository
from app.schemas.auth import VerifyEmailRequest
from app.services.audit_service import AuditService
from app.middlewares.error_handler import UserAleardyExists, UserNotFound, Forbidden, Unauthorized, EmailNotVerified
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import RegisterRequest, LoginRequest

from app.repositories.user_repository import UserRepository

from app.services.password_service import PasswordService
from app.services.otp_service import OTPService
from app.models.users import User
from app.core.security import verify_refresh_token, create_access_token, create_refresh_token
from app.repositories.session_repository import SessionRepository
# pyrefly: ignore [missing-import]
from user_agents import parse
from datetime import datetime, timedelta, UTC
from uuid import uuid4

class AuthService:

    def __init__(self, db: AsyncSession):
        self.db = db

        self.user_repository = UserRepository(db)

        self.password_service = PasswordService()
        self.otp_service = OTPService(db)
        self.audit_service = AuditService(db)

        self.session_repository = SessionRepository(db)
        self.otp_repository = OTPRepository(db)

    async def register(
        self,
        body: RegisterRequest,
        ip: str,
        user_agent: str,
        request_id: str,
    ):

        # 1. Normalize & validate data
        email = body.email.lower().strip()
        username = body.username.lower().strip()

        # 2. Check if email already exists
        alreadyExists = await self.user_repository.get_by_email(email)
        if alreadyExists:
            return UserAleardyExists()

        # 3. Hash password
        password = self.password_service.hash(body.password)

        # 4. Generate OTP
        otp = self.otp_service.generate()

        # 5. Save user
        user_id = uuid4()
        await self.user_repository.create(
            id=user_id,
            email=email,
            username=username,
            password=password,
            is_verified=False,
            is_active=True,
            is_admin=False,
        )
        # 6. Save OTP
        await self.otp_service.save_otp(
            user_id=user_id,
            otp=str(otp),
            attempts=0,
            expires_at = self.otp_service.expires_at(),
            is_verified = False,
            purpose="registration"
        )

        # 7. Send OTP email
        await self.otp_service.sendEmailOTP(email, otp)

        # 8. Log registration
        await self.audit_service.log_event(
            user_id=user_id,
            event="Registration",
            ip=ip,
            user_agent=user_agent,
        )
        # 9. Return response
        return {
            "message": "User registered successfully",
            "user_id": user_id,
            "otp": otp,
        }

    async def login(
        self,
        body: LoginRequest,
        ip: str,
        user_agent: str,
        request_id: str
    ):

        # 1- NORMILAZE COMMING DATA
        email = body.email.lower().strip()
        password = body.password
        refresh_token = body.refresh_token

        # 2- CHECK IF USER WITH THIS EMAIL REALLY EXISIT
        user: User = await self.user_repository.get_by_email(email)
        if not user:
            return UserNotFound()

        # 3- VERIFY PASSWORD
        is_valid_password = self.password_service.verify(password, user.password)
        if not is_valid_password:
            return Unauthorized()

        # 4- VIRIFY THE ACCOUNT STATES (IS ACTIVE / IS VERIFIED)
        if not user.is_active:
            return Forbidden()
        elif not user.is_verified:
            return EmailNotVerified()

        # 5- VERIFY THE REFRESH-TOKEN
        is_valid_refresh_token = verify_refresh_token(refresh_token)
        if is_valid_refresh_token:
            new_refresh_token = create_refresh_token(user.id)
            ua = parse(user_agent)
            await self.session_repository.revoke_all_sessions(user.id)
            session = await self.session_repository.create_new_session(
                user_id = user.id,
                refresh_token = new_refresh_token,
                ip = ip,
                user_agent = user_agent,
                device_name = ua.device.family,
                expires_at = datetime.now(UTC) + timedelta(days=30)
            )

            # 7- CREATE NEW ACCESS-TOKEN
            access_token = create_access_token(user.id, session.id)
            return {
                "message" : "Welcome Back!",
                "refresh_token": new_refresh_token,
                "old_refresh_token": refresh_token,
                "access_token": access_token,
                "user": user
            }

        # 6- SEND OTP
        otp = self.otp_service.generate()
        await self.otp_service.save_otp(
            user_id=user.id,
            otp=str(otp),
            attempts=0,
            expires_at = self.otp_service.expires_at(),
            is_verified = False,
            purpose="registration"
        )
        await self.otp_service.sendEmailOTP(email, otp)

        # 7- RETURN
        return RefreshTokenInvalid()

    async def verify_email(
        self,
        body: VerifyEmailRequest,
        ip: str,
        user_agent: str,
        request_id: str
    ):
        # 1- NORMILAZE
        email = body.email.lower().strip()
        otp = body.otp

        # 2- CHECK IF USER EXISTS
        user: User = await self.user_repository.get_by_email(email)
        if not user:
            return UserNotFound()

        # 3- VERIFY OTP
        database_otp = await self.otp_repository.get_by_email(user.id)
        if not database_otp:
            return OTPNotFound()

        if database_otp.otp != otp:
            database_otp.attempts += 1
            await self.db.commit()
            await self.db.refresh(database_otp)
            return OTPInvalid()
        
        # 5- VERIFY OTP ATTEMPTS
        if database_otp.attempts >= 5:
            return OtpAttempLimitReached()

        # 5.1 VERIFY OTP EXPIRES_AT
        if self.otp_service.is_expired(database_otp.expires_at):
            return OTPExpired()
        
        # 6- UPDATE OTP
        database_otp.is_verified = True
        database_otp.attempts += 1
        await self.db.commit()
        await self.db.refresh(database_otp)
        
        # 7- UPDATE USER
        user.is_verified = True
        await self.db.commit()
        await self.db.refresh(user)

        # 8- REVOKE ALL OLD SESSIONS
        await self.session_repository.revoke_all_sessions(user.id)

        # 8.1- CREATE NEW SESSION
        refresh_token = create_refresh_token(user.id)
        ua = parse(user_agent)
        session = await self.session_repository.create_new_session(
            user_id = user.id,
            refresh_token = refresh_token,
            ip = ip,
            user_agent = user_agent,
            device_name = ua.device.family,
            expires_at = datetime.now(UTC) + timedelta(days=30)
        )
        access_token = create_access_token(user.id, session.id)

        # 9- RETURN
        return {
            "message": "Email Verified Successfully",
            "is_verified": True,
            "refresh_token": refresh_token,
            "access_token": access_token,
            "user": user
        }

    
    async def logout(
        self, 
        body: LogoutRequest,
        request_id: str,
        user_agent: str,
        ip: str,
    ):
        # 1- NORMILAZE
        refresh_token = body.refresh_token
        user_id = body.user_id
        
        # 2- CHECK IF SESSION EXISTS
        session = await self.session_repository.get_by_refresh_token(refresh_token)
        if not session:
            return SessionNotFound()
        
        # 3- REVOKE ALL USER'S SESSIONS
        await self.session_repository.revoke_all_sessions(user_id)

        # 4- RETURN LOGOUTED
        return {
            "message": "Logged out successfully"
        }
        
        
    async def revoke_session(
        self, 
        session_id: str,
        user_id: str,
        request_id: str,
        ip: str,
        user_agent: str,
    ):

        # 1 - NORMILAZE
        session_id = UUID(session_id.strip())
        user_id = UUID(user_id.strip())

        # 2 - CHECK IF SESSION EXISTS
        session = await self.session_repository.get_by_id(session_id)
        if not session:
            return SessionNotFound()

        # 3 - REVOKE SESSION
        await self.session_repository.revoke_session(session_id)

        # 4 - LOG THE EVENT
        await self.audit_service.log_event(
            user_id=user_id,
            event="Session Revoked",
            ip=ip,
            user_agent=user_agent,
        )

        # 5 - RETURN
        return {
            "message": "Session revoked successfully"
        }

    async def refresh(
        self, 
        body: RefreshRequest,
        ip: str,
        user_agent: str,
        request_id: str,
    ):

        # 1. Verify JWT
        payload = verify_refresh_token(body.refresh_token)
    
        if not payload:
            return RefreshTokenInvalid()
    
        # 2. Find session
        session = await self.session_repository.get_by_refresh_token(
            body.refresh_token
        )
    
        if not session:
            return SessionNotFound()
    
        # 3. Ensure session isn't revoked
        if session.revoked:
            return Unauthorized()
    
        # 4. Create new tokens
        access_token = create_access_token(
            session.user_id,
            session.id,
        )
    
        return {
            "access_token": access_token,
            "refresh_token": body.refresh_token,
        }
            
    
            
            
            
    