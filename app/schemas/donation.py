from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class DonationCreate(BaseModel):
    full_amount: int = Field(min_length=0)
    comment: Optional[str] = None


class DonationDB(DonationCreate):
    id: int
    create_date: datetime


class DonationAdminDB(DonationDB):
    user_id: str
    invested_amount: int
    fully_invested: bool
    close_date: str
