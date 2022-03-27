import datetime

from sqlalchemy import Column, Integer, Date, ForeignKey, Index

from models.database import Base


class Emojie(Base):
    __tablename__ = 'Emojies'
    Id = Column(Integer, primary_key=True)
    ServerId = Column(Integer, ForeignKey('Servers.Id', ondelete='CASCADE'), primary_key=True)

    CountUsage = Column(Integer, default=1)
    LastUsage = Column(Date)

    def __init__(self, id: int, serverId: int):
        self.Id = id
        self.ServerId = serverId
        self.LastUsage = datetime.date.today()

    def IncrementUsage(self):
        self.LastUsage = datetime.date.today()
        self.CountUsage += 1
