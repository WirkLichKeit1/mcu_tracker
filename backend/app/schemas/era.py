from pydantic import BaseModel, ConfigDict

class EraBase(BaseModel):
    marathon_id: int
    name: str
    position: int

class EraCreate(EraBase):
    pass

class EraUpdate(BaseModel):
    name: str | None = None
    position: int | None = None

class EraOut(EraBase):
    model_config = ConfigDict(from_attributes=True)

    id: int