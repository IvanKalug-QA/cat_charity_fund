from typing import Optional
from datetime import datetime

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    pass


class DonationAllDb(DonationBase):
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True