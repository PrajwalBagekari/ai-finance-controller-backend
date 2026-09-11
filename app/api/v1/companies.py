from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate
from app.schemas.company import CompanyResponse

router = APIRouter(
    prefix="/api/v1/companies",
    tags=["Companies"],
)


@router.post(
    "",
    response_model=CompanyResponse,
)
def create_company(
    payload: CompanyCreate,
    db: Session = Depends(get_db),
):
    existing_company = (
        db.query(Company)
        .filter(Company.gstin == payload.gstin)
        .first()
    )

    if existing_company:
        raise HTTPException(
            status_code=400,
            detail="GSTIN already exists",
        )

    company = Company(
        name=payload.name,
        legal_name=payload.legal_name,
        gstin=payload.gstin,
        currency=payload.currency,
        fiscal_year_start=payload.fiscal_year_start,
        fiscal_year_end=payload.fiscal_year_end,
        status=payload.status,
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    return company


@router.get(
    "",
    response_model=list[CompanyResponse],
)
def get_companies(
    db: Session = Depends(get_db),
):
    return db.query(Company).all()
@router.get(
    "/{company_id}",
    response_model=CompanyResponse,
)
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
):
    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    return company


@router.put(
    "/{company_id}",
    response_model=CompanyResponse,
)
def update_company(
    company_id: int,
    payload: CompanyCreate,
    db: Session = Depends(get_db),
):
    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    company.name = payload.name
    company.legal_name = payload.legal_name
    company.gstin = payload.gstin
    company.currency = payload.currency
    company.fiscal_year_start = payload.fiscal_year_start
    company.fiscal_year_end = payload.fiscal_year_end
    company.status = payload.status

    db.commit()
    db.refresh(company)

    return company


@router.delete("/{company_id}")
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
):
    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    db.delete(company)
    db.commit()

    return {
        "message": "Company deleted successfully"
    }