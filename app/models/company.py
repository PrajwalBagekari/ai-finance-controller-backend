from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.sql import func

from app.database.base import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)

    legal_name = Column(String(255), nullable=False)

    gstin = Column(String(50), unique=True, nullable=False)

    currency = Column(String(10), nullable=False, default="INR")

    fiscal_year_start = Column(Date, nullable=True)

    fiscal_year_end = Column(Date, nullable=True)

    status = Column(String(50), nullable=False, default="Active")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )