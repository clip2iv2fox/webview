from fastapi import APIRouter, Path, Query

from app.repository.test import TestRepository
from app.schema import ResponseSchema, TestCreate, StandCreate

router = APIRouter(
    prefix="/test",
    tags=['test']
)


@router.post("", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_test(
        create_form: TestCreate
):
    await TestRepository.create(create_form)
    return ResponseSchema(detail="Successfully created data !")


@router.patch("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_person(
        test_id: int = Path(..., alias="id"),
        *,
        update_form: TestCreate
):
    await TestRepository.update(test_id, update_form)
    return ResponseSchema(detail="Successfully updated data !")


@router.delete("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_person(
        test_id: int = Path(..., alias="id"),
):
    await TestRepository.delete(test_id)
    return ResponseSchema(detail="Successfully deleted data !")


@router.get("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_person_by_id(
        person_id: int = Path(..., alias="id")
):
    result = await TestRepository.get_by_id(person_id)
    return ResponseSchema(detail="Successfully fetch data by id !", result=result)


@router.get("", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all_person(
        page: int = 1,
        limit: int = 10,
        columns: str = Query(None, alias="columns"),
        sort: str = Query(None, alias="sort"),
        filter: str = Query(None, alias="filter"),
):
    result = await TestRepository.get_all(page, limit, columns, sort, filter)
    return ResponseSchema(detail="Successfully fetch data by id !", result=result)

#
# router2 = APIRouter(
#     prefix="/stand",
#     tags=['stand']
# )
#
#
# @router2.post("", response_model=ResponseSchema, response_model_exclude_none=True)
# async def create_test(
#         create_form: StandCreate
# ):
#     await TestRepository.create(create_form)
#     return ResponseSchema(detail="Successfully created data !")
#
#
# @router2.patch("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
# async def update_test(
#         stand_id: int = Path(..., alias="id"),
#         *,
#         update_form: StandCreate
# ):
#     await TestRepository.update(stand_id, update_form)
#     return ResponseSchema(detail="Successfully updated data !")
#
#
# @router2.delete("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
# async def delete_person(
#         stand_id: int = Path(..., alias="id"),
# ):
#     await TestRepository.delete(stand_id)
#     return ResponseSchema(detail="Successfully deleted data !")
#
#
# @router2.get("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
# async def get_person_by_id(
#         stand_id: int = Path(..., alias="id")
# ):
#     result = await TestRepository.get_by_id(stand_id)
#     return ResponseSchema(detail="Successfully fetch data by id !", result=result)
#
#
# @router2.get("", response_model=ResponseSchema, response_model_exclude_none=True)
# async def get_all_person(
#         page: int = 1,
#         limit: int = 10,
#         columns: str = Query(None, alias="columns"),
#         sort: str = Query(None, alias="sort"),
#         filter: str = Query(None, alias="filter"),
# ):
#     result = await TestRepository.get_all(page, limit, columns, sort, filter)
#     return ResponseSchema(detail="Successfully fetch data by id !", result=result)
