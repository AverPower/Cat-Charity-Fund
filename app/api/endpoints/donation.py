from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def get_all_donations():
    return {}


@router.post('/')
async def create_donation():
    return {}


@router.get('/my')
async def get_user_donations():
    return {}
