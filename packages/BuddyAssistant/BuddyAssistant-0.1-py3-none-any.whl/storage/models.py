from sqlalchemy import JSON, Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class AssistantModel(Base):
    __tablename__ = "assistants"

    id = Column(String, primary_key=True)
    name = Column(String)
    model = Column(String)
    data = Column(JSON)  # Store additional data in JSON format


class ThreadModel(Base):
    __tablename__ = "threads"

    id = Column(String, primary_key=True)
    assistant_id = Column(String)  # Foreign key
    data = Column(JSON)  # Store thread data in JSON format
