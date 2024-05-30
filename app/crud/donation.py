from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models import (
    Donation,
    User
)
from app.schemas.donation import DonationCreate, DonationDB


class CRUDDonation(
    CRUDBase[
        Donation,
        DonationCreate,
        DonationDB
    ]
):
    async def get_opened_donations(
        self,
        session: AsyncSession
    ) -> list[Optional[Donation]]:
        opened_donations = await session.execute(
            select(
                Donation.id,
                Donation.full_amount,
                Donation.invested_amount,
            ).where(
                Donation.fully_invested == 0
            ).order_by(Donation.create_date.asc())
        )
        opened_donations = opened_donations.all()
        return opened_donations

    async def get_user_donations(
        self,
        session: AsyncSession,
        user: User
    ):
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == User.id
            )
        )
        donations = donations.scalars().all()
        return donations


crud_donation = CRUDDonation(Donation)
