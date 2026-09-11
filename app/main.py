from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.database.base import Base
from app.database.session import engine
from app.api.v1.auth import router as auth_router
# Import models
from app.models.user import User
from app.models.company import Company
from app.api.v1.companies import router as companies_router
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(companies_router)

@app.get("/")
def root():
    return {"message": "AI Finance Controller Backend Running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/db-test")
def db_test():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        return {
            "database": "connected",
            "result": result.scalar(),
        }
@app.get("/debug-routes")
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