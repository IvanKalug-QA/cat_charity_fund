from sqlalchemy import Column, Integer, ForeignKey, Text

from app.models.base import AbstractBase


class Donation(AbstractBase):
    user_id = Column(
        Integer, ForeignKey('user.id')
    )
    comment = Column(Text)
