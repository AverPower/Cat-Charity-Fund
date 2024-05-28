from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def get_all_charity_projects():
    return {}


@router.post('/')
def create_charity_project():
    return {}


@router.delete('/{project_id}')
def delete_charity_project(project_id):
    return {}


@router.patch('/{project_id}')
def update_charity_project(project_id):
    return {}
