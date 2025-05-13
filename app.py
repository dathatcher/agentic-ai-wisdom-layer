import streamlit as st
from agents.systems_thinking_agent import SystemsThinkingAgent

st.title("Systems Thinking Agent with JSON Model")

agent = SystemsThinkingAgent()
agent.load_from_json("systems_model.json")  # Ensure this is in the same folder or give full path

results = agent.analyze_dependencies()

st.subheader("Analysis Results")
st.json(results)

if st.button("Visualize System Graph"):
    agent.visualize_system()
