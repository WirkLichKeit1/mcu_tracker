from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.models import MarathonItem, Progress
from app.repositories.base import BaseRepository
from app.schemas.progress import ProgressCreate, ProgressUpdate

class ProgressRepository(BaseRepository[Progress]):
    def __init__(self, db: Session) -> None:
        super().__init__(Progress, db)

    def get_by_content(self, content_id: int) -> Progress | None:
        return (
            self.db.query(Progress)
            .filter(Progress.content_id == content_id)
            .first()
        )

    def list_by_marathon(self, marathon_id: int) -> list[Progress]:
        """Return all progress rows for content belonging to a marathon,
        including episode-level content (children of series)."""
        from app.models.models import Content

        # Direct content_ids from marathon items (series, movies, etc.)
        direct_ids = (
            self.db.query(MarathonItem.content_id)
            .filter(MarathonItem.marathon_id == marathon_id)
            .scalar_subquery()
        )
        # Episode content_ids: children whose parent is in the marathon
        episode_ids = (
            self.db.query(Content.id)
            .filter(Content.parent_id.in_(direct_ids))
            .scalar_subquery()
        )
        return (
            self.db.query(Progress)
            .filter(
                Progress.content_id.in_(direct_ids)
                | Progress.content_id.in_(episode_ids)
            )
            .all()
        )

    def upsert(self, schema: ProgressCreate) -> Progress:
        """Create or update a progress row for a given content_id."""
        obj = self.get_by_content(schema.content_id)
        if obj is None:
            obj = Progress(
                content_id=schema.content_id,
                watched=schema.watched,
                watched_at=datetime.now(timezone.utc) if schema.watched else None,
            )
            self.db.add(obj)
        else:
            obj.watched = schema.watched
            obj.watched_at = datetime.now(timezone.utc) if schema.watched else None
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, id: int, schema: ProgressUpdate) -> Progress | None:
        obj = self.get(id)
        if not obj:
            return None
        data = schema.model_dump(exclude_unset=True)
        if "watched" in data and data["watched"] and not obj.watched_at:
            obj.watched_at = datetime.now(timezone.utc)
        for field, value in data.items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj