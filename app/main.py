from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.v1.auth import router as auth_router
from app.api.v1.companies import router as companies_router
from app.core.config import settings
from app.database.base import Base
from app.database.session import engine
from app.models.company import Company
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(companies_router)


@app.get("/")
def root():
    return {
        "message": "AI Finance Controller Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/db-test")
def db_test():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))

        return {
            "database": "connected",
            "result": result.scalar(),
        }


@app.get("/debug-routes")
def debug_routes():
    routes = []

    for route in app.routes:
        routes.append(str(route))

    return routes


@app.get("/tables")
def tables():
    return {
        "tables": list(Base.metadata.tables.keys())
    }