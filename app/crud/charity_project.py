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
    ...


charity_project_crud = CRUDCharityProject(CharityProject)
