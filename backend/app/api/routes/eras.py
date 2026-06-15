from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.models import Era
from app.schemas.era import EraCreate, EraOut, EraUpdate
from app.services.era import EraService

router = APIRouter(prefix="/eras", tags=["eras"])

def get_service(db: Session = Depends(get_db)) -> EraService:
    return EraService(db)

@router.get("", response_model=list[EraOut])
def list_eras(
    marathon_id: int,
    service: EraService = Depends(get_service),
) -> list[Era]:
    return service.list(marathon_id=marathon_id)

@router.get("/{id}", response_model=EraOut)
def get_era(
    id: int,
    service: EraService = Depends(get_service),
) -> Era:
    return service.get(id)

@router.post("", response_model=EraOut, status_code=status.HTTP_201_CREATED)
def create_era(
    schema: EraCreate,
    service: EraService = Depends(get_service),
) -> Era:
    return service.create(schema)

@router.patch("/{id}", response_model=EraOut)
def update_era(
    id: int,
    schema: EraUpdate,
    service: EraService = Depends(get_service),
) -> Era:
    return service.update(id, schema)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_era(
    id: int,
    service: EraService = Depends(get_service),
) -> None:
    service.delete(id)