from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
from app.core.config import settings
import httpx
import secrets
from email.message import EmailMessage
import base64


state = secrets.token_urlsafe(32)

class GmailService:
    def __init__(self):
        self.client_id = settings.GMAIL_CLIENT_ID
        self.client_secret = settings.GMAIL_CLIENT_SECRET
        self.redirect_uri = settings.GMAIL_REDIRECT_URI

    def gmail_oauth(self):
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.send",
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent",
            "state": state
        }
        return RedirectResponse("https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params))

    async def exchange_code(self, code: str, state: str):
        params = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code"
        }
        
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://oauth2.googleapis.com/token?" + urlencode(params)
            )

        print(response.status_code)
        print(response.text)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text,
            )

        return response.json()

    async def send_email(self, access_token: str, to: str, subject: str, body: str):
        message = EmailMessage()
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body)

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://www.googleapis.com/gmail/v1/users/me/messages/send?",
                headers={
                    "Authorization": f"Bearer {access_token}"
                },
                json={
                    "raw": encoded_message
                }
            )

        print(response.status_code)
        print(response.text)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text,
            )

        return response.json()
            