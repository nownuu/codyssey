# todo.py
from fastapi import FastAPI, APIRouter
from typing import Dict, List

app = FastAPI()
router = APIRouter()

# 메모리에 TO-DO 저장할 리스트 객체
todo_list: List[Dict] = []

# 1) TO-DO 추가 (POST)
@router.post("/add_todo")
async def add_todo(item: Dict):
    todo_list.append(item)
    return {"message": "TODO added", "data": item}

# 2) TO-DO 전체 조회 (GET)
@router.get("/retrieve_todo")
async def retrieve_todo():
    return {"todo_list": todo_list}

# FastAPI app에 router 등록
app.include_router(router)
