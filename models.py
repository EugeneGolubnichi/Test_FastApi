import random
from sqlalchemy import Table, Index, Integer, String, Column, create_engine, ForeignKey ,func
from sqlalchemy.ext.declarative import declarative_base
from mac_creator import mac_creator, device_creator
from sqlalchemy.orm import Session, relationship

Base = declarative_base()
engine = create_engine("postgresql+psycopg2://horse:horse@localhost/horse_db")

class Endpoint(Base):
    __tablename__ = 'endpoints'
    id = Column(Integer, primary_key=True,autoincrement=True)
    point = Column(String(200))
    ondelete = 'RESTRICT'


class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer,primary_key=True)
    dev_id = Column(String(100))
    dev_type = Column(String(100))
    endpoint = Column(Integer, ForeignKey('endpoints.id'),nullable=True)
    device = relationship("Endpoint")





def add_endpoints():
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    a = 0
    while a < 10:
        a+=1
        q1 = Endpoint(
            point=random.randint(1,50)
                     )
        session.add(q1)
        session.commit()
    session.close()

def add_10_devices():
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    list_of_endpoints = [None, 1, 2]
    for i in range(10):
        d1 = Device(
            dev_id = mac_creator(),
            dev_type = device_creator(),
            endpoint = random.choice(list_of_endpoints)

)
        session.add(d1)
        session.commit()
        session.close()
#a = 0
#d1 = Device(
 #   dev_id = device_creator(),
 #   dev_type = mac_creator(),
 #   endpoint = random.randint(1,50)

#)
#session.add(d1)
#session.commit()
#session.close()

#def query_set():
#    query_list = session.query(Device.id, Device.dev_id, Device.dev_type, ).filter_by(endpoint = None).all()
#    for i in query_list:
#        print(str(i))

#query_count = session.query(Device.dev_type, func.count(Device.dev_type) ).filter_by(endpoint = None).group_by(Device.dev_type)
#for i in query_count:
    #print(str(i))

