from datetime import date
from typing import Optional, TypeVar, Generic, List

from fastapi import HTTPException
from pydantic import BaseModel, validator
from pydantic.generics import GenericModel

# from app.model.test import Sex

T = TypeVar('T')


class TestCreate(BaseModel):
    id_device: Optional[str] = None
    status: Optional[str] = None
    id_zone: Optional[str] = None
    x_coord: Optional[str] = None
    y_coord: Optional[str] = None
    id_user: Optional[str] = None
    id_stage: Optional[str] = None
    ip: Optional[str] = None

    # sex validation
    # @validator("sex")
    # def sex_validation(cls, v):
    #     if hasattr(Sex, v) is False:
    #         raise HTTPException(status_code=400, detail="Invalid input sex")
    #     return v

class TestCreateFirst(BaseModel):
    id_device: Optional[str] = None
    status: Optional[str] = None
    id_user: Optional[str] = None
    id_stage: Optional[str] = None


class TestCreatePartial(BaseModel):
    status: Optional[str] = None
    id_stage: Optional[str] = None


class StandCreate(BaseModel):
    stand_name: Optional[str] = None
    stand_x: Optional[str] = None
    stand_y: Optional[str] = None


class PropsCreate(BaseModel):
    prop: str
    val: str


class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None


class PageResponse(GenericModel, Generic[T]):
    """ The response for a pagination query. """

    page_number: int
    page_size: int
    total_pages: int
    total_record: int
    content: List[T]
