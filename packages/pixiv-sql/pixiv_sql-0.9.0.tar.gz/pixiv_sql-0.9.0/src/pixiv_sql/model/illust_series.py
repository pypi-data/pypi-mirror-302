from sqlalchemy import Column, ForeignKey, Integer
from pixiv_sql.model.base import BaseWithoutIdModel


class IllustSeries(BaseWithoutIdModel):
    """
    IllustSeries Model
    """

    __tablename__ = "illusts_series"

    illust_id = Column(Integer, ForeignKey("bookmarked_illusts.id"), primary_key=True)
    series_id = Column(Integer, ForeignKey("series.id"), primary_key=True)
