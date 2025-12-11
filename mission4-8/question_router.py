from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas import QuestionCreate
from models import Question
from database import get_db


router = APIRouter()


@router.post('/question/')
def question_create(question: QuestionCreate, db: Session = Depends(get_db)):
    new_question = Question(
        title=question.title,
        content=question.content
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return {
        'message': '질문이 성공적으로 등록되었습니다.',
        'question_id': new_question.id,
        'title': new_question.title,
        'content': new_question.content
    }
