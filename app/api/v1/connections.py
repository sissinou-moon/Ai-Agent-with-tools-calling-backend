from app.services.connections.notion_services import NotionService
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/connection", tags=["Connection"])    

@router.get("/notion/oauth")
async def notion_oauth():
    response = NotionService().notion_oauth()
    return response

@router.get("/notion/callback")
async def notion_callback(code: str, state: str):
    return await NotionService().exchange_code(code, state)

@router.get("/notion/databases")
async def notion_databases(body: dict):
    access_token = body.get("access_token")
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
