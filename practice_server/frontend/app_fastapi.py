import streamlit as st
import requests

server_url = "http://127.0.0.1:8000/greeting"

st.title("FastAPI와 연동")

if st.button("서버에 요청"):
    try:
        response = requests.get(server_url)
        st.text(response)
        result = response.json()
        st.success(result)
        
    except:
        st.error("요청 실패")


predict_url = "http://127.0.0.1:8000/predict"
input_data = {"x": "김상겸"}
if st.button("서버에 파라미터 요청"):
    try:
        response = requests.post(predict_url, params=input_data)
        st.text(response)
        result = response.json()
        st.success(result)
        
    except:
        st.error("요청 실패")
        
        
# 브라우저에서 숫자를 입력받기
num1 = st.number_input("첫번째 숫자", min_value=0, max_value=50)
num2 = st.number_input("두번째 숫자", min_value=0, max_value=50)
sum_numbers = {
    "x1": num1,
    "x2": num2
}

url = "http://127.0.0.1:8000/sum"
if st.button("서버에 더하기 요청"):
    try:
        response = requests.post(url, params=sum_numbers)
        result = response.json()
        st.success(result)
    except:
        st.error("요청 실패")




# streamlit run frontend/app_fastapi.py
