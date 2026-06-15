from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import Progress
from app.repositories.content import ContentRepository
from app.repositories.marathon_item import MarathonItemRepository
from app.repositories.progress import ProgressRepository
from app.schemas.progress import ProgressCreate, ProgressUpdate, ProgressOut, StatsOut

class ProgressService:
    def __init__(self, db: Session) -> None:
        self.repo = ProgressRepository(db)
        self.content_repo = ContentRepository(db)
        self.item_repo = MarathonItemRepository(db)

    def list(self, marathon_id: int) -> list[Progress]:
        return self.repo.list_by_marathon(marathon_id)

    def upsert(self, schema: ProgressCreate) -> Progress:
        if not self.content_repo.get(schema.content_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Content {schema.content_id} not found",
            )
        return self.repo.upsert(schema)

    def update(self, id: int, schema: ProgressUpdate) -> Progress:
        obj = self.repo.update(id, schema)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Progress {id} not found",
            )
        return obj

    def get_stats(self, marathon_id: int) -> StatsOut:
        items = self.item_repo.list_by_marathon(marathon_id)
        if not items:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Marathon {marathon_id} not found or has no items",
            )

        progress_rows = {p.content_id: p for p in self.repo.list_by_marathon(marathon_id)}

        completed = 0
        hours_watched: float = 0.0
        hours_remaining: float = 0.0

        for item in items:
            runtime_hours = (item.content.runtime or 0) / 60
            p = progress_rows.get(item.content_id)
            if p and p.watched:
                completed += 1
                hours_watched += runtime_hours
            else:
                hours_remaining += runtime_hours

        total = len(items)
        remaining = total - completed
        percentage = round((completed / total) * 100, 1) if total else 0.0

        return StatsOut(
            completed=completed,
            remaining=remaining,
            percentage=percentage,
            hours_watched=round(hours_watched, 1),
            hours_remaining=round(hours_remaining, 1),
        )