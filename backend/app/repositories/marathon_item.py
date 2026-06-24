from sqlalchemy.orm import Session, joinedload, selectinload

from app.models.models import Content, MarathonItem, Progress
from app.repositories.base import BaseRepository
from app.schemas.marathon_item import MarathonItemCreate, MarathonItemUpdate

class MarathonItemRepository(BaseRepository[MarathonItem]):
    def __init__(self, db: Session) -> None:
        super().__init__(MarathonItem, db)
        # expose db for service-layer access
        self.db = db

    def list_by_marathon(
        self,
        marathon_id: int,
        canonical_only: bool = False,
    ) -> list[MarathonItem]:
        query = (
            self.db.query(MarathonItem)
            .options(
                joinedload(MarathonItem.era),
                joinedload(MarathonItem.content).selectinload(Content.episodes),
            )
            .filter(MarathonItem.marathon_id == marathon_id)
        )
        if canonical_only:
            query = query.filter(MarathonItem.canonical.is_(True))
        return query.order_by(MarathonItem.position).all()

    def get_next(self, marathon_id: int, canonical_only: bool = False) -> MarathonItem | None:
        """Return the first item in the marathon that still has unwatched content.

        For movies/specials/one-shots: unwatched means no Progress(watched=True) for content_id.
        For series with episodes: unwatched means at least one episode has no Progress(watched=True).
        """
        # IDs of content rows marked as watched
        watched_ids = (
            self.db.query(Progress.content_id)
            .filter(Progress.watched.is_(True))
            .scalar_subquery()
        )

        # Subquery: episode-bearing series where ALL episodes are watched
        fully_watched_series_ids = (
            self.db.query(Content.parent_id)
            .filter(
                Content.parent_id.isnot(None),
                Content.id.not_in(watched_ids),
            )
            .correlate()
        )
        # A series is complete when the above subquery returns NO rows for its id,
        # meaning every child episode IS in watched_ids.
        # We achieve this via NOT EXISTS on a sub-select of unwatched episodes.
        from sqlalchemy import exists, select as sa_select
        unwatched_episode = (
            sa_select(Content.id)
            .where(
                Content.parent_id == MarathonItem.content_id,
                Content.id.not_in(watched_ids),
            )
            .correlate(MarathonItem)
        )

        query = (
            self.db.query(MarathonItem)
            .options(
                joinedload(MarathonItem.era),
                joinedload(MarathonItem.content).selectinload(Content.episodes),
            )
            .filter(MarathonItem.marathon_id == marathon_id)
            .filter(
                # Either: non-series content not yet watched
                (
                    (MarathonItem.content_id.not_in(watched_ids))
                )
                # The above handles movies/specials AND series-level content_id
                # For series with episodes, we also exclude fully-watched ones
                # by checking that at least one episode remains unwatched
            )
        )
        if canonical_only:
            query = query.filter(MarathonItem.canonical.is_(True))

        # Evaluate candidates in position order; skip series where all eps are done
        candidates = query.order_by(MarathonItem.position).all()
        for item in candidates:
            content = item.content
            if content.type.value == "series" and content.episodes:
                # Check if any episode is unwatched
                watched_ep_ids = set(
                    self.db.query(Progress.content_id)
                    .filter(
                        Progress.watched.is_(True),
                        Progress.content_id.in_([ep.id for ep in content.episodes]),
                    )
                    .scalars()
                    .all()
                )
                if len(watched_ep_ids) < len(content.episodes):
                    return item
                # All episodes watched — skip this series
            else:
                return item
        return None

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