# app.py

import streamlit as st
import json
from agents.systems_thinking_agent import SystemsThinkingAgent
from agents.chaos_theory_agent import ChaosTheoryAgent

st.title("Agentic AI Demo: Systems Thinking + Chaos Theory")

# --- Helper: Convert JSON model to graph format ---
def convert_json_to_graph_model(system_model):
    graph = {}

    # Tools and their relationships
    for tool in system_model.get("tools", []):
        name = tool["name"]
        graph[name] = []
        for targets in tool.get("relationships", {}).values():
            graph[name].extend(targets)

    # Applications -> deployed on + monitored by
    for app in system_model.get("applications", []):
        app_name = app["name"]
        graph.setdefault(app_name, [])
        graph[app_name].extend(app.get("deployed_on", []))
        graph[app_name].extend(app.get("monitored_by", []))

    # People -> tools they use
    for person in system_model.get("people", []):
        person_name = person["name"]
        graph[person_name] = person.get("uses_tools", [])

    # Servers -> apps they run
    for server in system_model.get("servers", []):
        server_name = server["hostname"]
        graph.setdefault(server_name, [])
        graph[server_name].extend(server.get("runs", []))

    return graph

# --- Load and transform input model ---
with open("systems_model.json") as f:
    system_model = json.load(f)

flat_graph = convert_json_to_graph_model(system_model)

# --- Systems Thinking Agent ---
st.header("Systems Thinking Agent")
st.caption("Identifies bottlenecks and isolated nodes.")
systems_agent = SystemsThinkingAgent()
systems_agent.load_from_json("systems_model.json")
systems_results = systems_agent.analyze_dependencies()
st.subheader("Systems Thinking Results")
st.json(systems_results)

if st.button("Visualize System Graph"):
    systems_agent.visualize_system()

# --- Chaos Theory Agent ---
st.header("Chaos Theory Agent")
st.caption("Analyzes volatility and feedback loops.")
chaos_agent = ChaosTheoryAgent()
chaos_agent.load_system(flat_graph)
chaos_results = chaos_agent.analyze_instability()
st.subheader("Chaos Theory Results")
st.json(chaos_results)

if st.button("Visualize Volatility Graph"):
    st.warning("Visualization not yet implemented for volatility scores.")