import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint

from models.database import Base


class Votum(Base):
    __tablename__ = 'Votums'
    Id = Column(Integer, primary_key=True)
    ServerId = Column(Integer, ForeignKey('Servers.Id', ondelete='CASCADE'))
    ChannelId = Column(Integer)
    MemberId = Column(Integer, ForeignKey('Members.Id', ondelete='CASCADE'))
    MessageId = Column(Integer)
    __table_args__ = (UniqueConstraint('ServerId', 'MemberId'),)
    EndTime = Column(DateTime)

    def __init__(self, serverId: int, channelId: int, messageId: int, memberId: int):
        self.ServerId = serverId
        self.ChannelId = channelId
        self.MessageId  = messageId
        self.MemberId = memberId
        self.EndTime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=4)))
