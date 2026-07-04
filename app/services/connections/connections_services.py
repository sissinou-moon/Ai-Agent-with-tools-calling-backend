from app.repositories.connections_repository import ConnectionRepository
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.connections import SaveConnection


class ConnectionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
        self.connection_repository = ConnectionRepository(db)

    async def save(self, user_id: str, body: SaveConnection):
        full_body = {
            "user_id": user_id,
            "app": body.app,
            "access_token": body.access_token,
            "data": {}
        }

        connection = await self.connection_repository.save(**full_body)

        await self.db.commit()
        await self.db.refresh(connection)

        return connection