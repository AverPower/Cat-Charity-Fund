from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donation import crud_donation
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationAdminDB
)
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationAdminDB],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    all_donations = await crud_donation.get_multi(session)
    return all_donations


@router.post(
    '/',
    response_model=DonationDB,
    dependencies=[Depends(current_user)]
)
async def create_donation(
    donation_obj: DonationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    new_donation = await crud_donation.create(
        donation_obj,
        session
    )
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
    dependencies=[Depends(current_user)]
)
async def get_user_donations():
    return {}
