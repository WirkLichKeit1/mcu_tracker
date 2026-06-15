from sqlalchemy.orm import Session

from app.models.models import Marathon
from app.repositories.base import BaseRepository
from app.schemas.marathon import MarathonCreate, MarathonUpdate

class MarathonRepository(BaseRepository[Marathon]):
    def __init__(self, db: Session) -> None:
        super().__init__(Marathon, db)

    def list_by_universe(self, universe_id: int) -> list[Marathon]:
        return (
            self.db.query(Marathon)
            .filter(Marathon.universe_id == universe_id)
            .all()
        )

    def create(self, schema: MarathonCreate) -> Marathon: # type: ignore[override]
        obj = Marathon(**schema.model_dump())
        return super().create(obj)

    def update(self, id: int, schema: MarathonUpdate) -> Marathon | None:
        obj = self.get(id)
        if not obj:
            return None
        for field, value in schema.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj