from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.charity_project import CharityProjectDB
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud


router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB]
)
def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    all_charity_projects = charity_project_crud.get_multi(session)
    return all_charity_projects


@router.post('/')
def create_charity_project():
    return {}


@router.delete('/{project_id}')
def delete_charity_project(project_id):
    return {}


@router.patch('/{project_id}')
def update_charity_project(project_id):
    return {}
