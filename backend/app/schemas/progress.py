from datetime import datetime

from pydantic import BaseModel, ConfigDict

class ProgressBase(BaseModel):
    content_id: int
    watched: bool = False
    rating: float | None = None
    notes: str | None = None

class ProgressCreate(BaseModel):
    content_id: int
    watched: bool

class ProgressUpdate(BaseModel):
    watched: bool | None = None
    rating: float | None = None
    notes: str | None = None

class ProgressOut(ProgressBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    watched_at: datetime | None = None

# --- /next response ---

class NextItemOut(BaseModel):
    id: int
    content_id: int
    title: str
    type: str
    position: int
    era: str | None = None
    poster_url: str | None = None
    runtime: int | None = None
    canonical: bool

# --- /stats response ---

class StatsOut(BaseModel):
    completed: int
    remaining: int
    percentage: float
    hours_watched: float
    hours_remaining: float