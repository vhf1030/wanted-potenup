from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse


app = FastAPI()

@app.get("/")  # 주소
def root_index():
    return "Hello World! Wanted AI"

# get방식은 서버의 데이터를 요청하는 것 -> 서버에 데이터가 있어야 한다
data = {
    "서울": {
        "온도": "-2",
        "날씨": "맑음"
    },
    "판교": {
        "온도": "0",
        "날씨": "흐림"
    }
}

# 날씨 관련 라우터 분리
weather_router = APIRouter(prefix="/api/v1/weather", tags=["weather"])

@weather_router.get("/")
def get_weather(city: str):
    return data[city]

@weather_router.get("/today")
def get_weather():
    return {"message": "오늘은 추워요"}

@weather_router.get("/{days}")
def get_weather(days: int):
    return {"message": f"{days}일은 추워요"}

app.include_router(weather_router)

# 저장할 딕셔너리
users_dict = {}

class Users(BaseModel):
    id: int
    name: str = Field(..., min_length=3, max_length=50)
    email: str
    price: float = Field(..., gt=0)  # 희망가격


class UsersResponse(BaseModel):  # 응답양식 설정
    id: int
    name: str = Field(..., min_length=3, max_length=50)
    price: float = Field(..., gt=0)  # 희망가격


# 데이터 유효성 검증
@app.post("/users", response_model=UsersResponse)
def create_users(data: Users):
    users_dict[data.id] = {
        "name": data.name,
        "email": data.email,
        "price": data.price
    }
    print("회원가입이 되었습니다.", users_dict)
    # response = {
    #     "status": "success",
    #     "data": users_dict[data.id]
    # }
    response = UsersResponse(
        id=data.id,
        name=data.name,
        price=data.price
    )
    
    return response
    # return JSONResponse(content=response, status_code=200)
    # return {"message": f"id는 {data.id}입니다. 이름은 {data.name}입니다."}


# def create_users(id: int, name: str, email: str):
#     users_dict[id] = {
#         "name": name,
#         "email": email
#     }
#     print("회원가입이 되었습니다.", users_dict)
#     return {"message": f"id는 {id}입니다. 이름은 {name}입니다."}


user = {
    "홍길동": {
        "나이": 28,
        "성별": "남"
    },
    "춘향이": {
        "나이": 18,
        "성별": "여"
    }
}

@app.get("/user")
def get_user(name: str):
    return user[name]


@app.get("/user/{name}")
def get_user(name: str):
    return {
        "response": "결과입니다",
        "message": f"{name}님 안녕하세요"
    }


fish_data = {
    "방어": {
        "가격": 50000,
        "날짜": 20250115
    }
}

@app.post("/fish-data")
def update_fish_data(fish: str, pay: int, days: int):
    fish_data[fish] = {
        "가격": pay,
        "날짜": days
    }
    return fish_data

from file_processing import file_router
app.include_router(file_router)

#########################################################################
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from fastapi import Depends

Base = declarative_base()

# 데이터 베이스 모델의 스키마 정의
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

DB_URL = "sqlite:///./wanted_database.db"
engine = create_engine(
    DB_URL
)

# 데이터 베이스 테이블 생성
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():  # 의존성 부여
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 회원가입하기
@app.post("/users_db")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    db_user = User(name=name, email=email)
    db.add(db_user)
    db.commit()
    return "데이터베이스에 저장 완료"
    
# 데이터 조회하기
@app.get("/users_db")
def read_all_users(db: Session = Depends(get_db)):
    all_users = db.query(User).all()
    return all_users
    

@app.put("/users_db/{user_id}")
def update_user(user_id: int, name: str, email: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    db_user.name = name
    db_user.email = email
    db.commit()
    db.refresh(db_user)
    return "데이터 수정"






# uvicorn main:app --reload --host 0.0.0.0
# http://192.168.10.87:8000/docs#/


    
    