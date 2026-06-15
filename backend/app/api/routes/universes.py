from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.models import Universe
from app.schemas.universe import UniverseCreate, UniverseOut, UniverseUpdate
from app.services.universe import UniverseService

router = APIRouter(prefix="/universes", tags=["universes"])

def get_service(db: Session = Depends(get_db)) -> UniverseService:
    return UniverseService(db)

@router.get("", response_model=list[UniverseOut])
def list_universes(
    skip: int = 0,
    limit: int = 100,
    service: UniverseService = Depends(get_service),
) -> list[Universe]:
    return service.list(skip=skip, limit=limit)

@router.get("/{id}", response_model=UniverseOut)
def get_universe(
    id: int,
    service: UniverseService = Depends(get_service),
) -> Universe:
    return service.get(id)

@router.post("", response_model=UniverseOut, status_code=status.HTTP_201_CREATED)
def create_universe(
    schema: UniverseCreate,
    service: UniverseService = Depends(get_service),
) -> Universe:
    return service.create(schema)

@router.patch("/{id}", response_model=UniverseOut)
def update_universe(
    id: int,
    schema: UniverseUpdate,
    service: UniverseService = Depends(get_service),
) -> Universe:
    return service.update(id, schema)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_universe(
    id: int,
    service: UniverseService = Depends(get_service),
) -> None:
    service.delete(id)