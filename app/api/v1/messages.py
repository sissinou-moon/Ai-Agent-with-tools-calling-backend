from uuid import UUID
from app.services.messages.messages import MessageService
from app.schemas.messages import MessageRequest
from app.core.security import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Request, Depends

router = APIRouter(prefix="/message", tags=["Message"])

@router.post("/{conversation_id}")
async def Send_Message(
    request: Request,
    body: MessageRequest,
    conversation_id: str,
    #current_user = Depends(get_current_user),
):

    message_service = MessageService()
    message = await message_service.message(
        #current_user.id, 
        user_id=UUID("12345678-1234-5678-1234-567812345678"), 
        body=body, 
        conversation_id=conversation_id
    )
    
    return {
        "message": message
    }
    