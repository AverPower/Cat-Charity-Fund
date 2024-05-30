from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donation import crud_donation
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationAdminDB
)
from app.models.user import User
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
    """
    Только для суперюзеров.

    Получает список всех пожертвований.
    """
    all_donations = await crud_donation.get_multi(session)
    return all_donations


@router.post(
    '/',
    response_model=DonationDB,
)
async def create_donation(
    donation_obj: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Сделать пожертвование.

    """
    new_donation = await crud_donation.create(
        donation_obj,
        session,
        user
    )
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Получить список моих пожертвований.
    """
    user_donations = await crud_donation.get_user_donations(session, user)
    return user_donations
