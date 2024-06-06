from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate
from app.models.charity_project import CharityProject


class CRUDCharityProject(
    CRUDBase[
        CharityProject,
        CharityProjectCreate,
        CharityProjectUpdate
    ]
):
    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ):
        closed_projects = await session.execute(
            select(
                CharityProject
            ).where(
                CharityProject.fully_invested == 1
            ).order_by(
                CharityProject.close_date - CharityProject.create_date
            )
        )
        return closed_projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
