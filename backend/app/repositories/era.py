from sqlalchemy.orm import Session

from app.models.models import Era
from app.repositories.base import BaseRepository
from app.schemas.era import EraCreate, EraUpdate

class EraRepository(BaseRepository[Era]):
    def __init__(self, db: Session) -> None:
        super().__init__(Era, db)

    def list_by_marathon(self, marathon_id: int) -> list[Era]:
        return (
            self.db.query(Era)
            .filter(Era.marathon_id == marathon_id)
            .order_by(Era.position)
            .all()
        )

    def create(self, schema: EraCreate) -> Era:  # type: ignore[override]
        obj = Era(**schema.model_dump())
        return super().create(obj)

    def update(self, id: int, schema: EraUpdate) -> Era | None:
        obj = self.get(id)
        if not obj:
            return None
        for field, value in schema.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj