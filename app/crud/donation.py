from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseCRUD
from app.models import Donation, User


class DonationCRUD(BaseCRUD):
    async def get_user_donations(
        self,
        user: User,
        session: AsyncSession
    ):
        user_donations = await session.execute(
            select(self.model).where(
                self.model.user_id == user.id
            )
        )
        return user_donations.scalars().all()


donation_crud = DonationCRUD(Donation)