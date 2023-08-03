# from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import langchain
from langchain.chat_models import ChatAnthropic
# from langchain.schema import AIMessage, HumanMessage, SystemMessage
import streamlit as st

from contexts import *

context_choices = {
    "Business Advisor": BUSINESS_ADVISOR,
    "Empathetic Advisor": EMPATHETIC_ADVISOR,
    "Plan Interrogator": PLAN_INTERROGATOR,
    "Careful Responder": CAREFUL_RESPONDER,
    "Elephant Path Advisor": ELEPHANT_PATH_ADVISOR,
    "A Shorter Letter": A_SHORTER_LETTER,
    "Gotta keep moving": GOTTA_KEEP_MOVING,
    "Prescriptive Advisor": PRESCRIPTIVE_ADVISOR,
    "One Question at a Time": ONE_QUESTION_AT_A_TIME,
}

def reset_context():
    st.session_state["anthropic_messages"] = []

llm = ChatAnthropic()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "anthropic_messages" not in st.session_state:
    st.session_state["anthropic_messages"] = []

if "message_count" not in st.session_state:
    st.session_state["message_count"] = 0

with st.sidebar:
    "Ask me about your business ideas!"
    "I like to help you make your plans more real."
    "Let's talk through the next steps in your business plan."
    "You can change my personality by selecting traits below."
    context_selections = st.multiselect(
        label="Configure Bot",
        options=context_choices.keys(),
        default=context_choices.keys(),
        on_change=reset_context(),
    )
    context = [context_choices[choice] for choice in context_selections]

st.title("💬 Chatbot")

# print("Messages")
for msg in st.session_state.messages:
    print(msg)
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st.session_state["anthropic_messages"].append(HumanMessage(content=prompt))
    st.session_state["message_count"] += 1
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = llm.predict_messages(context + st.session_state.anthropic_messages)
    print(response)
    msg = response.content
    st.session_state["anthropic_messages"].append(AIMessage(content=msg))
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

    # if st.session_state.message_count % 3 == 0:
    #     check_for_plan = SystemMessage(content="Provide a summary of the plan as you understand it so far. If the user has not provides a part pf the plan, call it out as missing.")
    #     st.session_state["anthropic_messages"].append(check_for_plan)
    #     response = llm.predict_messages(st.session_state.anthropic_messages)
    #     print(response)
    #     msg = response.content
    #     st.session_state["anthropic_messages"].append(AIMessage(content=msg))
    #     st.session_state.messages.append({"role": "assistant", "content": msg})
    #     st.chat_message("assistant").write(msg)
    #
    # if st.session_state.message_count % 5 == 0:
    #     check_for_plan = SystemMessage(content="Offer some unsolicited feedback on the plan so far. What's missing? What's vague? What's just plain silly?")
    #     st.session_state["anthropic_messages"].append(check_for_plan)
    #     response = llm.predict_messages(st.session_state.anthropic_messages)
    #     print(response)
    #     msg = response.content
    #     st.session_state["anthropic_messages"].append(AIMessage(content=msg))
    #     st.session_state.messages.append({"role": "assistant", "content": msg})
    #     st.chat_message("assistant").write(msg)
    #
    # if st.session_state.message_count % 7 == 0:
    #     check_for_plan = SystemMessage(content="Think about the plan as described so far. Document the plan in markdown format with the following sections: Executive Summary, Introduction & Strategy, Plan Details, Risks & Opportunities, Conclusion")
    #     st.session_state["anthropic_messages"].append(check_for_plan)
    #     response = llm.predict_messages(st.session_state.anthropic_messages)
    #     print(response)
    #     msg = response.content
    #     st.session_state["anthropic_messages"].append(AIMessage(content=msg))
    #     st.session_state.messages.append({"role": "assistant", "content": msg})
    #     st.chat_message("assistant").write(msg)
