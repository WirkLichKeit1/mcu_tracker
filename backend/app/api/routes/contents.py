from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.models import Content, ContentType
from app.schemas.content import ContentCreate, ContentOut, ContentUpdate
from app.services.content import ContentService

router = APIRouter(prefix="/contents", tags=["contents"])

def get_service(db: Session = Depends(get_db)) -> ContentService:
    return ContentService(db)

@router.get("", response_model=list[ContentOut])
def list_contents(
    skip: int = 0,
    limit: int = 100,
    type: ContentType | None = None,
    service: ContentService = Depends(get_service),
) -> list[Content]:
    return service.list(skip=skip, limit=limit, type=type)

@router.get("/{id}", response_model=ContentOut)
def get_content(
    id: int,
    service: ContentService = Depends(get_service),
) -> Content:
    return service.get(id)

@router.post("", response_model=ContentOut, status_code=status.HTTP_201_CREATED)
def create_content(
    schema: ContentCreate,
    service: ContentService = Depends(get_service),
) -> Content:
    return service.create(schema)

@router.patch("/{id}", response_model=ContentOut)
def update_content(
    id: int,
    schema: ContentUpdate,
    service: ContentService = Depends(get_service),
) -> Content:
    return service.update(id, schema)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_content(
    id: int,
    service: ContentService = Depends(get_service),
) -> None:
    service.delete(id)