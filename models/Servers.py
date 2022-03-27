from sqlalchemy import Column, Integer, String, Index
from models.database import Base


class Server(Base):
    __tablename__ = 'Servers'
    Id = Column(Integer, primary_key=True)

    InfoChannel = Column(Integer)
    MemberName = Column(String, default='Member')
    BanText = Column(String, default='has been banned.')
    JoinRole = Column(Integer)

    def __init__(self, id: int):
        self.Id = id

