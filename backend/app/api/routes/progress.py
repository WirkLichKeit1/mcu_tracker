from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.models import Progress
from app.schemas.progress import ProgressCreate, ProgressOut, ProgressUpdate, StatsOut
from app.services.progress import ProgressService

router = APIRouter(tags=["progress"])

def get_service(db: Session = Depends(get_db)) -> ProgressService:
    return ProgressService(db)

@router.get("/marathons/{marathon_id}/progress", response_model=list[ProgressOut])
def list_progress(
    marathon_id: int,
    service: ProgressService = Depends(get_service),
) -> list[Progress]:
    return service.list(marathon_id=marathon_id)

@router.get("/marathons/{marathon_id}/stats", response_model=StatsOut)
def get_stats(
    marathon_id: int,
    service: ProgressService = Depends(get_service),
) -> StatsOut:
    return service.get_stats(marathon_id=marathon_id)

@router.post("/progress", response_model=ProgressOut, status_code=status.HTTP_201_CREATED)
def upsert_progress(
    schema: ProgressCreate,
    service: ProgressService = Depends(get_service),
) -> Progress:
    return service.upsert(schema)

@router.patch("/progress/{id}", response_model=ProgressOut)
def update_progress(
    id: int,
    schema: ProgressUpdate,
    service: ProgressService = Depends(get_service),
) -> Progress:
    return service.update(id, schema)