from pydantic import BaseModel


class TeamBase(BaseModel):
    name: str
    score: int


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True


class QuestionBase(BaseModel):
    question: str
    A_field: str
    B_field: str
    C_field: str
    D_field: str


class QuestionCreate(QuestionBase):
    solution: str


class Question(QuestionBase):
    id: int

    class Config:
        orm_mode = True


class AnswerBase(BaseModel):
    team_id: int
    question_id: int
    answer: str


class AnswerCreate(AnswerBase):
    pass


class Answer(AnswerBase):
    id: int

    class Config:
        orm_mode = True
