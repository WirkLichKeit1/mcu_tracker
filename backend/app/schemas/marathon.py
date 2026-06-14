from datetime import datetime

from pydantic import BaseModel, ConfigDict

class MarathonBase(BaseModel):
    universe_id: int
    name: str
    description: str | None = None

class MarathonCreate(MarathonBase):
    pass

class MarathonUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class MarathonOut(MarathonBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime