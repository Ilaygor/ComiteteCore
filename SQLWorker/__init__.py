from models.database import Session
from models.Members import Member
from sqlalchemy import func
from sqlalchemy import over
from sqlalchemy import desc
session = Session()


def SetAlive(memberId, serverId):
    member = session.query(Member).filter(Member.ServerId == serverId,
                                          Member.MemberId == memberId).first()
    member.IsAlive = True
    session.commit()


def SetDead(memberId, serverId):
    member = session.query(Member).filter(Member.ServerId == serverId,
                                          Member.MemberId == memberId).first()
    member.IsAlive = False
    session.commit()


def AddNewMem(serverId, memberId):
    member = Member(serverId=serverId, memberId=memberId)
    session.add(member)
    session.commit()

def GetRank(memberId, serverId):
    members = session.query(Member, over(func.row_number())).filter(Member.ServerId == serverId).order_by(desc(Member.TotalXp))

    for member, rownum in filter(lambda member: member[0].MemberId == memberId, members):
        return rownum
