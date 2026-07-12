from pydantic import BaseModel

class SaveEventWebhook(BaseModel):
    type: str
    data: dict