
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()


class BookInfo(BaseModel):
    title: str = Field(description="도서 제목")  # LLM이 description을 반영
    author: str = Field(description="글쓴이")
    publication_year: int = Field(description="출판 연도")
    summary: str = Field(description="내용 요약")

parser = PydanticOutputParser(pydantic_object=BookInfo)
llm = ChatOpenAI(
    model_name='gpt-4o-mini',
    # api_key=openai_key,  # load_dotenv로 API키 적용된 상태
    temperature=0
)
prompt = PromptTemplate.from_template(
    """
    사용자가 입력한 도서의 정보를 알려주세요
    도서의 제목, 글쓴이, 출판 연도를 알려주세요
    도서의 간단한 내용을 200자 이내로 요약하세요
    도서 이름: {book_title}
    출력:{format}
    """
)
# partial varible: 사용자가 아닌 개발자가 접근하는 변수
prompt = prompt.partial(format=parser.get_format_instructions())

chain = (
    prompt | llm | parser
)

def send_bookinfo(book_title):
    output = chain.invoke(book_title)
    return output
    # return output.json()

# print(send_bookinfo('설득의 심리학'))
