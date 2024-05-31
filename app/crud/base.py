from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from app.core.db import Base
from app.models.user import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ) -> Optional[ModelType]:
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ) -> List[ModelType]:
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in: CreateSchemaType,
            session: AsyncSession,
            user: Optional[User] = None,
            invested_amount: Optional[int] = None
    ):
        obj_in_data = obj_in.dict()

        if user is not None:
            obj_in_data['user_id'] = user.id

        db_obj = self.model(**obj_in_data)
        if invested_amount is not None:
            self.update_object(db_obj, invested_amount)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj: ModelType,
            obj_in: UpdateSchemaType,
            session: AsyncSession,
    ) -> ModelType:
        if db_obj.fully_invested:
            raise HTTPException(
                status_code=404,
                detail='Нельзя редактировать закрытый проект!'
            )
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj: ModelType,
            session: AsyncSession,
    ) -> ModelType:
        if db_obj.invested_amount:
            db_obj.fully_invested = True
            session.add()
            await session.commit()
            await session.refresh(db_obj)
            return db_obj
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def update_invested_amount(
            self,
            obj_id: int,
            invested_amount: int,
            session: AsyncSession,
    ) -> ModelType:
        db_obj = await self.get(obj_id, session)
        db_obj = self.update_object(db_obj, invested_amount)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    @staticmethod
    def update_object(db_obj: ModelType, invested_amount: int):
        setattr(db_obj, 'invested_amount', invested_amount)
        if db_obj.full_amount == db_obj.invested_amount:
            db_obj.fully_invested = True
            db_obj.close_date = func.now()
        return db_obj

    async def get_user_objects(
        self,
        session: AsyncSession,
        user: User
    ):
        objects = await session.execute(
            select(ModelType).where(
                ModelType.user_id == User.id
            )
        )
        objects = objects.scalars().all()
        return objects

    async def get_opened_objects(
        self,
        session: AsyncSession
    ) -> list[Optional[ModelType]]:
        opened_objects = await session.execute(
            select(
                self.model.id,
                self.model.full_amount,
                self.model.invested_amount,
            ).where(
                self.model.fully_invested == 0
            ).order_by(self.model.create_date.asc())
        )
        opened_objects = opened_objects.all()
        return opened_objects
