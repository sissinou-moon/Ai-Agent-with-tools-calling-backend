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