from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt, Field


class AbstractBase(BaseModel):
    full_amount: PositiveInt


class CharityProjectCreate(AbstractBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectCreate):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]


class CharityProjectDB(BaseModel):
    name: str
    description: str
    full_amount: int
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True