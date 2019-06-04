'''
Creating a DB with SQLAlchemy
'''

#  Configuration - import all the nesessary modules
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


#  Class - representation of table as a Python class
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Hiking(Base):
    __tablename__ = 'hiking'

    id = Column(Integer, primary_key=True)
    park = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'park': self.park,
        }


class TrailInfo(Base):
    __tablename__ = 'trail_info'

    id = Column(Integer, primary_key=True)
    trail = Column(String, nullable=False)
    date = Column(String)
    url = Column(String)
    address = Column(String)
    distance = Column(String)
    elevation = Column(String)
    level = Column(String)

    park_id = Column(Integer, ForeignKey('hiking.id'))
    hiking = relationship(Hiking)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'trail': self.trail,
            'date': self.date,
            'url': self.url,
            'address': self.address,
            'distance': self.distance,
            'elevation': self.elevation,
            'level': self.level,
        }


engine = create_engine('sqlite:///hikingtrailinfo.db')
Base.metadata.create_all(engine)
