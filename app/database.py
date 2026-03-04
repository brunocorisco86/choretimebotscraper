from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Aviary(Base):
    __tablename__ = 'aviaries'
    id = Column(Integer, primary_key=True)
    number = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False)

class AviaryReading(Base):
    __tablename__ = 'aviary_readings'
    id = Column(Integer, primary_key=True)
    aviary_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.now, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    ammonia = Column(Float)
    age = Column(Integer)
    water_consumption = Column(Float)
    static_pressure = Column(Float)

class Batch(Base):
    __tablename__ = 'batches'
    id = Column(Integer, primary_key=True)
    aviary_id = Column(String, index=True)
    lodging_date = Column(DateTime, nullable=False)
    slaughter_date = Column(DateTime)

def init_db(db_uri):
    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
