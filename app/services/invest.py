from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase, CreateSchemaType, ModelType
from app.core.user import User


def donate_calculation(
    left_money: int,
    sources: list[tuple[int, int]]
):
    update_amounts = []
    for source in sources:
        donation = min(left_money, source[0] - source[1])
        left_money -= donation
        update_amounts.append(source[1] + donation)
        if not left_money:
            break
    return left_money, update_amounts


async def invest(
    crud_create: CRUDBase,
    crud_update: CRUDBase,
    obj_data: CreateSchemaType,
    session: AsyncSession,
    user: User
) -> ModelType:
    opened_objects = await crud_update.get_opened_objects(session)
    invested_amount = None
    if opened_objects:
        opened_objects_ids = [info[0] for info in opened_objects]
        objects_info = [(info[1], info[2]) for info in opened_objects]
        full_amount = obj_data.full_amount
        left_sum, updated_objects_info = donate_calculation(full_amount, objects_info)
        invested_amount = full_amount - left_sum
        for data in zip(opened_objects_ids, updated_objects_info):
            await crud_update.update_invested_amount(
                obj_id=data[0],
                invested_amount=data[1],
                session=session
            )
    new_object = await crud_create.create(
        obj_data,
        session,
        user=user,
        invested_amount=invested_amount
    )
    return new_object
