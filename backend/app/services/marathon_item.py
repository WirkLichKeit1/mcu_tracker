from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import MarathonItem
from app.repositories.content import ContentRepository
from app.repositories.era import EraRepository
from app.repositories.marathon import MarathonRepository
from app.repositories.marathon_item import MarathonItemRepository
from app.repositories.progress import ProgressRepository
from app.schemas.marathon_item import MarathonItemCreate, MarathonItemUpdate
from app.schemas.progress import NextItemOut

class MarathonItemService:
    def __init__(self, db: Session) -> None:
        self.repo = MarathonItemRepository(db)
        self.marathon_repo = MarathonRepository(db)
        self.content_repo = ContentRepository(db)
        self.era_repo = EraRepository(db)

    def list(
        self,
        marathon_id: int,
        canonical_only: bool = False,
    ) -> list[MarathonItem]:
        if not self.marathon_repo.get(marathon_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Marathon {marathon_id} not found",
            )
        return self.repo.list_by_marathon(marathon_id, canonical_only=canonical_only)

    def get(self, id: int) -> MarathonItem:
        obj = self.repo.get(id)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"MarathonItem {id} not found",
            )
        return obj

    def create(self, schema: MarathonItemCreate) -> MarathonItem:
        if not self.marathon_repo.get(schema.marathon_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Marathon {schema.marathon_id} not found",
            )
        if not self.content_repo.get(schema.content_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Content {schema.content_id} not found",
            )
        if schema.era_id and not self.era_repo.get(schema.era_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Era {schema.era_id} not found",
            )
        return self.repo.create(schema)

    def update(self, id: int, schema: MarathonItemUpdate) -> MarathonItem:
        if schema.era_id and not self.era_repo.get(schema.era_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Era {schema.era_id} not found",
            )
        obj = self.repo.update(id, schema)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"MarathonItem {id} not found",
            )
        return obj

    def delete(self, id: int) -> None:
        if not self.repo.delete(id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"MarathonItem {id} not found",
            )

    def get_next(self, marathon_id: int, canonical_only: bool = False) -> NextItemOut:
        if not self.marathon_repo.get(marathon_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Marathon {marathon_id} not found",
            )
        item = self.repo.get_next(marathon_id, canonical_only=canonical_only)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No unwatched items remaining in this marathon",
            )

        content = item.content

        # If this is a series with episodes, find the first unwatched episode
        if content.type.value == "series" and content.episodes:
            progress_repo = ProgressRepository(self.repo.db)
            progress_map = {
                p.content_id: p
                for p in progress_repo.list_by_marathon(marathon_id)
            }
            next_episode = None
            for ep in sorted(content.episodes, key=lambda e: e.episode_number or 0):
                ep_progress = progress_map.get(ep.id)
                if not ep_progress or not ep_progress.watched:
                    next_episode = ep
                    break

            if next_episode:
                return NextItemOut(
                    id=item.id,
                    content_id=next_episode.id,
                    title=f"{content.title} — {next_episode.title}",
                    type="episode",
                    position=item.position,
                    era=item.era.name if item.era else None,
                    poster_url=content.poster_url,
                    runtime=next_episode.runtime,
                    canonical=item.canonical,
                )

        # Movie, special, one-shot — or series without episodes seeded yet
        return NextItemOut(
            id=item.id,
            content_id=content.id,
            title=content.title,
            type=content.type.value,
            position=item.position,
            era=item.era.name if item.era else None,
            poster_url=content.poster_url,
            runtime=content.runtime,
            canonical=item.canonical,
        )