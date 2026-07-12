from sqlalchemy import select
from app.models.connections import Connection
from app.models.events import Event

class ConnectionRepository:
    def __init__(self, db):
        self.db = db

    async def save(self, **kwargs):
        connection = Connection(**kwargs)
        self.db.add(connection)
        return connection

    async def read_events_by_user_id(self, user_id: str):
        result = await self.db.execute(
            select(Event).where(
                Event.user_id == user_id
            )
        )
        return result.scalars().all()