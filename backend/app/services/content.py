from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import Content, ContentType
from app.repositories.content import ContentRepository
from app.schemas.content import ContentCreate, ContentUpdate

class ContentService:
    def __init__(self, db: Session) -> None:
        self.repo = ContentRepository(db)

    def list(
        self,
        skip: int = 0,
        limit: int = 100,
        type: ContentType | None = None,
    ) -> list[Content]:
        return self.repo.list(skip=skip, limit=limit, type=type)

    def get(self, id: int) -> Content:
        obj = self.repo.get(id)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Content {id} not found",
            )
        return obj

    def create(self, schema: ContentCreate) -> Content:
        if schema.tmdb_id and self.repo.get_by_tmdb_id(schema.tmdb_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Content with tmdb_id {schema.tmdb_id} already exists",
            )
        return self.repo.create(schema)

    def update(self, id: int, schema: ContentUpdate) -> Content:
        if schema.tmdb_id:
            existing = self.repo.get_by_tmdb_id(schema.tmdb_id)
            if existing and existing.id != id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"tmdb_id {schema.tmdb_id} is already taken",
                )
        obj = self.repo.update(id, schema)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Content {id} not found",
            )
        return obj

    def list_episodes(self, parent_id: int) -> list[Content]:
        parent = self.repo.get(parent_id)
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Content {parent_id} not found",
            )
        return self.repo.list_episodes(parent_id)

    def delete(self, id: int) -> None:
        if not self.repo.delete(id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Content {id} not found",
            )