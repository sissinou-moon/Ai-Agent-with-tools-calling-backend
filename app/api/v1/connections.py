from app.schemas.connections import UpdateConnection
from app.schemas.connections import GithubSearchRequest
from app.services.connections.github_services import GitHubService
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.services.connections.connections_services import ConnectionService
from app.schemas.connections import SaveConnection
from app.core.security import get_current_user
from app.services.connections.notion_services import NotionService
from fastapi import APIRouter, Depends
from app.database import get_db

router = APIRouter(prefix="/connection", tags=["Connection"])    

@router.get("/notion/oauth")
async def notion_oauth():
    response = NotionService().notion_oauth()
    return response

@router.get("/notion/callback")
async def notion_callback(code: str, state: str):
    return await NotionService().exchange_code(code, state)

@router.get("/github/oauth")
async def github_oauth(db = Depends(get_db)):
    response = GitHubService(db).github_oauth()
    return response

@router.get("/github/callback")
async def github_callback(code: str, state: str, db = Depends(get_db)):
    return await GitHubService(db).exchange_code(code, state)

@router.post("/save")
async def save(body: SaveConnection, current_user=Depends(get_current_user), db = Depends(get_db)):
    user_id = current_user.get("sub")
    return await ConnectionService(db).save(user_id, body)

@router.get("/notion/databases")
async def notion_databases(body: dict, current_user=Depends(get_current_user)):
    access_token = body.get("access_token")
    user_id = current_user.get("sub")
    if not access_token:
        return {"error": "Access token is required"}
    return await NotionService().list_databases(access_token)

@router.post("/notion/add_row")
async def add_row(body: dict):
    access_token = body.get("access_token")
    database_id = body.get("database_id")
    properties = body.get("properties")
    schema = body.get("schema")
    if not access_token or not database_id or not properties:
        return {"error": "Access token, database ID, and properties are required"}
    return await NotionService().add_row_database(access_token, database_id, properties, schema)

@router.post("/github/search")
async def github_search(body: GithubSearchRequest, current_user=Depends(get_current_user), db = Depends(get_db)):
    return await GitHubService(db).search_repository(body.access_token, body.owner, body.repo, body.query, body.per_page)

@router.get("/github/user")
async def github_user(body: dict, current_user=Depends(get_current_user), db = Depends(get_db)):
    access_token = body.get("access_token")
    user_id = current_user.get("sub")
    if not access_token:
        return {"error": "Access token is required"}
    try:
        github_user = await GitHubService(db).search_user(access_token)

        repos = await GitHubService(db).read_repos(github_user.get("repos_url"))
        final_repos = []

        for repo in repos:
            final_repos.append({
                "name": repo.get("name"),
                "full_name": repo.get("full_name"),
                "id": repo.get("id"),
                "description": repo.get("description"),
            })
        
        updateConnection = UpdateConnection(
            user_id=user_id,
            app="github",
            access_token=access_token,
            data={
                "login": github_user.get("login"),
                "id": github_user.get("id"),
                "avatar_url": github_user.get("avatar_url"),
                "repos": final_repos
            }
        )

        await ConnectionService(db).update(updateConnection)
        
        return updateConnection
    except Exception as e:
        return {"error": str(e)}
