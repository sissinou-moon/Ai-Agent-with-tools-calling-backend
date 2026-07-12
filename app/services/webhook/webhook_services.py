from app.repositories.webhook_repository import WebhookRepository
from app.schemas.webhook import SaveEventWebhook
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.events import Event


class EventWebhookService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.webhook_repo = WebhookRepository(db)
        pass

    async def save_event_webhook(self, body: dict) -> bool:
        result = await self.webhook_repo.save_event_webhook(**body)
        return result

    