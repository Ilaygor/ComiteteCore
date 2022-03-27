from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Index, UniqueConstraint
from models.database import Base


class Member(Base):
    __tablename__ = 'Members'
    Id = Column(Integer, primary_key=True)
    MemberId = Column(Integer)
    ServerId = Column(Integer, ForeignKey('Servers.Id', ondelete='CASCADE'))
    __table_args__ = (UniqueConstraint('ServerId', 'MemberId'),)
    IsAlive = Column(Boolean, default=True)

    Info = Column(String, default='')
    Mentions = Column(Integer, default=0)

    Level = Column(Integer, default=1)
    Xp = Column(Float, default=0)
    MaxXp = Column(Float, default=50)
    TotalXp = Column(Float, default=0)

    def __init__(self, serverId: int, memberId: int):
        self.ServerId = serverId
        self.MemberId = memberId

