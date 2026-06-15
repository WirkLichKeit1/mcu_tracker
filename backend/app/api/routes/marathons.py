from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.models import Marathon
from app.schemas.marathon import MarathonCreate, MarathonOut, MarathonUpdate
from app.services.marathon import MarathonService

router = APIRouter(prefix="/marathons", tags=["marathons"])

def get_service(db: Session = Depends(get_db)) -> MarathonService:
    return MarathonService(db)

@router.get("/", response_model=list[MarathonOut])
def list_marathons(
    universe_id: int | None = None,
    service: MarathonService = Depends(get_service),
) -> list[Marathon]:
    return service.list(universe_id=universe_id)

@router.get("/{id}", response_model=MarathonOut)
def get_marathon(
    id: int,
    service: MarathonService = Depends(get_service),
) -> Marathon:
    return service.get(id)

@router.post("/", response_model=MarathonOut, status_code=status.HTTP_201_CREATED)
def create_marathon(
    schema: MarathonCreate,
    service: MarathonService = Depends(get_service),
) -> Marathon:
    return service.create(schema)

@router.patch("/{id}", response_model=MarathonOut)
def update_marathon(
    id: int,
    schema: MarathonUpdate,
    service: MarathonService = Depends(get_service),
) -> Marathon:
    return service.update(id, schema)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_marathon(
    id: int,
    service: MarathonService = Depends(get_service),
) -> None:
    service.delete(id)