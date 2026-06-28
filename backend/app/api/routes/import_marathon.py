"""
Marathon import routes.

POST /import/preview  — upload file (.txt/.csv/.xlsx), return matched items preview
POST /import/confirm  — create marathon from confirmed preview
GET  /contents/search — search content by title (for manual add)
"""
from __future__ import annotations

import io
import csv

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.models import Content, ContentType, Era, Marathon, MarathonItem, Universe
from app.schemas.content import ContentOut
from app.schemas.marathon import MarathonOut

router = APIRouter(tags=["import"])


# ---------------------------------------------------------------------------
# Content search
# ---------------------------------------------------------------------------

@router.get("/contents/search", response_model=list[ContentOut])
def search_contents(
    q: str,
    db: Session = Depends(get_db),
) -> list[Content]:
    """Search content by title (case-insensitive, partial match).
    Excludes episode rows (type=episode) — only top-level content.
    """
    if not q or len(q) < 2:
        return []
    return (
        db.query(Content)
        .filter(
            Content.title.ilike(f"%{q}%"),
            Content.type != ContentType.episode,
            Content.parent_id.is_(None),
        )
        .order_by(Content.title)
        .limit(20)
        .all()
    )


# ---------------------------------------------------------------------------
# Import preview
# ---------------------------------------------------------------------------

class PreviewItem:
    def __init__(
        self,
        *,
        line: int,
        raw: str,
        content_id: int | None,
        title: str,
        type: str | None,
        runtime: int | None,
        matched: bool,
    ) -> None:
        self.line = line
        self.raw = raw
        self.content_id = content_id
        self.title = title
        self.type = type
        self.runtime = runtime
        self.matched = matched

    def to_dict(self) -> dict:
        return {
            "line": self.line,
            "raw": self.raw,
            "content_id": self.content_id,
            "title": self.title,
            "type": self.type,
            "runtime": self.runtime,
            "matched": self.matched,
        }


def _parse_file(filename: str, data: bytes) -> list[str]:
    """Return a flat list of title strings from the uploaded file."""
    ext = filename.rsplit(".", 1)[-1].lower()

    if ext == "txt":
        text = data.decode("utf-8", errors="replace")
        return [line.strip() for line in text.splitlines() if line.strip()]

    if ext == "csv":
        text = data.decode("utf-8", errors="replace")
        reader = csv.reader(io.StringIO(text))
        titles = []
        for row in reader:
            if row:
                titles.append(row[0].strip())
        return [t for t in titles if t]

    if ext in ("xlsx", "xls"):
        try:
            import openpyxl
        except ImportError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="openpyxl not installed — cannot parse .xlsx files",
            )
        wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True)
        ws = wb.active
        titles = []
        for row in ws.iter_rows(values_only=True):
            if row and row[0]:
                titles.append(str(row[0]).strip())
        return [t for t in titles if t]

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=f"Unsupported file type: .{ext}. Use .txt, .csv or .xlsx",
    )


def _match_title(title: str, db: Session) -> Content | None:
    """Exact match first, then case-insensitive, then partial."""
    # Exact
    c = db.query(Content).filter(
        Content.title == title,
        Content.parent_id.is_(None),
    ).first()
    if c:
        return c
    # Case-insensitive
    c = db.query(Content).filter(
        Content.title.ilike(title),
        Content.parent_id.is_(None),
    ).first()
    if c:
        return c
    # Partial — only if unambiguous
    results = (
        db.query(Content)
        .filter(
            Content.title.ilike(f"%{title}%"),
            Content.parent_id.is_(None),
        )
        .all()
    )
    if len(results) == 1:
        return results[0]
    return None


@router.post("/import/preview")
async def import_preview(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> dict:
    """Parse uploaded file and return preview with match status for each line."""
    data = await file.read()
    try:
        titles = _parse_file(file.filename or "upload.txt", data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Could not parse file: {e}",
        )

    items = []
    for i, raw in enumerate(titles, start=1):
        content = _match_title(raw, db)
        items.append(
            PreviewItem(
                line=i,
                raw=raw,
                content_id=content.id if content else None,
                title=content.title if content else raw,
                type=content.type.value if content else None,
                runtime=content.runtime if content else None,
                matched=content is not None,
            ).to_dict()
        )

    matched = sum(1 for it in items if it["matched"])
    return {
        "total": len(items),
        "matched": matched,
        "unmatched": len(items) - matched,
        "items": items,
    }


# ---------------------------------------------------------------------------
# Import confirm — create marathon from preview
# ---------------------------------------------------------------------------

class ConfirmItem:
    content_id: int
    title: str
    canonical: bool = True


from pydantic import BaseModel


class ConfirmItemIn(BaseModel):
    content_id: int | None = None
    title: str
    canonical: bool = True


class ImportConfirmIn(BaseModel):
    name: str
    description: str | None = None
    universe_id: int
    items: list[ConfirmItemIn]


@router.post("/import/confirm", response_model=MarathonOut, status_code=status.HTTP_201_CREATED)
def import_confirm(
    body: ImportConfirmIn,
    db: Session = Depends(get_db),
) -> Marathon:
    """Create a marathon from a confirmed import list.

    Items with content_id=None are created as new Content rows (movie type by default).
    """
    if not body.items:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Marathon must have at least one item",
        )

    universe = db.query(Universe).filter(Universe.id == body.universe_id).first()
    if not universe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Universe {body.universe_id} not found",
        )

    # Create marathon
    marathon = Marathon(
        universe_id=body.universe_id,
        name=body.name,
        description=body.description,
    )
    db.add(marathon)
    db.flush()

    # Create a default era for manually-imported marathons
    default_era = Era(
        marathon_id=marathon.id,
        name="Geral",
        position=1,
    )
    db.add(default_era)
    db.flush()

    # Create marathon items
    for position, item in enumerate(body.items, start=1):
        content_id = item.content_id

        # If no match, create a stub Content
        if content_id is None:
            stub = Content(
                title=item.title,
                type=ContentType.movie,
            )
            db.add(stub)
            db.flush()
            content_id = stub.id

        db.add(MarathonItem(
            marathon_id=marathon.id,
            content_id=content_id,
            era_id=default_era.id,
            position=position,
            canonical=item.canonical,
        ))

    db.commit()
    db.refresh(marathon)
    return marathon