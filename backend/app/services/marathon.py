from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import Marathon
from app.repositories.marathon import MarathonRepository
from app.repositories.universe import UniverseRepository
from app.schemas.marathon import MarathonCreate, MarathonUpdate

class MarathonService:
    def __init__(self, db: Session) -> None:
        self.repo = MarathonRepository(db)
        self.universe_repo = UniverseRepository(db)

    def list(self, universe_id: int | None = None) -> list[Marathon]:
        if universe_id is not None:
            return self.repo.list_by_universe(universe_id)
        return self.repo.list()

    def get(self, id: int) -> Marathon:
        obj = self.repo.get(id)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Marathon {id} not found",
            )
        return obj

    def create(self, schema: MarathonCreate) -> Marathon:
        if not self.universe_repo.get(schema.universe_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Universe {schema.universe_id} not found",
            )
        return self.repo.create(schema)

    def update(self, id: int, schema: MarathonUpdate) -> Marathon:
        obj = self.repo.update(id, schema)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Marathon {id} not found",
            )
        return obj

    def delete(self, id: int) -> None:
        if not self.repo.delete(id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Marathon {id} not found",
            )