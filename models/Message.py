import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from models.database import Base


class Message(Base):
    __tablename__ = 'Messages'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    MemberId = Column(Integer, ForeignKey('Members.Id', ondelete='CASCADE'))
    Text = Column(String)
    ChannelId = Column(Integer)
    Created = Column(DateTime)

    def __init__(self, memberId: int, channelId: int, text: str):
        self.MemberId = memberId
        self.ChannelId = channelId
        self.Text = text
        self.Created = datetime.datetime.now()
