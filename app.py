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
    st.session_state["new_graph_uploaded"] = True
else:
    with open("systems_model.json") as f:
        system_model = json.load(f)
    st.session_state["new_graph_uploaded"] = False

st.markdown(
    "**📘 Tip:** Modify the systems_model.json locally or upload a different model above. "
    "The Complexity Sentinel will detect changes. Use this with the walkthrough guide to explore different scenarios."
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

# Events Panel (Sidebar)
if "events" in system_model:
    st.sidebar.header("📆 Events Overview")
    event_counts = {}
    for event in system_model["events"]:
        initiator = event.get("initiator", "Unknown")
        event_counts[initiator] = event_counts.get(initiator, 0) + 1
    for actor, count in sorted(event_counts.items(), key=lambda x: -x[1]):
        st.sidebar.write(f"🔸 {actor}: {count} events")

# Agent Selection
selected_agents = st.multiselect("Select Agents to Run", [
    "Systems Thinking", "Chaos Theory", "Karma", "Complexity Sentinel"
], default=["Systems Thinking", "Chaos Theory", "Karma"])

# Systems Thinking
if "Systems Thinking" in selected_agents:
    st.header("🧩 Systems Thinking Agent")
    st.markdown("""
    ### 🧩 Systems Thinking Agent – Interpretation Guide

    - 🔗 **Dependency Analysis**:
        - **Bottlenecks**: Nodes with many incoming edges (e.g., tools used by many)
        - **Isolated Nodes**: Nodes with no inbound/outbound edges

    - 🧠 **Perspectives Analysis**:
        - Based on DSRP (Distinctions, Systems, Relationships, Perspectives)
        - Each perspective shows how a role/team views a node
        - ⚠️ *Note: this is filter-only, not dynamic yet — in AI, this would change agent behavior*
    """)

    systems_agent = SystemsThinkingAgent()
    systems_agent.load_from_dict(system_model)

    st.subheader("Dependency Analysis")
    st.json(systems_agent.analyze_dependencies())

    if st.checkbox("Show System Dependency Graph"):
        systems_agent.visualize_system()

    st.subheader("Perspectives Analysis (P from DSRP)")
    perspectives_results = systems_agent.analyze_perspectives_from_dict(system_model)
    perspective_options = ["All Perspectives"] + list(perspectives_results.keys())
    selected_perspective = st.selectbox("Select Perspective", perspective_options)
    st.markdown(
        "**⚠️ Note:** This dropdown does *not* affect agent logic — it filters only. "
        "In future AI-enhanced versions, perspectives will shape reasoning dynamically."
    )
    if selected_perspective == "All Perspectives":
        st.json(perspectives_results)
    else:
        st.json({selected_perspective: perspectives_results[selected_perspective]})

# Chaos Theory
if "Chaos Theory" in selected_agents:
    st.header("🌪 Chaos Theory Agent")
    st.markdown("""
    ### 🌪 Chaos Theory Agent – Interpretation Guide

    - ✅ **Volatility Score** (0 to 1): Higher = more ripple risk
      - Low (< 0.3): Stable
      - Medium (0.3 – 0.7): Sensitive
      - High (> 0.7): Fragile, may cascade failure

    - ♻️ **Feedback Loops**:
      - Cycles across nodes = amplification risk

    - 🔁 **Volatile Nodes**:
      - Shown in red (> 0.7) on chart
    """)

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
    st.markdown("""
    ### 🧘 Karma Agent – Interpretation Guide

    - ⚖️ **Karma Rating**: Combination of:
        - *Intention*: Human or perspective-labeled value
        - *Impact*: Ripple reach (from Chaos Theory)
        - *Activity*: Event association

    - 🔵 Positive: Helpful intent + high influence
    - 🔴 Negative: Risky impact or harmful intent
    - ⚪ Neutral: Mixed or uncertain

    - Interpreting Karma:
        - Positive intent + low impact = underleveraged
        - Negative intent + high impact = ethical fragility
    """)

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
        st.session_state.previous_flat_graph = None

    if st.session_state.previous_flat_graph is None:
        st.info("No previous model loaded yet. Import a second model to detect structural changes.")
        sentinel_results = {
            "added_nodes": [],
            "removed_nodes": [],
            "added_edges": [],
            "removed_edges": []
        }
    else:
        sentinel = ComplexitySentinelAgent()
        sentinel_results = sentinel.detect_changes(
            st.session_state.previous_flat_graph, flat_graph
        )

    st.subheader("Detected Changes")
    st.json(sentinel_results)

    st.session_state.previous_flat_graph = flat_graph
