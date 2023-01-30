from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import os
import crud
import models
import schemas
from database import SessionLocal, engine
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles



print("We are in the main.......")
if not os.path.exists('.\sqlitedb'):
    print("Making folder.......")
    os.makedirs('.\sqlitedb')

print("Creating tables.......")
models.Base.metadata.create_all(bind=engine)
print("Tables created.......")

app = FastAPI(docs_url=None, redoc_url=None)


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )




origins = [
    "http://localhost:8000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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


#@app.on_event('startup')
#def init_data(status: bool, question_id: int = 0):
#    if status:
#        current_question_id = question_id
#    else:
#    print(current_question_id)
#    return current_question_id


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
    global current_question_id
    current_question_id = question_id
    return db_question


@app.put("/questions/{question_id}/", response_model=schemas.Question)
def update_question(question_id: int, question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return crud.update_question_by_id(db=db, question=question, question_id=question_id)


@app.delete("/questions/all/")
def delete_questions(db: Session = Depends(get_db)):
    return crud.delete_questions(db=db)


@app.delete("/questions/{question_id}/")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    return crud.delete_question(db=db, question_id=question_id)


@app.post("/answer/", response_model=schemas.Answer)
def create_answer(answer: schemas.AnswerCreate, db: Session = Depends(get_db)):
    return crud.create_answer(db=db, answer=answer, question_id=current_question_id)


@app.get("/answer/question/{question_id}/")
def get_answers_by_question_id(question_id: int, db: Session = Depends(get_db)):
    return crud.get_answers_by_question_id(db=db, question_id=question_id)


@app.get("/answer/team/{team_id}/")
def get_answers_by_team_id(team_id: int, db: Session = Depends(get_db)):
    return crud.get_answers_by_team_id(db=db, team_id=team_id)


@app.patch("/score/{team_id}/")
def update_score_by_team_id(team_id: int, score: str, db: Session = Depends(get_db)):
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


@app.delete("/teams/all/")
def delete_teams(db: Session = Depends(get_db)):
    return crud.delete_teams(db=db)


@app.delete("/teams/{team_id}/")
def delete_team_by_id(team_id: int, db: Session = Depends(get_db)):
    return crud.delete_team_by_id(db=db, team_id=team_id)

@app.get("/question_id/")
def get_question_id(db: Session = Depends(get_db)):
    return current_question_id

@app.delete("/answers/")
def delete_answers(db: Session = Depends(get_db)):
    return crud.delete_answers(db=db)
