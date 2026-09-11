from datetime import date
from datetime import datetime

from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str
    legal_name: str
    gstin: str
    currency: str = "INR"
    fiscal_year_start: date | None = None
    fiscal_year_end: date | None = None
    status: str = "Active"


class CompanyUpdate(BaseModel):
    name: str
    legal_name: str
    gstin: str
    currency: str
    fiscal_year_start: date | None = None
    fiscal_year_end: date | None = None
    status: str


class CompanyResponse(BaseModel):
    id: int
    name: str
    legal_name: str
    gstin: str
    currency: str
    fiscal_year_start: date | None
    fiscal_year_end: date | None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True