from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donation import donation_crud
from app.core.db import get_async_session
from app.schemas.donation import DonationAllDb, DonationCreate
from app.core.user import current_superuser, current_user
from app.models import User
from app.services.transactions import investing

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationAllDb],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)])
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationAllDb,
    response_model_exclude_none=True,
    response_model_exclude={
        'invested_amount', 'fully_invested',
        'close_date', 'user_id'})
async def create_donation(
    create_schema: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    donation = await donation_crud.create(
        create_schema, session, user)
    await investing(session)
    await session.refresh(donation)
    return donation


@router.get(
    '/my',
    response_model=list[DonationAllDb],
    response_model_exclude_none=True,
    response_model_exclude={
        'user_id', 'invested_amount',
        'fully_invested', 'close_date'})
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_user_donations(
        user, session
    )