from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charityproject import (
    CharityProjectDB,
    CharityProjectCreate,
    CharityProjectUpdate)
from app.crud.charityproject import charity_project_crud
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
    return await charity_project_crud.get_multi(session)


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
    charity_project = await charity_project_crud.create(
        create_schema, session
    )
    await investing(session)
    await session.refresh(charity_project)
    return charity_project


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
    charity_project = await check_exists_object(
        project_id, charity_project_crud, session)
    await check_unique_name_project(
        update_schema,
        session,
        charity_project.id)
    await check_project_before_edit(charity_project, update_schema)
    charity_project = await charity_project_crud.update(
        charity_project, update_schema, session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)])
async def remove_charityproject(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_exists_object(
        project_id, charity_project_crud, session)
    await check_project_before_remove(charity_project)
    charity_project = await charity_project_crud.remove(
        charity_project, session)
    return charity_project