import streamlit as st
from langchain_core.messages import ChatMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

import uuid
import sys
import os
root_path = os.path.abspath(".")
if root_path not in sys.path:
    sys.path.append(root_path)
from config.api_keys import openai_key

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
        st.session_state['store'][session_ids] = ChatMessageHistory()  # !!TODO!!
    
    history = st.session_state['store'][session_ids]
    return history
        
history = get_session_history(session_id)
# print(history)

# 기존 대화 메시지 표시 - 스트림 기능을 추가하는 것을 고려해서 미리 출력함
print("\n\nstart")
for msg in history.messages:
    print(msg)  # 디버깅 출력
    msg_type = type(msg).__name__
    print(msg_type)

    # HumanMessage → user, AIMessage → assistant로 변환
    if msg_type == "HumanMessage":
        role = "user"
    elif msg_type == "AIMessageChunk":
        role = "assistant"
    else:
        continue  # "AIMessageChunk" 또는 불필요한 타입이면 무시

    with st.chat_message(role):
        st.write(msg.content)

user_input = st.chat_input("메세지를 입력해주세요")
if user_input:
    # 사용자 메시지를 화면에 표시 & 기록
    st.chat_message("user").write(user_input)
    history.add_message(ChatMessage(role="user", content=user_input))  # 유저 메시지 저장
    
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

    # AI 응답을 위한 채팅 메시지 공간 생성
    with st.chat_message("assistant"):
        response_placeholder = st.empty()  # 응답이 업데이트될 공간
        full_response = ""  # 전체 응답을 저장할 변수

        # 스트리밍 방식으로 응답 출력
        for chunk in chain_with_history.stream(
            {"question": user_input}, 
            config={"configurable": {"session_id": session_id}}
        ):
            full_response += chunk.content  # 응답 추가
            response_placeholder.write(full_response)  # 실시간으로 업데이트

    # AI 응답을 기록하여 히스토리 유지
    history.add_message(ChatMessage(role="assistant", content=full_response)) 
    
        
        