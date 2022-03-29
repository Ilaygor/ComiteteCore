from sqlalchemy import desc

from models.Members import Member
from models.database import Session

session = Session()


def SetAlive(memberId, serverId):
    member = session.query(Member)\
        .filter(Member.ServerId == serverId)\
        .filter(Member.MemberId == memberId).first()
    member.IsAlive = True
    session.commit()


def SetDead(memberId, serverId):
    member = session.query(Member)\
        .filter(Member.ServerId == serverId)\
        .filter(Member.MemberId == memberId).first()
    member.IsAlive = False
    session.commit()


def AddNewMem(serverId, memberId):
    member = Member(serverId=serverId, memberId=memberId)
    session.add(member)
    session.commit()


def GetRank(memberId, serverId):
    members = session.query(Member)\
        .filter(Member.ServerId == serverId)\
        .filter(Member.IsAlive).order_by(desc(Member.TotalXp))
    i = 0

    for member in members:
        i += 1
        if member.MemberId == memberId and member.ServerId == serverId:
            return i
