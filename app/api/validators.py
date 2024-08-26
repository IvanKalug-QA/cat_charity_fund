from typing import Optional
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import CharityProject


async def check_exists_object(
    obj_id: int, crud_operation, session: AsyncSession
):
    obj_db = await crud_operation.get(obj_id, session)
    if obj_db is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Object does not exist!'
        )
    return obj_db


async def check_project_before_edit(
    obj_db, update_schema
) -> None:
    if obj_db.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Project closed!'
        )
    if (update_schema.full_amount is not None and
            update_schema.full_amount < obj_db.invested_amount):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='The amount must be more than the donated funds'
        )


async def check_project_before_remove(obj_db) -> None:
    if obj_db.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='In project has money!'
        )


async def check_unique_name_project(
    schema, session: AsyncSession, project_id: Optional[int] = None
) -> None:
    if schema.name is None:
        return
    check_name = select(CharityProject.name).where(
        CharityProject.name == schema.name)
    if project_id:
        check_name = check_name.where(
            CharityProject.id != project_id
        )
    check_name = await session.execute(check_name)
    check_name = check_name.scalars().first()
    if check_name is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Name exist!'
        )