from fastapi import FastAPI
import numpy as np
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
# async def root():
def root():
    return {"message": "Hello World"}

@app.get("/home")
def home():
    return {"message": "Home World"}

@app.post("/name")
def set_name(name):
    '''
    이름을 돌려주는 페이지
    '''
    return {
        "result": name
    }

# 요청 본문(Request Body)을 위한 Pydantic 모델 정의
class MemberInfo(BaseModel):
    name: str
    age: int
    sex: str

# POST 요청 처리
@app.post("/member")
def set_info(info: MemberInfo):
    '''
    이름, 나이, 성별을 돌려주는 페이지
    '''
    return {
        "result": f"{info.name}님의 나이는 {info.age}, 성별은 {info.sex}입니다"
    }

