from typing import List
from app.repositories.connections_repository import ConnectionRepository
from fastapi import HTTPException
from urllib.parse import urlencode
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
import secrets
from fastapi.responses import RedirectResponse
import httpx

class GitHubService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.client_id = settings.GITHUB_CLIENT_ID
        self.client_secret = settings.GITHUB_CLIENT_SECRET
        self.redirect_uri = settings.GITHUB_REDIRECT_URI
        self.connection_repository = ConnectionRepository(db)

    def github_oauth(self):
        state = secrets.token_urlsafe(32)
        parames = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "user,repo,write:public_repo",
            "state": state
        }
        url = "https://github.com/login/oauth/authorize?" + urlencode(parames)
        return RedirectResponse(url)

    async def exchange_code(self, code: str, state: str):
        # TODO:
        # verify state matches what you generated

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://github.com/login/oauth/access_token",
                headers={
                    "Accept": "application/json"
                },
                json={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": self.redirect_uri,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=response.json(),
            )

        token_data = response.json()

        return token_data

    async def search_repository(
        self,
        access_token: str,
        owner: str,
        repo: str,
        query: str,
        per_page: int = 10,
    ) -> List[dict]:

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        params = {
            "q": f"{query} repo:{owner}/{repo}",
            "per_page": per_page,
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                "https://api.github.com/search/code",
                headers=headers,
                params=params,
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json(),
            )

        data = response.json()

        results = []

        for item in data.get("items", []):
            results.append(
                {
                    "name": item["name"],
                    "path": item["path"],
                    "sha": item["sha"],
                    "url": item["html_url"],
                    "repository": item["repository"]["full_name"],
                }
            )

        return results

    async def search_user(self, access_token: str):
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                "https://api.github.com/user",
                headers=headers,
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json(),
            )

        return response.json()

    async def read_repos(self, url: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            response.raise_for_status()

            repos = response.json()

        return repos