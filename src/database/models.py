# src/database/models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Employee(Base):
    __tablename__ = "employees"
    email = Column(String, primary_key=True)
    practice = Column(String)
    level = Column(String)
    location = Column(String)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String)
    timestamp = Column(DateTime)
    session_id = Column(String)
    user_email = Column(String)
    model = Column(String)
    input_tokens = Column(Integer)
    output_tokens = Column(Integer)
    cost_usd = Column(Float)
    tool_name = Column(String)
    success = Column(Boolean)
    duration_ms = Column(Integer)