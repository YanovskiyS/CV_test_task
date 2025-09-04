from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import insert, select, update, delete


class BaseRepository:
    model =None
    schema = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filtered_by):
        query = select(self.model).filter(*filter).filter_by(**filtered_by)
        result = await self.session.execute(query)
        return [
            self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()
        ]

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except:
            raise HTTPException(status_code=402, detail="Not found")
        return model

    async def edit(
            self, data: BaseModel, exclude_unset: bool = False, **filter_by
    ) -> None:
        product_update = (
            update(self.model)
            .filter_by(**filter_by)
            .values(data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(product_update)

    async def delete(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)