from sqlalchemy import Column, String
from pixiv_sql.model.base import BaseModel


class Series(BaseModel):
    """
    Series Model
    """

    __tablename__ = "series"

    title = Column(String(255), nullable=False)
