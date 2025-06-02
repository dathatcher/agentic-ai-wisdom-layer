# llm_dashboard.py

import streamlit as st
import json
import os
import matplotlib.pyplot as plt

from agents.systems_thinking_agent_llm import SystemsThinkingAgentLLM
from agents.chaos_theory_agent_llm import ChaosTheoryAgentLLM
from agents.karma_agent_llm import KarmaAgentLLM
from agents.complexity_sentinel_agent_llm import ComplexitySentinelAgentLLM
from agents.meta_contexts import get_meta_context
from dotenv import load_dotenv
load_dotenv()


st.set_page_config(page_title="LLM Wisdom Layer Dashboard V1", layout="wide")
st.title("🧠 LLM-Powered Wisdom Layer Dashboard v1")

# Upload current and previous JSON models
current_model_file = st.file_uploader("Upload CURRENT system model", type="json", key="current")
previous_model_file = st.file_uploader("Upload PREVIOUS system model", type="json", key="previous")

if current_model_file:
    current_model = json.load(current_model_file)
    st.session_state["current_model"] = current_model
else:
    st.warning("Upload the current model to proceed.")
    st.stop()

if previous_model_file:
    previous_model = json.load(previous_model_file)
    st.session_state["previous_model"] = previous_model
else:
    previous_model = None
    st.session_state["previous_model"] = None

# Select Agent
agent_choice = st.selectbox("Choose an Agent", [
    "Systems Thinking", "Chaos Theory", "Karma", "Complexity Sentinel"
])

# Predefined questions
question_options = {
    "Systems Thinking": [
        "What are the bottlenecks in this system?",
        "Which teams are isolated from the rest of the system?",
        "How do tools connect across teams and apps?",
        "Where might communication breakdowns occur?",
        "Are there underutilized components in the system?"
    ],
    "Chaos Theory": [
        "Which nodes are most volatile and why?",
        "What would happen if PayrollApp fails?",
        "Which feedback loops could cause cascading failures?",
        "Where is the system most fragile to changes?",
        "How does volatility propagate through the stack?"
    ],
    "Karma": [
        "Which actors are ethically fragile?",
        "Who has high impact but unclear intention?",
        "Which teams have positive intent but low leverage?",
        "What nodes might be causing unintended harm?",
        "Where can ethical improvements shift the system?"
    ],
    "Complexity Sentinel": [
        "What new relationships or nodes have emerged unexpectedly?",
        "Which system changes are most likely to introduce risk?",
        "Are there new bottlenecks forming in the updated model?",
        "What patterns suggest a phase shift in complexity?",
        "Did the last change increase or decrease entropy?"
    ]
}

sample = st.selectbox("Sample Questions", question_options.get(agent_choice, []))
user_query = st.text_input("Ask the selected agent a question:", value=sample)

# Run Smart Prompt
if st.button("Submit Question"):
    with st.spinner(f"Running {agent_choice} Agent with Smart Prompt..."):
        meta_context = get_meta_context(st.session_state["current_model"])

        if agent_choice == "Systems Thinking":
            agent = SystemsThinkingAgentLLM()
            result = agent.smart_prompt(st.session_state["current_model"], meta_context, user_query)

        elif agent_choice == "Chaos Theory":
            agent = ChaosTheoryAgentLLM()
            result = agent.smart_prompt(st.session_state["current_model"], meta_context, user_query)

        elif agent_choice == "Karma":
            agent = KarmaAgentLLM()
            result = agent.smart_prompt(st.session_state["current_model"], meta_context, user_query)

        elif agent_choice == "Complexity Sentinel":
            agent = ComplexitySentinelAgentLLM()
            result = agent.smart_prompt(
                current_model=st.session_state["current_model"],
                previous_model=st.session_state["previous_model"],
                meta_context=meta_context,
                user_query=user_query
            )

        st.subheader("🔍 Agent Insight")

        try:
            result = result.strip()
            parsed = json.loads(result)
            st.json(parsed)
        except json.JSONDecodeError:
            st.warning("⚠️ The response is not JSON. Displaying raw text instead.")
            st.markdown(result)
