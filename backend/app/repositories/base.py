from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from app.database.session import Base

ModelT = TypeVar("ModelT", bound=Base)

class BaseRepository(Generic[ModelT]):
    def __init__(self, model: type[ModelT], db: Session) -> None:
        self.model = model
        self.db = db

    def get(self, id: int) -> ModelT | None:
        return self.db.get(self.model, id)

    def list(self, skip: int = 0, limit: int = 100) -> list[ModelT]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj: ModelT) -> ModelT:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: int) -> bool:
        obj = self.get(id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True