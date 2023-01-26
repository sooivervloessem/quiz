from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base





class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True )
    score = Column(Integer, index=True)


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
    A_field = Column(String, index=True)
    B_field = Column(String, index=True)
    C_field = Column(String, index=True)
    D_field = Column(String, index=True)
    solution = Column(String, index=True)


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, index=True)
    question_id = Column(Integer, index=True)
    answer = Column(String, index=True)
