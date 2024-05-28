from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    full_amount: Optional[int] = Field(None, gt=0)


class CharityProjectCreate(BaseModel):
    name: str = Field(max_length=100)
    description: str
    full_amount: int = Field(gt=0)


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None
