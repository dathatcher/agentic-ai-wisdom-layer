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

# Inline version of flatten_model to avoid import issues
def flatten_model(system_model):
    graph = {}
    for tool in system_model.get("tools", []):
        graph[tool["name"]] = []
        for targets in tool.get("relationships", {}).values():
            graph[tool["name"]].extend(targets)
    for app in system_model.get("applications", []):
        graph.setdefault(app["name"], [])
        graph[app["name"]].extend(app.get("deployed_on", []))
        graph[app["name"]].extend(app.get("monitored_by", []))
    for person in system_model.get("people", []):
        graph[person["name"]] = person.get("uses_tools", [])
        for team in person.get("teams", []):
            graph[person["name"]].append(team)
    for server in system_model.get("servers", []):
        graph.setdefault(server["hostname"], [])
        graph[server["hostname"]].extend(server.get("runs", []))
    for team in system_model.get("teams", []):
        graph.setdefault(team["name"], [])
        for member in team.get("members", []):
            graph[team["name"]].append(member)
        for resp_type, targets in team.get("responsibilities", {}).items():
            for target in targets:
                graph[team["name"]].append(target)
    for event in system_model.get("events", []):
        graph[event["id"]] = []
        if "initiator" in event:
            graph.setdefault(event["initiator"], []).append(event["id"])
        if "related_to" in event:
            if isinstance(event["related_to"], list):
                graph[event["id"]].extend(event["related_to"])
            else:
                graph[event["id"]].append(event["related_to"])
        for sub in event.get("sub_events", []):
            graph[event["id"]].append(sub)
    return graph

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
agent_choice = st.selectbox("Choose an Agent", [
    "Systems Thinking", "Chaos Theory", "Karma", "Complexity Sentinel"
])

# Predefined sample questions by agent
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

# Execute Smart Prompt
if st.button("Submit Question"):
    with st.spinner(f"Running {agent_choice} Agent with Smart Prompt..."):
        meta_context = get_meta_context(system_model)
        if agent_choice == "Systems Thinking":
            agent = SystemsThinkingAgentLLM()
            result = agent.smart_prompt(system_model, meta_context, user_query)
        elif agent_choice == "Chaos Theory":
            agent = ChaosTheoryAgentLLM()
            result = agent.smart_prompt(system_model, meta_context, user_query)
        elif agent_choice == "Karma":
            agent = KarmaAgentLLM()
            result = agent.smart_prompt(system_model, meta_context, user_query)
        elif agent_choice == "Complexity Sentinel":
            agent = ComplexitySentinelAgentLLM()
            result = agent.smart_prompt(system_model, st.session_state.previous_flat_graph, meta_context, user_query)

        st.subheader("🔍 Agent Insight")
        try:
            parsed = json.loads(result)
            st.json(parsed)
        except:
            st.write(result)

# Fallback to classic agents if no query is submitted
if not user_query:
    flat_graph = flatten_model(system_model)

    if agent_choice == "Systems Thinking":
        from agents.systems_thinking_agent import SystemsThinkingAgent
        agent = SystemsThinkingAgent()
        agent.load_from_dict(system_model)
        st.subheader("Dependency Analysis")
        st.json(agent.analyze_dependencies())
        st.subheader("Perspectives Analysis")
        st.json(agent.analyze_perspectives_from_dict(system_model))

    elif agent_choice == "Chaos Theory":
        from agents.chaos_theory_agent import ChaosTheoryAgent
        agent = ChaosTheoryAgent()
        agent.load_system(flat_graph)
        st.subheader("Chaos Insights")
        st.json(agent.analyze_instability())

    elif agent_choice == "Karma":
        from agents.karma_agent import KarmaAgent
        agent = KarmaAgent()
        agent.load_system(flat_graph, events=system_model.get("events", []))
        st.subheader("Karma Assessment")
        st.json(agent.report())

    elif agent_choice == "Complexity Sentinel":
        from agents.complexity_sentinel_agent import ComplexitySentinelAgent
        sentinel = ComplexitySentinelAgent()
        new_graph = flatten_model(system_model)
        if st.session_state.previous_flat_graph:
            st.subheader("Detected Changes")
            st.json(sentinel.detect_changes(st.session_state.previous_flat_graph, new_graph))
        st.session_state.previous_flat_graph = new_graph
