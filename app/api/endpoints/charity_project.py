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
from app.services.donation import donate_calculation


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
    opened_donations = await crud_donation.get_opened_donations(session)
    new_info = None
    if opened_donations:
        ids = [info[0] for info in opened_donations]
        donate_info = [(info[1], info[2]) for info in opened_donations]
        project_sum = charity_project_data.full_amount
        left_sum, updated_donate_info = donate_calculation(project_sum, donate_info)
        new_info = {'invested_amount': project_sum - left_sum}
        for data in zip(ids, updated_donate_info):
            update_donate = await crud_donation.get(data[0], session)
            await crud_donation.update_invested_amount(
                update_donate,
                data[1][1],
                session
            )

    new_charity_project = await charity_project_crud.create(
        charity_project_data,
        session,
        new_info=new_info
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
    # TODO - get project by id
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
    # TODO - get project by id
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
