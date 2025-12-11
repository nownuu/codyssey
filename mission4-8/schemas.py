from pydantic import BaseModel, validator


class QuestionCreate(BaseModel):
    title: str
    content: str

    @validator('title', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('값은 빈 문자열일 수 없습니다.')
        return v
