from sqlalchemy import select
from sqlalchemy import update
from app.schemas.connections import UpdateConnection
from app.repositories.connections_repository import ConnectionRepository
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.connections import SaveConnection
from app.models.connections import Connection

class ConnectionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
        self.connection_repository = ConnectionRepository(db)

    async def save(self, user_id: str, body: SaveConnection):
        full_body = {
            "user_id": user_id,
            "app": body.app,
            "access_token": body.access_token,
            "data": body.data | {}
        }

        connection = await self.connection_repository.save(**full_body)

        await self.db.commit()
        await self.db.refresh(connection)

        return connection

    async def update(self, body: UpdateConnection):
        connection = await self.db.scalar(
            select(Connection).where(
                Connection.user_id == body.user_id,
                Connection.app == body.app
            )
        )
        
        if body.data:
            connection.data = {
                **(connection.data or {}),
                **body.data
            }
        
        if body.access_token:
            connection.access_token = body.access_token
        
        await self.db.commit()