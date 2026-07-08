from pydantic import BaseModel

class SaveConnection(BaseModel):
    user_id: str
    app: str
    access_token: str
    data: dict

class GithubSearchRequest(BaseModel):
    access_token: str
    owner: str
    repo: str
    query: str
    per_page: int = 10

class UpdateConnection(BaseModel):
    user_id: str
    app: str
    access_token: str | None = None
    data: dict | None = None
