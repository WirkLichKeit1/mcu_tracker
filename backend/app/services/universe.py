from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import Universe
from app.repositories.universe import UniverseRepository
from app.schemas.universe import UniverseCreate, UniverseUpdate

class UniverseService:
    def __init__(self, db: Session) -> None:
        self.repo = UniverseRepository(db)

    def list(self, skip: int = 0, limit: int = 100) -> list[Universe]:
        return self.repo.list(skip=skip, limit=limit)

    def get(self, id: int) -> Universe:
        obj = self.repo.get(id)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Universe {id} not found",
            )
        return obj

    def create(self, schema: UniverseCreate) -> Universe:
        if self.repo.get_by_slug(schema.slug):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Universe with slug '{schema.slug}' already exists",
            )
        return self.repo.create(schema)

    def update(self, id: int, schema: UniverseUpdate) -> Universe:
        if schema.slug:
            existing = self.repo.get_by_slug(schema.slug)
            if existing and existing.id != id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Slug '{schema.slug}' is already taken",
                )
        obj = self.repo.update(id, schema)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Universe {id} not found",
            )
        return obj

    def delete(self, id: int) -> None:
        if not self.repo.delete(id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Universe {id} not found",
            )