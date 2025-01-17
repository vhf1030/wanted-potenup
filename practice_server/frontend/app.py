import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Streamlit 실습 진행",
    # layout="wide",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("스트림릿 기본 사용법 익히기")
st.header("첫번째 메뉴")
st.write("첫번째 내용 작성")

st.header("두번째 메뉴")
st.write("두번째 메뉴 내용 작성")
st.header("세번째 메뉴")
st.subheader("서브헤더")
st.text("일반 텍스트 작성")

user_name = st.text_input("이름을 입력하세요")
st.write(f"{user_name}님 안녕하세요")

select_box_input = st.selectbox(
    "관심있는 어종을 선택해주세요",  # 질문
    ["방어", "넙치", "광어"]
)
st.write(f"선택한 어종은 {select_box_input} 입니다")

data = {
    "이름": ["철수", "영희"],
    "나이": [28, 32],
}

df = pd.DataFrame(data)
st.table(df)


# streamlit run frontend/app.py
