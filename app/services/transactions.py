from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Donation, CharityProject


async def investing(
    session: AsyncSession
):
    all_projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested.is_(False)
        )
    )
    all_projects = all_projects.scalars().all()
    all_donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested.is_(False)
        )
    )
    all_donations = all_donations.scalars().all()
    if not all_projects or not all_projects:
        return
    idx_donation = 0
    idx_project = 0
    while idx_donation < len(all_donations) and idx_project < len(
            all_projects):
        amount_need = all_projects[
            idx_project].full_amount - all_projects[
                idx_project].invested_amount
        if all_donations[idx_donation].full_amount - all_donations[
                idx_donation].invested_amount <= amount_need:
            all_projects[idx_project].invested_amount += (
                all_donations[
                    idx_donation].full_amount - all_donations[
                        idx_donation].invested_amount)
            all_donations[idx_donation].invested_amount = all_donations[
                idx_donation].full_amount
            if all_projects[idx_project].invested_amount == all_projects[
                    idx_project].full_amount:
                all_projects[idx_project].fully_invested = True
                all_projects[idx_project].close_date = datetime.now()
                session.add(all_projects[idx_project])
                idx_project += 1
            all_donations[idx_donation].fully_invested = True
            all_donations[idx_donation].close_date = datetime.now()
            session.add(all_donations[idx_donation])
            idx_donation += 1
        else:
            all_donations[idx_donation].invested_amount += amount_need
            all_projects[idx_project].invested_amount = all_projects[
                idx_project].full_amount
            all_projects[idx_project].fully_invested = True
            all_projects[idx_project].close_date = datetime.now()
            session.add(all_projects[idx_project])
            idx_project += 1
    await session.commit()