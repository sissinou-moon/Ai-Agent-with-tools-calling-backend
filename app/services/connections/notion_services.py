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

    async def list_databases(self, access_token: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.notion.com/v1/search",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Notion-Version": "2022-06-28",
                },
                json={
                    "filter": {
                        "property": "object",
                        "value": "database"
                    }
                }
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=response.json(),
            )

        result = response.json()
        structured_response = []

        for database in result["results"]:
            structured_response.append({
                "title": database["title"][0]["plain_text"],
                "id": database["id"],
                "properties": database["properties"]
            })


        return structured_response

    async def add_row_database(
        self,
        access_token: str,
        database_id: str,
        properties: dict,
        schema: dict
    ):
        structured_properties = {}

        # 1️⃣ Normalize Title (Text)
        if "Title" in schema:
            title_schema = schema["Title"]
            if title_schema["type"] == "title" and "Title" in properties:
                structured_properties["Title"] = {"title": [{"text": {"content": properties["Title"]}}]}
                del properties["Title"]

        # 2️⃣ Handle Each Column Based on Type
        for name, value in properties.items():
            if name not in schema:
                # Skip columns that don't exist in the schema
                continue

            prop_type = schema[name]["type"]

            if prop_type == "title":
                # Already handled above, but safe to keep
                structured_properties[name] = {"title": [{"text": {"content": str(value)}}]}

            elif prop_type == "rich_text":
                structured_properties[name] = {"rich_text": [{"text": {"content": str(value)}}]}

            elif prop_type == "number":
                structured_properties[name] = {"number": float(value)}

            elif prop_type == "checkbox":
                structured_properties[name] = {"checkbox": bool(value)}

            elif prop_type == "select":
                structured_properties[name] = {
                    "select": {"name": str(value)}
                }

            elif prop_type == "multi_select":
                if isinstance(value, list):
                    structured_properties[name] = {"multi_select": [{"name": str(v)} for v in value]}
                else:
                    # Handle single string input
                    structured_properties[name] = {"multi_select": [{"name": str(value)}]}

            elif prop_type == "date":
                # Handle ISO format or timestamp
                structured_properties[name] = {"date": {"start": str(value)}}

            elif prop_type == "email":
                structured_properties[name] = {"email": str(value)}

            elif prop_type == "phone":
                structured_properties[name] = {"phone_number": str(value)}

            elif prop_type == "url":
                structured_properties[name] = {"url": str(value)}

        # 3️⃣ Add the database_id → parent
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.notion.com/v1/pages",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Notion-Version": "2022-06-28",
                },
                json={
                    "parent": {
                        "database_id": database_id
                    },
                    "properties": structured_properties
                }
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json(),
            )

        return response.json()