from sqlalchemy.orm import Session

from app.models.models import Content, ContentType
from app.repositories.base import BaseRepository
from app.schemas.content import ContentCreate, ContentUpdate

from typing import List

class ContentRepository(BaseRepository[Content]):
    def __init__(self, db: Session) -> None:
        super().__init__(Content, db)

    def list(
        self,
        skip: int = 0,
        limit: int = 100,
        type: ContentType | None = None,
    ) -> List[Content]:
        query = self.db.query(Content)
        if type is not None:
            query = query.filter(Content.type == type)
        return query.offset(skip).limit(limit).all()

    def list_episodes(self, parent_id: int) -> List[Content]:
        return (
            self.db.query(Content)
            .filter(Content.parent_id == parent_id)
            .order_by(Content.episode_number)
            .all()
        )

    def get_by_tmdb_id(self, tmdb_id: int) -> Content | None:
        return self.db.query(Content).filter(Content.tmdb_id == tmdb_id).first()

    def create(self, schema: ContentCreate) -> Content:  # type: ignore[override]
        obj = Content(**schema.model_dump())
        return super().create(obj)

    def update(self, id: int, schema: ContentUpdate) -> Content | None:
        obj = self.get(id)
        if not obj:
            return None
        for field, value in schema.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj