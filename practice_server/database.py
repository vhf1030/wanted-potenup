from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

# 데이터 베이스 모델의 스키마 정의
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    fish = relationship("Fish", back_populates="seller")
    
# 데이터 베이스 모델의 스키마 정의
class Fish(Base):
    __tablename__ = "fishdata"
    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String)
    price = Column(Integer)
    seller = relationship("User", back_populates="fish")
    
DB_URL = "sqlite:///./wanted_database.db"
engine = create_engine(
    DB_URL
)

# 데이터 베이스 테이블 생성
Base.metadata.create_all(bind=engine)



