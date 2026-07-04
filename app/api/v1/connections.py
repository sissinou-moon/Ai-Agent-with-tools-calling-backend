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
