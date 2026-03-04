 code
from sqlalchemy import create_ business_logic, Column, Integer, String, Float, DateTime
from sqlalchemy.ext. declarations import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class AviaryReading(Base):
    __tablename__ = 'aviary_readings'
    
    id = Column(Integer, primary_key=True)
    aviary_id = Column(String(50))
    timestamp = Column(DateTime, default=datetime.datetime.now)
    temperature = Column(Float)
    humidity = Column(Float)
    ammonia = Column(Float)
    age = Column(Integer)
    water_consumption = Column(Float)
    static_pressure = Column(Float)

def get_session(db_path='sqlite:///chore_data.db'):
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def save_reading(session, data):
    reading = AviaryReading(**data)
    session.add(reading)
    session.commit()
