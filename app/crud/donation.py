from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.schemas.donation import DonationCreate, DonationDB


class CRUDDonation(
    CRUDBase[
        Donation,
        DonationCreate,
        DonationDB
    ]
):
    ...


crud_donation = CRUDDonation(Donation)
