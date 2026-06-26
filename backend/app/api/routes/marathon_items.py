from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.models import MarathonItem
from app.schemas.marathon_item import (
    MarathonItemCreate,
    MarathonItemDetailOut,
    MarathonItemOut,
    MarathonItemUpdate,
)
from app.schemas.progress import NextItemOut
from app.services.marathon_item import MarathonItemService

router = APIRouter(tags=["marathon_items"])

def get_service(db: Session = Depends(get_db)) -> MarathonItemService:
    return MarathonItemService(db)

@router.get("/marathons/{marathon_id}/items", response_model=list[MarathonItemDetailOut])
def list_marathon_items(
    marathon_id: int,
    canonical_only: bool = False,
    service: MarathonItemService = Depends(get_service),
) -> list[dict]:
    return service.list(marathon_id=marathon_id, canonical_only=canonical_only)

@router.get("/marathons/{marathon_id}/next", response_model=NextItemOut)
def get_next(
    marathon_id: int,
    canonical_only: bool = False,
    service: MarathonItemService = Depends(get_service),
) -> NextItemOut:
    return service.get_next(marathon_id=marathon_id, canonical_only=canonical_only)

@router.get("/items/{id}", response_model=MarathonItemOut)
def get_marathon_item(
    id: int,
    service: MarathonItemService = Depends(get_service),
) -> MarathonItem:
    return service.get(id)

@router.post("/items", response_model=MarathonItemOut, status_code=status.HTTP_201_CREATED)
def create_marathon_item(
    schema: MarathonItemCreate,
    service: MarathonItemService = Depends(get_service),
) -> MarathonItem:
    return service.create(schema)

@router.patch("/items/{id}", response_model=MarathonItemOut)
def update_marathon_item(
    id: int,
    schema: MarathonItemUpdate,
    service: MarathonItemService = Depends(get_service),
) -> MarathonItem:
    return service.update(id, schema)

@router.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_marathon_item(
    id: int,
    service: MarathonItemService = Depends(get_service),
) -> None:
    service.delete(id)