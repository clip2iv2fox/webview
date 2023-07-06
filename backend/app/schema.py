from datetime import date
from typing import Optional, TypeVar, Generic, List

from fastapi import HTTPException
from pydantic import BaseModel, validator
from pydantic.generics import GenericModel

# from app.model.test import Sex

T = TypeVar('T')


class TestCreate(BaseModel):
    id_device: str
    id_zone: str
    id_user: str
    id_stage: str
    ip: str

    # sex validation
    # @validator("sex")
    # def sex_validation(cls, v):
    #     if hasattr(Sex, v) is False:
    #         raise HTTPException(status_code=400, detail="Invalid input sex")
    #     return v


class StandCreate(BaseModel):
    stand_name: str
    stand_x: str
    stand_y: str


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
