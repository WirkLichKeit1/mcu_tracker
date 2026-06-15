from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import Era
from app.repositories.era import EraRepository
from app.repositories.marathon import MarathonRepository
from app.schemas.era import EraCreate, EraUpdate

class EraService:
    def __init__(self, db: Session) -> None:
        self.repo = EraRepository(db)
        self.marathon_repo = MarathonRepository(db)

    def list(self, marathon_id: int) -> list[Era]:
        return self.repo.list_by_marathon(marathon_id)

    def get(self, id: int) -> Era:
        obj = self.repo.get(id)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Era {id} not found",
            )
        return obj

    def create(self, schema: EraCreate) -> Era:
        if not self.marathon_repo.get(schema.marathon_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Marathon {schema.marathon_id} not found",
            )
        return self.repo.create(schema)

    def update(self, id: int, schema: EraUpdate) -> Era:
        obj = self.repo.update(id, schema)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Era {id} not found",
            )
        return obj

    def delete(self, id: int) -> None:
        if not self.repo.delete(id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Era {id} not found",
            )