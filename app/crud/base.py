from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User


class BaseCRUD:
    def __init__(self, model):
        self.model = model

    async def get(
            self, obj_id: int,
            session: AsyncSession):
        obj_model = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return obj_model.scalars().first()

    async def get_multi(
        self, session: AsyncSession
    ):
        objs_db = await session.execute(select(self.model))
        return objs_db.scalars().all()

    async def create(
        self,
        obj_schema,
        session: AsyncSession,
        user: Optional[User] = None,
    ):
        obj_schema_data = obj_schema.dict()
        if user is not None:
            obj_schema_data['user_id'] = user.id
        db_obj = self.model(**obj_schema_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_model,
        update_schema,
        session: AsyncSession
    ):
        db_model_data = jsonable_encoder(db_model)
        update_schema_data = update_schema.dict(exclude_unset=True)
        for field in db_model_data:
            if field in update_schema_data:
                setattr(db_model, field, update_schema_data[field])
        if db_model.full_amount == db_model.invested_amount:
            db_model.fully_invested = True
            db_model.close_date = datetime.now()
        session.add(db_model)
        await session.commit()
        await session.refresh(db_model)
        return db_model

    async def remove(
        self,
        obj_model: int,
        session: AsyncSession
    ):
        await session.delete(obj_model)
        await session.commit()
        return obj_model
