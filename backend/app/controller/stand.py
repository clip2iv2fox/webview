from fastapi import APIRouter, Path, Query

from app.repository.stand import StandRepository
from app.schema import ResponseSchema, StandCreate

router = APIRouter(
    prefix="/stand",
    tags=['stand']
)


@router.post("", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_stand(
        create_form: StandCreate
):
    await StandRepository.create(create_form)
    return ResponseSchema(detail="Successfully created data !")


@router.patch("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_stand(
        stand_id: int = Path(..., alias="id"),
        *,
        update_form: StandCreate
):
    await StandRepository.update(stand_id, update_form)
    return ResponseSchema(detail="Successfully updated data !")


@router.delete("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_stand(
        stand_id: int = Path(..., alias="id"),
):
    await StandRepository.delete(stand_id)
    return ResponseSchema(detail="Successfully deleted data !")


@router.get("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_stand_by_id(
        stand_id: int = Path(..., alias="id")
):
    result = await StandRepository.get_by_id(stand_id)
    return ResponseSchema(detail="Successfully fetch data by id !", result=result)


@router.get("", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all_stand(
        page: int = 1,
        limit: int = 10,
        columns: str = Query(None, alias="columns"),
        sort: str = Query(None, alias="sort"),
        filter: str = Query(None, alias="filter"),
):
    result = await StandRepository.get_all(page, limit, columns, sort, filter)
    return ResponseSchema(detail="Successfully fetch data by id !", result=result)
