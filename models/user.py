from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from utils.config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=False, unique=True)
    medications = relationship("Medication", back_populates="user")

class Medication(Base):
    __tablename__ = 'medications'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date_time = Column(DateTime, nullable=False)  # Убедитесь, что колонка date_time присутствует
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="medications")

# Создание таблиц
Base.metadata.create_all(engine)
