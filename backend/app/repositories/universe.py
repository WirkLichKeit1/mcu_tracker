from sqlalchemy.orm import Session

from app.models.models import Universe
from app.repositories.base import BaseRepository
from app.schemas.universe import UniverseCreate, UniverseUpdate

class UniverseRepository(BaseRepository[Universe]):
    def __init__(self, db: Session) -> None:
        super().__init__(Universe, db)

    def get_by_slug(self, slug: str) -> Universe | None:
        return self.db.query(Universe).filter(Universe.slug == slug).first()

    def create(self, schema: UniverseCreate) -> Universe: # type: ignore[override]
        obj = Universe(**schema.model_dump())
        return super().create(obj)

    def update(self, id: int, schema: UniverseUpdate) -> Universe | None:
        obj = self.get(id)
        if not obj:
            return None
        for field, value in schema.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj