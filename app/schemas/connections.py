from pydantic import BaseModel

class SaveConnection(BaseModel):
    user_id: str
    app: str
    access_token: str