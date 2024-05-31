from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.charity_project import (
    CharityProjectDB,
    CharityProjectCreate,
    CharityProjectUpdate
)
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.crud.donation import crud_donation
from app.core.user import current_superuser
from app.services.invest import invest


router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB]
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Получает список всех проектов.
    """
    all_charity_projects = await charity_project_crud.get_multi(session)
    return all_charity_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project_data: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.

    Создает благотворительный проект.
    """
    new_charity_project = await invest(
        charity_project_crud,
        crud_donation,
        charity_project_data,
        session
    )
    return new_charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.

    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы средства, его можно только закрыть.
    """
    charity_project_to_delete = await charity_project_crud.get(
        project_id,
        session
    )
    deleted_charity_project = await charity_project_crud.remove(
        charity_project_to_delete,
        session
    )
    return deleted_charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.

    Закрытый проект нельзя редактировать, также нельзя установить требуемую сумму меньше уже вложенной.
    """
    charity_project_to_update = await charity_project_crud.get(
        project_id,
        session
    )
    updated_charity_project = await charity_project_crud.update(
        charity_project_to_update,
        obj_in,
        session
    )
    return updated_charity_project
