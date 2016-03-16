import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from nailgun.db.sqlalchemy import db_str
from nailgun.db.sqlalchemy.models.network import NetworkGroup

engine = create_engine(db_str, client_encoding='utf8', echo=True)
s = scoped_session(sessionmaker(autoflush=True, autocommit=False, bind=engine))

ng = s.query(NetworkGroup).filter(NetworkGroup.id==1).one()
meta = ng.meta

#s.query(NetworkGroup).filter(NetworkGroup.name=='fuelweb_admin').update({'meta':meta})
#s.query(NetworkGroup).filter(NetworkGroup.name=='fuelweb_admin').all()

for ngroup in s.query(NetworkGroup).filter(NetworkGroup.name=='fuelweb_admin').all():
    print ngroup.id
    s.query(NetworkGroup).filter(NetworkGroup.id==ngroup.id).update({'meta':meta})