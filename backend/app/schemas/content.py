from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.models import ContentType

class ContentBase(BaseModel):
    tmdb_id: int | None = None
    title: str
    description: str | None = None
    type: ContentType
    poster_url: str | None = None
    release_date: str | None = None
    runtime: int | None = None

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    tmdb_id: int | None = None
    title: str | None = None
    description: str | None = None
    type: ContentType | None = None
    poster_url: str | None = None
    release_date: str | None = None
    runtime: int | None = None

class ContentOut(ContentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    episode_number: int | None = None
    parent_id: int | None = None
    created_at: datetime