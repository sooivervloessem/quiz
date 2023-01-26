from sqlalchemy.orm import Session
from sqlalchemy import update, delete


import models
import schemas


def get_questions(db: Session):
    return db.query(models.Question).all()


def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Question(question=question.question, A_field=question.A_field, B_field=question.B_field,
                                  C_field=question.C_field, D_field=question.D_field)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_question_by_id(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id).first()


def update_question_by_id(db: Session, question: schemas.QuestionCreate, question_id: int):
    db_question = db.get(models.Question, question_id)
    question_data = question.dict(exclude_unset=True)
    for key, value in question_data.items():
        setattr(db_question, key, value)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def delete_question(db: Session, question_id: int):
    db_question = db.get(models.Question, question_id)
    db.delete(db_question)
    db.commit()

    # Renumber the primary key values
    i = 1
    for row in db.query(models.Question).order_by(models.Question.id):
        question_update = update(models.Question).where(models.Question.id == row.id).values(id=i)
        db.execute(question_update)
        i += 1
    db.commit()
    return {"Question deleted": True}


def delete_questions(db: Session):
    db.query(models.Question).delete()
    db.commit()
    return {"All questions have been deleted": True}


def get_teams(db: Session):
    return db.query(models.Team).all()


def create_team(db: Session, team: schemas.TeamCreate):
    db_team = models.Team(name=team.name, score=team.score)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def get_team_by_id(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()


def update_team_by_id(db: Session, team_id: int, team: schemas.TeamCreate):
    db_team = db.get(models.Team, team_id)
    team_data = team.dict(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def delete_team_by_id(db: Session, team_id: int):
    db_team = db.get(models.Team, team_id)
    db.delete(db_team)
    db.commit()

    # Renumber the primary key values
    i = 1
    for row in db.query(models.Team).order_by(models.Team.id):
        team_update = update(models.Team).where(models.Team.id == row.id).values(id=i)
        db.execute(team_update)
        i += 1
    db.commit()
    return {"Team deleted": True}


def delete_teams(db: Session):
    db.query(models.Team).delete()
    db.commit()
    return {"All teams have been deleted": True}


def create_answer(db: Session, answer: schemas.AnswerCreate):
    db_answer = models.Answer(team_id=answer.team_id, question_id=answer.question_id, answer=answer.answer)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def get_answers_by_question_id(db: Session, question_id: int):
    return db.query(models.Answer).filter(models.Answer.question_id == question_id).all()


def get_answers_by_team_id(db: Session, team_id: int):
    return db.query(models.Answer).filter(models.Answer.team_id == team_id).all()


def update_score_by_team_id(db: Session, team_id: int, score: int):
    db_score = db.get(models.Answer, team_id)
    setattr(db_score, "score", score)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score


def get_score_by_team_id(db: Session, team_id: int):
    return db.query(models.Team.score).filter(models.Team.team_id == team_id).all()
