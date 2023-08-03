# from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from langchain.chat_models import ChatAnthropic
# from langchain.schema import AIMessage, HumanMessage, SystemMessage
import streamlit as st

from contexts import *

context = [
    BUSINESS_ADVISOR,
    EMPATHETIC_ADVISOR,
    PLAN_INTERROGATOR,
    CAREFUL_RESPONDER,
    ELEPHANT_PATH_ADVISOR,
    A_SHORTER_LETTER,
    GOTTA_KEEP_MOVING,
    PRESCRIPTIVE_ADVISOR,
    ONE_QUESTION_AT_A_TIME,
]

llm = ChatAnthropic()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "anthropic_messages" not in st.session_state:
    st.session_state["anthropic_messages"] = context

if "message_count" not in st.session_state:
    st.session_state["message_count"] = 0

with st.sidebar:
    "Ask me about your business ideas!"
    "I like to help you make your plans more real."
    "Let's talk through the next steps in your business plan."

st.title("💬 Chatbot")

print("Messages")
for msg in st.session_state.messages:
    print(msg)
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st.session_state["anthropic_messages"].append(HumanMessage(content=prompt))
    st.session_state["message_count"] += 1
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = llm.predict_messages(st.session_state.anthropic_messages)
    print(response)
    msg = response.content
    st.session_state["anthropic_messages"].append(AIMessage(content=msg))
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

    if st.session_state.message_count % 3 == 0:
        check_for_plan = SystemMessage(content="Provide a summary of the plan as you understand it so far. If the user has not provides a part pf the plan, call it out as missing.")
        st.session_state["anthropic_messages"].append(check_for_plan)
        response = llm.predict_messages(st.session_state.anthropic_messages)
        print(response)
        msg = response.content
        st.session_state["anthropic_messages"].append(AIMessage(content=msg))
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

    if st.session_state.message_count % 5 == 0:
        check_for_plan = SystemMessage(content="Offer some unsolicited feedback on the plan so far. What's missing? What's vague? What's just plain silly?")
        st.session_state["anthropic_messages"].append(check_for_plan)
        response = llm.predict_messages(st.session_state.anthropic_messages)
        print(response)
        msg = response.content
        st.session_state["anthropic_messages"].append(AIMessage(content=msg))
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
