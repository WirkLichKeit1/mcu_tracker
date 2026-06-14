from pydantic import BaseModel, ConfigDict

from app.schemas.content import ContentOut
from app.schemas.era import EraOut

class MarathonItemBase(BaseModel):
    marathon_id: int
    content_id: int
    era_id: int | None = None
    position: int
    canonical: bool = True

class MarathonItemCreate(MarathonItemBase):
    pass

class MarathonItemUpdate(BaseModel):
    era_id: int | None = None
    position: int | None = None
    canonical: bool | None = None

class MarathonItemOut(MarathonItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class MarathonItemDetailOut(MarathonItemOut):
    """Marathon item with nested content and era data."""

    content: ContentOut
    era: EraOut | None = None