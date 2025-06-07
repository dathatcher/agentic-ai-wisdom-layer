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

st.set_page_config(page_title="LLM Wisdom Layer Dashboard ", layout="wide")
st.title("🧠 LLM-Powered Wisdom Layer Dashboard ")

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

# Add Ripple Simulation UI if Chaos Agent selected
if agent_choice == "Chaos Theory":
    st.markdown("---")
    st.subheader("⚡ Ripple Simulation (Chaos Agent)")

    with st.form("RippleForm"):
        ripple_target = st.selectbox(
            "Choose a node to simulate removal",
            options=[
                obj["data"]["name"]
                for obj in st.session_state["current_model"].get("Human Interactions", [])
                if "name" in obj["data"]
            ],
            index=0
        )
        ripple_step = st.number_input("Start Step Number", min_value=1, max_value=10, value=1)
        run_multi_step = st.checkbox("🌀 Run full ripple propagation (multi-step)")
        submit_ripple = st.form_submit_button("Simulate Ripple")

    if submit_ripple:
        agent = ChaosTheoryAgentLLM()
        ripple_event = {"type": "remove_person", "target": ripple_target}

        if run_multi_step:
            with st.spinner("Simulating multi-step ripple..."):
                updated_model = agent.simulate_multi_step_ripple(
                    model=st.session_state["current_model"],
                    origin_event=ripple_event,
                    max_steps=3
                )
                for entry in updated_model.get("ripple_history", []):
                    st.markdown(f"### 🌀 Step {entry['step']} Summary")
                    st.markdown(entry['summary'])
                    st.markdown(f"**Severity Score:** {entry.get('severity_score', 'N/A')} (scale 0-100 based on number of impacted nodes)")
                    if entry.get("llm_analysis"):
                        st.info(entry["llm_analysis"])
        else:
            updated_model = agent.simulate_ripple_step(st.session_state["current_model"], ripple_event, ripple_step)
            ripple_summary = agent.summarize_timestep(updated_model, ripple_step)
            st.success(f"Ripple Step {ripple_step} from removal of {ripple_target}")
            st.code(ripple_summary, language="markdown")
