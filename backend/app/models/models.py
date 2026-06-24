from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.session import Base

class ContentType(PyEnum):
    movie = "movie"
    series = "series"
    episode = "episode"
    special = "special"
    one_shot = "one_shot"

class Universe(Base):
    __tablename__ = "universe"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    marathons: Mapped[list["Marathon"]] = relationship(
        "Marathon", back_populates="universe", cascade="all, delete-orphan"
    )

class Marathon(Base):
    __tablename__ = "marathon"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    universe_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("universe.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    universe: Mapped["Universe"] = relationship("Universe", back_populates="marathons")
    eras: Mapped[list["Era"]] = relationship(
        "Era", back_populates="marathon", cascade="all, delete-orphan"
    )
    items: Mapped[list["MarathonItem"]] = relationship(
        "MarathonItem", back_populates="marathon", cascade="all, delete-orphan"
    )

class Era(Base):
    __tablename__ = "era"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    marathon_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("marathon.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("marathon_id", "position", name="uq_era_marathon_position"),
    )

    marathon: Mapped["Marathon"] = relationship("Marathon", back_populates="eras")
    items: Mapped[list["MarathonItem"]] = relationship(
        "MarathonItem", back_populates="era"
    )

class Content(Base):
    __tablename__ = "content"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tmdb_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    type: Mapped[ContentType] = mapped_column(
        Enum(ContentType), nullable=False
    )
    poster_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    release_date: Mapped[str | None] = mapped_column(String(20), nullable=True)
    runtime: Mapped[int | None] = mapped_column(Integer, nullable=True)  # minutes
    episode_number: Mapped[int | None] = mapped_column(Integer, nullable=True)  # position within season
    parent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("content.id", ondelete="CASCADE"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Self-referential: season → episodes
    episodes: Mapped[list["Content"]] = relationship(
        "Content",
        back_populates="parent",
        cascade="all, delete-orphan",
        order_by="Content.episode_number",
        foreign_keys="Content.parent_id",
    )
    parent: Mapped["Content | None"] = relationship(
        "Content",
        back_populates="episodes",
        remote_side="Content.id",
        foreign_keys="Content.parent_id",
    )

    marathon_items: Mapped[list["MarathonItem"]] = relationship(
        "MarathonItem", back_populates="content"
    )
    progress: Mapped[list["Progress"]] = relationship(
        "Progress", back_populates="content", cascade="all, delete-orphan"
    )

class MarathonItem(Base):
    __tablename__ = "marathon_item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    marathon_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("marathon.id", ondelete="CASCADE"), nullable=False
    )
    content_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("content.id", ondelete="CASCADE"), nullable=False
    )
    era_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("era.id", ondelete="SET NULL"), nullable=True
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    canonical: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    __table_args__ = (
        UniqueConstraint(
            "marathon_id", "position", name="uq_marathon_item_position"
        ),
    )

    marathon: Mapped["Marathon"] = relationship("Marathon", back_populates="items")
    content: Mapped["Content"] = relationship("Content", back_populates="marathon_items")
    era: Mapped["Era | None"] = relationship("Era", back_populates="items")
    progress: Mapped["Progress | None"] = relationship(
        "Progress",
        primaryjoin="and_(MarathonItem.content_id == foreign(Progress.content_id))",
        viewonly=True,
        uselist=False,
    )

class Progress(Base):
    __tablename__ = "progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("content.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    watched: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    watched_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    content: Mapped["Content"] = relationship("Content", back_populates="progress")