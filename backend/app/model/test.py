from datetime import date, datetime
from typing import Optional

from sqlalchemy import Enum, Column, DateTime
from sqlmodel import SQLModel, Field


# class Sex(str, Enum):
#     MALE = "MALE"
#     FEMALE = "FEMALE"


class Test(SQLModel, table=True):
    __tablename__ = "test"

    id: Optional[int] = Field(None, primary_key=True, nullable=False)
    id_device: str
    id_zone: str
    birth_date: date
    birth_place: str
    country: str

    create_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(
        sa_column=Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)
    )
