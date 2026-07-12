from app.core.security import get_current_user
from app.services.webhook.webhook_services import EventWebhookService
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.events import Event
from app.schemas.webhook import SaveEventWebhook

router = APIRouter(prefix="/webhook", tags=["Events Webhook"])    

@router.post("/events/save")
async def save_events_webhook(
    request: Request,
    body: SaveEventWebhook,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    event_webhook_service = EventWebhookService(db)

    try:
        final_body = {
            "type": body.type,
            "source": "webhook",
            "data": body.data,
            "user_id": current_user.get("sub")
        }
        result = await event_webhook_service.save_event_webhook(final_body)
        await db.commit()
        return {"data": result, "message": "Event webhook saved successfully"}
    except Exception as e:
        await db.rollback()
        return {"success": False, "message": str(e)}