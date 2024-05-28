from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def get_all_donations():
    return {}


@router.post('/')
def create_donation():
    return {}


@router.get('/my')
def get_user_donations():
    return {}
