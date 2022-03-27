from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint

from models.database import Base


class RoleList(Base):
    __tablename__ = 'RoleLists'
    Id = Column(Integer, primary_key=True)
    RoleId = Column(Integer)
    MemberId = Column(Integer, ForeignKey('Members.Id', ondelete='CASCADE'))
    __table_args__ = (UniqueConstraint('MemberId', 'RoleId'),)


    def __init__(self, memberId: int, roleId: int):
        self.MemberId = memberId
        self.RoleId = roleId
