from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from app.config import settings

_cors_origins = ["*"] if settings.ENV == "development" else []

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


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}