import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint

from models.database import Base


class BoostList(Base):
    __tablename__ = 'BoostLists'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    ChannelId = Column(Integer)
    ServerId = Column(Integer, ForeignKey('Servers.Id', ondelete='CASCADE'))
    __table_args__ = (UniqueConstraint('ChannelId', 'ServerId'),)

    CreatedTime = Column(DateTime)

    def __init__(self, channelId: int, serverId: int):
        self.ChannelId = channelId
        self.ServerId = serverId
        self.CreatedTime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))
