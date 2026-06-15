from sqlalchemy.orm import Session, joinedload

from app.models.models import MarathonItem, Progress
from app.repositories.base import BaseRepository
from app.schemas.marathon_item import MarathonItemCreate, MarathonItemUpdate

class MarathonItemRepository(BaseRepository[MarathonItem]):
    def __init__(self, db: Session) -> None:
        super().__init__(MarathonItem, db)

    def list_by_marathon(
        self,
        marathon_id: int,
        canonical_only: bool = False,
    ) -> list[MarathonItem]:
        query = (
            self.db.query(MarathonItem)
            .options(
                joinedload(MarathonItem.content),
                joinedload(MarathonItem.era),
            )
            .filter(MarathonItem.marathon_id == marathon_id)
        )
        if canonical_only:
            query = query.filter(MarathonItem.canonical.is_(True))
        return query.order_by(MarathonItem.position).all()

    def get_next(self, marathon_id: int, canonical_only: bool = False) -> MarathonItem | None:
        """Return the first unwatched item in the marathon."""
        watched_content_ids = (
            self.db.query(Progress.content_id)
            .filter(Progress.watched.is_(True))
            .scalar_subquery()
        )
        query = (
            self.db.query(MarathonItem)
            .options(
                joinedload(MarathonItem.content),
                joinedload(MarathonItem.era),
            )
            .filter(
                MarathonItem.marathon_id == marathon_id,
                MarathonItem.content_id.not_in(watched_content_ids),
            )
        )
        if canonical_only:
            query = query.filter(MarathonItem.canonical.is_(True))
        return query.order_by(MarathonItem.position).first()

    def create(self, schema: MarathonItemCreate) -> MarathonItem:  # type: ignore[override]
        obj = MarathonItem(**schema.model_dump())
        return super().create(obj)

    def update(self, id: int, schema: MarathonItemUpdate) -> MarathonItem | None:
        obj = self.get(id)
        if not obj:
            return None
        for field, value in schema.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj