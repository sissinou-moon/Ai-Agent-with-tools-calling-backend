from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.messages import router as message_router
from app.api.v1.connections import router as connection_router
from app.api.v2.events_webhook import router as events_webhook_router

router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
router.include_router(message_router)
router.include_router(connection_router)
router.include_router(events_webhook_router)
