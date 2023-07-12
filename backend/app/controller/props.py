from fastapi import APIRouter, Path, Query

from app.repository.props import PropsRepository
from app.schema import ResponseSchema, PropsCreate

router = APIRouter(
    prefix="/props",
    tags=['props']
)


@router.post("", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_test(
        create_form: PropsCreate
):
    await PropsRepository.create(create_form)
    return ResponseSchema(detail="Successfully created data !")


@router.patch("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_test(
        test_id: str = Path(..., alias="id"),
        *,
        update_form: PropsCreate
):
    await PropsRepository.update(test_id, update_form)
    return ResponseSchema(detail="Successfully updated data !")


@router.delete("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_test(
        test_id: str = Path(..., alias="id"),
):
    await PropsRepository.delete(test_id)
    return ResponseSchema(detail="Successfully deleted data !")


@router.get("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_test_by_id(
        test_id: str = Path(..., alias="id")
):
    result = await PropsRepository.get_by_id(test_id)
    return ResponseSchema(detail="Successfully fetch data by id !", result=result)


@router.get("", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all_test(
        page: int = 1,
        limit: int = 10,
        columns: str = Query(None, alias="columns"),
        sort: str = Query(None, alias="sort"),
        filter: str = Query(None, alias="filter")
):
    result = await PropsRepository.get_all(page, limit, columns, sort, filter)
    return ResponseSchema(detail="Successfully fetch data by id !", result=result)
