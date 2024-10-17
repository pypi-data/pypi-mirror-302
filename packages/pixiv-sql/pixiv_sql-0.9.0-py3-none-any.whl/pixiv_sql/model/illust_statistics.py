from sqlalchemy import Column, ForeignKey, Integer
from pixiv_sql.model.base import BaseWithoutIdModel


class IllustStatistics(BaseWithoutIdModel):
    """
    IllustStatistics Model
    """

    __tablename__ = "illust_statistics"

    illust_id = Column(Integer, ForeignKey("bookmarked_illusts.id"), primary_key=True)
    total_view = Column(Integer, default=0, nullable=False)
    total_bookmarks = Column(Integer, default=0, nullable=False)
