from app.models.connections import Connection

class ConnectionRepository:
    def __init__(self, db):
        self.db = db

    async def save(self, **kwargs):
        connection = Connection(**kwargs)
        self.db.add(connection)
        return connection