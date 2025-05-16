# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Simulation Framework
# For license and reuse contact: david.austin.thatcher@gmail.com

import streamlit as st
import matplotlib.pyplot as plt
import json
from agents.systems_thinking_agent import SystemsThinkingAgent
from agents.chaos_theory_agent import ChaosTheoryAgent
from agents.karma_agent import KarmaAgent
from agents.complexity_sentinel_agent import ComplexitySentinelAgent

st.set_page_config(page_title="Agentic AI Dashboard", layout="wide")
st.title("🧠 Agentic AI Interactive Dashboard")

# Upload JSON
uploaded_file = st.file_uploader("Upload a system model (.json)", type="json")
if uploaded_file:
    system_model = json.load(uploaded_file)
else:
    with open("systems_model.json") as f:
        system_model = json.load(f)
st.markdown(
    "**⚠️ Note:** You can modify the systems_model.json file locally and import it here (above)."
     " Follow the instructions in the WALKTHROUGH.md to explore how different structures, roles, or events affect the output."
     " Any structural or behavioral change in the file will be detected and reflected by the Complexity Sentinel agent."
)
# Convert JSON to flat graph
def convert_json_to_graph(system_model):
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
        for tool in team.get("responsibilities", {}).get("owns_tools", []):
            graph[team["name"]].append(tool)
        for app in team.get("responsibilities", {}).get("monitors_apps", []):
            graph[team["name"]].append(app)
        for integration in team.get("responsibilities", {}).get("integrates_with", []):
            graph[team["name"]].append(integration)
        for app in team.get("responsibilities", {}).get("owns_apps", []):
            graph[team["name"]].append(app)
        for used_tool in team.get("responsibilities", {}).get("uses_tools", []):
            graph[team["name"]].append(used_tool)
        for responded_app in team.get("responsibilities", {}).get("responds_to", []):
            graph[team["name"]].append(responded_app)
    for event in system_model.get("events", []):
        graph[event["id"]] = []
        if "initiator" in event:
            graph.setdefault(event["initiator"], []).append(event["id"])
        if "related_to" in event:
            graph[event["id"]].append(event["related_to"])
        for sub in event.get("sub_events", []):
            graph[event["id"]].append(sub)
    return graph

flat_graph = convert_json_to_graph(system_model)

# Display Events Panel
if "events" in system_model:
    st.sidebar.header("📆 Events Overview")
    event_counts = {}
    for event in system_model["events"]:
        initiator = event.get("initiator", "Unknown")
        event_counts[initiator] = event_counts.get(initiator, 0) + 1

    for actor, count in sorted(event_counts.items(), key=lambda x: -x[1]):
        st.sidebar.write(f"🔸 {actor}: {count} events")

# Select Agents
selected_agents = st.multiselect("Select Agents to Run", [
    "Systems Thinking", "Chaos Theory", "Karma", "Complexity Sentinel"
], default=["Systems Thinking", "Chaos Theory", "Karma"])

# Systems Thinking
if "Systems Thinking" in selected_agents:
    st.header("🧩 Systems Thinking Agent")
    systems_agent = SystemsThinkingAgent()
    systems_agent.load_from_dict(system_model)

    st.subheader("Dependency Analysis")
    systems_results = systems_agent.analyze_dependencies()
    st.json(systems_results)

    if st.checkbox("Show System Dependency Graph"):
        systems_agent.visualize_system()

    st.subheader("Perspectives Analysis (P from DSRP)")
    perspectives_results = systems_agent.analyze_perspectives_from_dict(system_model)
    perspective_options = ["All Perspectives"] + list(perspectives_results.keys())
    selected_perspective = st.selectbox("Select Perspective", perspective_options)
 
    st.markdown(
      "**⚠️ Note:** This dropdown does _not_ change the behavior of agents. "
      "It only filters the view of perspectives. In a future implementation, AI agents will dynamically re-evaluate "
      "each layer based on the selected perspective."
    )

    if selected_perspective == "All Perspectives":
        st.json(perspectives_results)
    else:
        st.json({selected_perspective: perspectives_results[selected_perspective]})

# Chaos Theory
if "Chaos Theory" in selected_agents:
    st.header("🌪 Chaos Theory Agent")
    chaos_agent = ChaosTheoryAgent()
    chaos_agent.load_system(flat_graph, decay_factor=0.6)
    chaos_results = chaos_agent.analyze_instability()
    st.json(chaos_results)

    if st.checkbox("Show Volatility Chart"):
        labels = list(chaos_results["volatility_scores"].keys())
        values = list(chaos_results["volatility_scores"].values())
        colors = ["red" if v > 0.7 else "orange" if v > 0.4 else "green" for v in values]
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(labels, values, color=colors)
        ax.set_xlim(0, 1)
        ax.set_xlabel("Volatility Score")
        ax.set_title("Chaos Theory Agent: Volatility Scores")
        st.pyplot(fig)

# Karma
if "Karma" in selected_agents:
    st.header("🧘 Karma Agent")
    karma_agent = KarmaAgent()
    karma_agent.load_system(flat_graph, events=system_model.get("events", []))
    karma_results = karma_agent.report()
    st.json(karma_results)

    if st.checkbox("Show Karma Score Chart"):
        labels = list(karma_results.keys())
        scores = [v["impact_score"] for v in karma_results.values()]
        colors = [
            "blue" if v["karma_rating"] == "Positive"
            else "gray" if v["karma_rating"] == "Neutral"
            else "red"
            for v in karma_results.values()
        ]
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(labels, scores, color=colors)
        ax.set_xlim(0, 1)
        ax.set_xlabel("Impact Score")
        ax.set_title("Karma Agent: Ethical Impact Ratings")
        st.pyplot(fig)

# Complexity Sentinel
if "Complexity Sentinel" in selected_agents:
    st.header("🕵️‍♂️ Complexity Sentinel Agent")
    if "previous_flat_graph" not in st.session_state:
        st.session_state.previous_flat_graph = flat_graph
    sentinel = ComplexitySentinelAgent()
    sentinel_results = sentinel.detect_changes(
        st.session_state.previous_flat_graph, flat_graph
    )
    st.subheader("Detected Changes")
    st.json(sentinel_results)
    st.session_state.previous_flat_graph = flat_graph
