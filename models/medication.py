from sqlalchemy import create_engine, Column, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils.config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class Medication(Base):
    __tablename__ = 'medications'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    time = Column(Time, nullable=False)

    def __repr__(self):
        return f"<Medication(name='{self.name}', time='{self.time}')>"

# Создание таблиц
Base.metadata.create_all(engine)
