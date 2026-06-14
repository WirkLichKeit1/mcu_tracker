from datetime import datetime

from pydantic import BaseModel, ConfigDict

class UniverseBase(BaseModel):
    name: str
    slug: str
    description: str | None = None

class UniverseCreate(UniverseBase):
    pass

class UniverseUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None

class UniverseOut(UniverseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime