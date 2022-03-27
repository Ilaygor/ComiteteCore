from models.database import create_db, DATABASE_NAME
import os.path
from models import Members, Servers, Emojies, IgnorLists, RoleLists, Votums, database

if not os.path.exists(DATABASE_NAME):
    create_db()

session = database.Session()
from sqlalchemy import func
from sqlalchemy import over

server = session.query(Members.Member, over(func.row_number())).filter(Members.Member.ServerId == 890861254888026122)
for member, rownum in server:
    print(member.Id, rownum)

for member, rownum in filter(lambda member: member[0].MemberId == 269860812355665921, server):
    print(member.Id, rownum)
