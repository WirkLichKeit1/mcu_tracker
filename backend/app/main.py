from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from app.config import settings
from app.api.routes import universes, marathons, eras, contents, marathon_items, progress

if settings.ENV == "development":
    _cors_origins = ["*"]
else:
    _cors_origins = [settings.FRONTEND_URL]

app = FastAPI(
    title="MCU Tracker",
    description="Track your MCU marathon progress",
    version="0.1.0",
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=_cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ],
)

app.include_router(universes.router)
app.include_router(marathons.router)
app.include_router(eras.router)
app.include_router(contents.router)
app.include_router(marathon_items.router)
app.include_router(progress.router)

@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}