from fastapi import HTTPException

def UserAleardyExists():
    raise HTTPException(
        status_code=409,
        detail="User Aleardy Exists",
    )

def UserNotFound():
    raise HTTPException(
        status_code=404,
        detail="User Not Exisit",
    )

def Unauthorized():
    raise HTTPException(
        status_code=401,
        detail="Unauthorized",
    )

def Forbidden():
    raise HTTPException(
        status_code=403,
        detail="Inactive Account",
    )

def EmailNotVerified():
    raise HTTPException(
        status_code=403,
        detail="Email Not Verified",
    )

def OTPNotFound():
    raise HTTPException(
        status_code=404,
        detail="OTP Not Found",
    )

def OTPInvalid():
    raise HTTPException(
        status_code=400,
        detail="Invalid OTP",
    )

def OTPExpired():
    raise HTTPException(
        status_code=400,
        detail="OTP Expired",
    )

def OtpAttempLimitReached():
    raise HTTPException(
        status_code=400,
        detail="OTP Attemp Limit Reached",
    )

def OTPSentAlready():
    raise HTTPException(
        status_code=429,
        detail="OTP Already Sent",
    )

def RefreshTokenInvalid():
    raise HTTPException(
        status_code=401,
        detail="Refresh Token Invalid",
    )

def SessionNotFound():
    raise HTTPException(
        status_code=404,
        detail="Session Not Found",
    )

