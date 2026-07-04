from urllib.parse import urlencode
from app.core.config import settings
import secrets
from fastapi.responses import RedirectResponse
from fastapi import HTTPException, Query
import base64, requests
import httpx

def basic_auth_header(client_id: str, client_secret: str) -> str:
    token = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    return f"Basic {token}"

class NotionService:
    def __init__(self):
        self.client_id = settings.NOTION_CLIENT_ID
        self.client_secret = settings.NOTION_CLIENT_SECRET
        self.redirect_url = settings.NOTION_REDIRECT_URL
        self.base_url = "https://api.notion.com/v1"

    def notion_oauth(self):
        state = secrets.token_urlsafe(32)
    
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "owner": "user",
            "redirect_uri": self.redirect_url,
            "state": state,
        }
        url = "https://api.notion.com/v1/oauth/authorize?" + urlencode(params)
        return RedirectResponse(url)

    async def exchange_code(self, code: str, state: str):
        # TODO:
        # verify state matches what you generated

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.notion.com/v1/oauth/token",
                auth=(self.client_id, self.client_secret),
                json={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": self.redirect_url,
                },
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=response.json(),
            )

        token_data = response.json()

        # Save to your database
        # access_token
        # workspace_id
        # workspace_name
        # bot_id
        # owner
        # duplicated_template_id (if present)

        return token_data

    