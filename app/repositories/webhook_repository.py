from app.models.events import Event
from app.schemas.webhook import SaveEventWebhook
from sqlalchemy.ext.asyncio import AsyncSession
class WebhookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        pass

    async def save_event_webhook(self, **kwargs) -> bool:
        event_webhook = Event(**kwargs)
        self.db.add(event_webhook)
        return True