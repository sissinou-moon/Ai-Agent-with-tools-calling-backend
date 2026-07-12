import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta


from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


SECRET_KEY = "secret"
ALGORITHM = "HS256"

security = HTTPBearer()


def create_access_token(user_id: str, session_id: str):
    payload = {
        "sub": str(user_id),
        "sid": str(session_id),
        "type": "access",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: str):
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=30)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_webhook_token(user_id: str):
    payload = {
        "sub": str(user_id),
        "type": "token",
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_refresh_token(refresh_token: str) -> bool:
    try:
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "refresh":
            return None

        return True

    except ExpiredSignatureError:
        return None

    except InvalidTokenError:
        return None

def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload["type"] != "access":
            return None

        return payload

    except ExpiredSignatureError:
        return None

    except InvalidTokenError:
        return None
        
def verify_webhook_token(webhook_token: str):
    try:
        payload = jwt.decode(
            webhook_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "token":
            return None

        return payload

    except InvalidTokenError:
        return None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload