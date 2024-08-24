from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charityproject import (
    CharityProjectDB,
    CharityProjectCreate,
    CharityProjectUpdate)
from app.crud.charityproject import charityproject_crud
from app.api.validators import (
    check_exists_object,
    check_project_before_remove,
    check_project_before_edit,
    check_unique_name_project)
from app.services.transactions import investing

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB])
async def get_all_charityprojects(
        session: AsyncSession = Depends(get_async_session)):
    charityprojects = await charityproject_crud.get_multi(session)
    return charityprojects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)])
async def create_charityproject(
    create_schema: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_unique_name_project(create_schema, session)
    charityproject = await charityproject_crud.create(
        create_schema, session
    )
    await investing(session)
    await session.refresh(charityproject)
    return charityproject


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)])
async def update_charityproject(
    project_id: int,
    update_schema: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    charityproject = await check_exists_object(
        project_id, charityproject_crud, session)
    await check_unique_name_project(
        update_schema,
        session,
        charityproject.id)
    await check_project_before_edit(charityproject, update_schema)
    charityproject = await charityproject_crud.update(
        charityproject, update_schema, session
    )
    return charityproject


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)])
async def remove_charityproject(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    charityproject = await check_exists_object(
        project_id, charityproject_crud, session)
    await check_project_before_remove(charityproject)
    charityproject = await charityproject_crud.remove(
        charityproject, session)
    return charityproject