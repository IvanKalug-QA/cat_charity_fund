from datetime import datetime

from sqlalchemy import (
    Column, Integer,
    Boolean, DateTime,)

from app.core.db import Base


def set_time():
    return datetime.now()


class AbstractBase(Base):
    __abstract__ = True
    full_amount = Column(
        Integer, nullable=False,
    )
    invested_amount = Column(
        Integer, default=0
    )
    fully_invested = Column(
        Boolean, default=False
    )
    create_date = Column(
        DateTime, default=set_time
    )
    close_date = Column(DateTime)