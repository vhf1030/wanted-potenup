import streamlit as st
from langchain_core.messages import ChatMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai.chat_models import ChatOpenAI
import uuid
import sys
import os
root_path = os.path.abspath(".")
if root_path not in sys.path:
    sys.path.append(root_path)
from config.api_keys import openai_key

# session_id = st.session_state.get("session_id", "user_123")
# session_id = str(uuid.uuid4())  # 요청을 받을때마다 계속 바뀜
# 유저별 고유한 세션 ID 생성 (최초 실행 시 한 번만 생성)
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())  # 최초 요청 시 한 번만 생성

session_id = st.session_state["session_id"]  # 저장된 세션 ID 사용

st.set_page_config(page_title='ChatBot', page_icon='')
st.title('My ChatBot')

if 'store' not in st.session_state:  # 스트림릿은 유저가 실행할 때마다 초기화 되기 때문에 session state에 변수를 저장해야 함
    st.session_state['store'] = dict()

def get_session_history(session_ids):
    print(f'세션: {session_ids}')
    
    if session_ids not in st.session_state['store']:
        st.session_state['store'][session_ids] = ChatMessageHistory()
    
    history = st.session_state['store'][session_ids]
    return history
        
history = get_session_history(session_id)
# print(history)

# # 기존 대화 메시지 표시 - 스트림 기능을 추가하는 것을 고려해서 미리 출력 필요함
# for msg in history.messages:
#     with st.chat_message(msg.type):  # "user" 또는 "ai"
#         st.write(msg.content)


user_input = st.chat_input("메세지를 입력해주세요")
if user_input:

    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        api_key=openai_key
    )
    
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ('system', '질문에 간단하게 답을 해주세요.'),
            MessagesPlaceholder(variable_name='chat_history'),  # 'chat_history'는 디폴트 변수명이므로 고정 해야 함
            ('user', '{question}')
        ]
    )
    
    chain = chat_prompt | llm
    
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key='question',
        history_messages_key='chat_history',
    )

    ai_message = chain_with_history.invoke(
        {'question': user_input},
        config={'configurable': {'session_id': session_id}}, 
    )
    
for msg in history.messages:
    with st.chat_message(msg.type):  # `type`은 "user" 또는 "ai"
        st.write(msg.content)  # 메시지 내용 출력
        
        