import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


st.title("데이터 업로드 받기")
st.header("1. 데이터 업로드하기")

uploaded_file = st.file_uploader("csv파일을 업로드하세요", type=['csv', 'xlsx'])
if uploaded_file is not None:
    st.write("업로드 된 데이터")
    try:
        df = pd.read_csv(uploaded_file)
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding="cp949")
    st.dataframe(df)

    st.header("시각화")
    st.subheader("영화별 매출액")
    fig = px.bar(df, x="영화명", y="매출액")
    st.plotly_chart(fig)

    st.subheader("스크린수별 매출액")
    fig = px.scatter(df, x="스크린수", y="매출액")
    st.plotly_chart(fig)
    
    remove_columns = st.multiselect("제거할 칼럼을 선택해주세요", df.columns)
    if remove_columns:
        rmd_df = df.drop(remove_columns, axis=1)
        st.dataframe(rmd_df)
    


# streamlit run frontend/app3.py



