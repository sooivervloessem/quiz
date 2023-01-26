from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

import os
import crud
import models
import schemas
from database import SessionLocal, engine

print("We are in the main.......")
if not os.path.exists('.\sqlitedb'):
    print("Making folder.......")
    os.makedirs('.\sqlitedb')

print("Creating tables.......")
models.Base.metadata.create_all(bind=engine)
print("Tables created.......")

app = FastAPI()

origins = [
    "http://localhost:8000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/questions/", response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return crud.create_question(db=db, question=question)


@app.get("/questions/", response_model=list[schemas.Question])
def get_questions(db: Session = Depends(get_db)):
    questions = crud.get_questions(db)
    return questions


@app.get("/questions/{question_id}/", response_model=schemas.Question)
def get_question_by_id(question_id: int, db: Session = Depends(get_db)):
    db_question = crud.get_question_by_id(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


@app.put("/questions/{question_id}/", response_model=schemas.Question)
def update_question(question_id: int, question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return crud.update_question_by_id(db=db, question=question, question_id=question_id)


@app.delete("/questions/{question_id}/")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    return crud.delete_question(db=db, question_id=question_id)


@app.delete("/questions/all/")
def delete_questions(db: Session = Depends(get_db)):
    return crud.delete_questions(db=db)


@app.post("/answer/", response_model=schemas.Answer)
def create_answer(answer: schemas.AnswerCreate, db: Session = Depends(get_db)):
    return crud.create_answer(db=db, answer=answer)


@app.get("/answer/{question_id}/")
def get_answers_by_question_id(question_id: int, db: Session = Depends(get_db)):
    return crud.get_answers_by_question_id(db=db, question_id=question_id)


@app.patch("/score/{team_id}")
def update_score_by_team_id(team_id: int, score: int, db: Session = Depends(get_db)):
    return crud.update_score_by_team_id(db=db, team_id=team_id, score=score)


@app.get("/score/{team_id}/")
def get_score_by_team_id(team_id: int, db: Session = Depends(get_db)):
    return crud.get_score_by_team_id(db=db, team_id=team_id)


@app.post("/teams/")
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    return crud.create_team(db=db, team=team)


@app.get("/teams/")
def get_teams(db: Session = Depends(get_db)):
    return crud.get_teams(db=db)


@app.get("/teams/{team_id}/")
def get_team_by_id(team_id: int, db: Session = Depends(get_db)):
    return crud.get_team_by_id(db=db, team_id=team_id)


@app.patch("/teams/{team_id}/")
def update_team_by_id(team_id: int, team: schemas.TeamCreate, db: Session = Depends(get_db)):
    return crud.update_team_by_id(db=db, team_id=team_id, team=team)


@app.delete("/teams/{team_id}/")
def delete_team_by_id(team_id: int, db: Session = Depends(get_db)):
    return crud.delete_team_by_id(db=db, team_id=team_id)


@app.delete("/teams/all/")
def delete_teams(db: Session = Depends(get_db)):
    return crud.delete_teams(db=db)

