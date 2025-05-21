# app.py

import streamlit as st
import json
import os
import matplotlib.pyplot as plt

from agents.systems_thinking_agent import SystemsThinkingAgent
from agents.chaos_theory_agent import ChaosTheoryAgent
from agents.karma_agent import KarmaAgent
from agents.complexity_sentinel_agent import ComplexitySentinelAgent
from agents.complexity_sentinel_agent_llm import ComplexitySentinelAgentLLM
from agents.meta_contexts import get_meta_context

st.set_page_config(page_title="LLM Wisdom Layer Dashboard", layout="wide")
st.title("🧠 LLM-Powered Wisdom Layer Dashboard")

# Upload JSON
uploaded_file = st.file_uploader("Upload your mental model (systems_model.json)", type="json")
if uploaded_file:
    system_model = json.load(uploaded_file)
else:
    default_path = "systems_model.json"
    if os.path.exists(default_path):
        with open(default_path) as f:
            system_model = json.load(f)
    else:
        st.warning("Please upload a system model to continue.")
        st.stop()

if "previous_flat_graph" not in st.session_state:
    st.session_state.previous_flat_graph = None

# Agent Selection
agent_choice = st.selectbox("Choose an Agent", ["Systems Thinking", "Chaos Theory", "Karma", "Complexity Sentinel"])
user_query = st.text_input("Ask the Complexity Sentinel Agent a question:")

if st.button("Submit Question"):
    with st.spinner(f"Running {agent_choice} Agent with Smart Prompt..."):
        if agent_choice == "Complexity Sentinel":
            agent = ComplexitySentinelAgentLLM()
            meta_context = get_meta_context(system_model)
            result = agent.smart_prompt(system_model, st.session_state.previous_flat_graph, meta_context, user_query)

            st.subheader("🔍 Agent Insight")
            try:
                parsed = json.loads(result)
                st.json(parsed)
            except:
                st.write(result)

# Run classic agents
if agent_choice == "Systems Thinking":
    agent = SystemsThinkingAgent()
    agent.load_from_dict(system_model)
    st.subheader("Dependency Analysis")
    st.json(agent.analyze_dependencies())
    st.subheader("Perspectives Analysis")
    st.json(agent.analyze_perspectives_from_dict(system_model))

elif agent_choice == "Chaos Theory":
    agent = ChaosTheoryAgent()
    flat_graph = agent.flatten_model(system_model)
    agent.load_system(flat_graph)
    st.subheader("Chaos Insights")
    st.json(agent.analyze_instability())

elif agent_choice == "Karma":
    agent = KarmaAgent()
    flat_graph = agent.flatten_model(system_model)
    agent.load_system(flat_graph, events=system_model.get("events", []))
    st.subheader("Karma Assessment")
    st.json(agent.report())

# Update previous graph snapshot
if agent_choice == "Complexity Sentinel":
    sentinel = ComplexitySentinelAgent()
    flat_graph = sentinel.flatten_model(system_model)
    if st.session_state.previous_flat_graph:
        st.subheader("Detected Changes")
        st.json(sentinel.detect_changes(st.session_state.previous_flat_graph, flat_graph))
    st.session_state.previous_flat_graph = flat_graph
