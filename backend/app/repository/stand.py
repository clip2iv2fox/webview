import math

from sqlalchemy import update, delete, or_, text, func, column
from sqlalchemy.sql import select
from datetime import datetime

from app.config import db, commit_rollback
from app.model import Stand, Test, Props
from app.schema import StandCreate, PropsCreate, PageResponse


class StandRepository:

    @staticmethod
    async def create(create_form: StandCreate):
        """ create Stand data """
        db.add(Stand(
            stand_name=create_form.stand_name,
            stand_x=create_form.stand_x,
            stand_y=create_form.stand_y,
        ))
        for i in range(1, int(create_form.stand_y) + 1):
            for j in range(1, int(create_form.stand_x) + 1):
                db.add(Test(
                    id_device="",
                    status="EMPTY",
                    id_zone=create_form.stand_name,
                    x_coord=j,
                    y_coord=i,
                    id_user="",
                    id_stage="",
                    ip="Enter IP here"
                ))
                await commit_rollback()
        await commit_rollback()

    @staticmethod
    async def get_by_id(stand_id: int):
        """ retrieve Stand data by id """
        query = select(Stand).where(Stand.stand_name == stand_id)
        return (await db.execute(query)).scalar_one_or_none()

    @staticmethod
    async def update(stand_id: int, update_form: StandCreate):
        """ update Stand data by id"""

        query = update(Stand) \
            .where(Stand.stand_name == stand_id) \
            .values(**update_form.dict()) \
            .execution_options(synchronize_session="fetch")

        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def delete(stand_id: int):
        """ delete Stand data by id """
        # select stand name
        # query = select(Stand).where(Stand.id == stand_id)
        # stand_name = (await db.execute(query)).scalar_one_or_none().stand_name
        stand_name = stand_id

        # delete tests with this name
        query = delete(Test).where(Test.id_zone == stand_name)
        await db.execute(query)
        await commit_rollback()

        # delete stand
        query = delete(Stand).where(Stand.stand_name == stand_id)
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def get_all(
            page: int = 1,
            limit: int = 10,
            columns: str = None,
            sort: str = None,
            filter: str = None
    ):
        query = select(from_obj=Stand, columns="*")

        # select columns dynamically
        if columns is not None and columns != "all":
            # we need column format data like this --> [column(id),column(id_device),column(id_zone)...]

            query = select(from_obj=Stand, columns=convert_columns(columns))

        # select filter dynamically
        if filter is not None and filter != "null":
            # we need filter format data like this  --> {'name': 'an','ip':'an'}

            # convert string to dict format
            criteria = dict(x.split("*") for x in filter.split('-'))

            criteria_list = []

            # check every key in dict. are there any table attributes that are the same as the dict key ?

            for attr, value in criteria.items():
                _attr = getattr(Stand, attr)

                # filter format
                search = "%{}%".format(value)

                # criteria list
                criteria_list.append(_attr.like(search))

            query = query.filter(or_(*criteria_list))

        # select sort dynamically
        if sort is not None and sort != "null":
            # we need sort format data like this --> ['id','name']
            query = query.order_by(text(convert_sort(sort)))

        # count query
        count_query = select(func.count(1)).select_from(query)

        offset_page = page - 1
        # pagination
        query = (query.offset(offset_page * limit).limit(limit))

        # total record
        total_record = (await db.execute(count_query)).scalar() or 0

        # total page
        total_page = math.ceil(total_record / limit)

        # result
        result = (await db.execute(query)).fetchall()

        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_page,
            total_record=total_record,
            content=result
        )


def convert_sort(sort):
    """
    # separate string using split('-')
    split_sort = sort.split('-')
    # join to list with ','
    new_sort = ','.join(split_sort)
    """
    return ','.join(sort.split('-'))


def convert_columns(columns):
    """
    # seperate string using split ('-')
    new_columns = columns.split('-')

    # add to list with column format
    column_list = []
    for data in new_columns:
        column_list.append(data)

    # we use lambda function to make code simple

    """

    return list(map(lambda x: column(x), columns.split('-')))
