from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

class Goal(Base):
    __tablename__ = "goals"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    short_term_goal = Column(Text)
    long_term_goal = Column(Text)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    ai_response = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
