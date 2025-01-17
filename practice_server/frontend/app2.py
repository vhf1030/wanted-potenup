import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

data = {
    "x": range(1, 11),
    "y": np.random.randint(1, 100, 10)
}
df = pd.DataFrame(data)
df


# 기본 차트 그리기
st.title("데이터 시각화 - 차트 그리기")
st.header("1. 라인차트")
st.line_chart(df.set_index("x"))

# 바차트 그리기
st.header("2. 바차트")
st.bar_chart(df.set_index("x"))

# matplot 라이브러리 차트 그리기
st.header("3. matplot")
plt.figure(figsize=(10, 5))
plt.plot(df["x"], df["y"], marker='o', color='blue')
plt.title("line chart")
plt.legend()
st.pyplot(plt)

# seaborn 차트 그리기
st.header("4. seaborn")
plt.figure(figsize=(10, 5))
sns.barplot(x="x", y="y", data=df)
plt.title("bar chart")
plt.legend()
st.pyplot(plt)

# plotly 차트 그리기
st.header("5. plotly")
fig = px.scatter(df, x="x", y="y")
st.plotly_chart(fig)


# streamlit run frontend/app2.py

