
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
    for server in system_model.get("servers", []):
        graph.setdefault(server["hostname"], [])
        graph[server["hostname"]].extend(server.get("runs", []))
    return graph

flat_graph = convert_json_to_graph(system_model)

# Select Agents
selected_agents = st.multiselect("Select Agents to Run", [
    "Systems Thinking", "Chaos Theory", "Karma", "Complexity Sentinel"
], default=["Systems Thinking", "Chaos Theory", "Karma"])

# Systems Thinking
if "Systems Thinking" in selected_agents:
    st.header("🧩 Systems Thinking Agent")
    systems_agent = SystemsThinkingAgent()
    systems_agent.load_from_json("systems_model.json")

    # Dependency analysis
    st.subheader("Dependency Analysis")
    systems_results = systems_agent.analyze_dependencies()
    st.json(systems_results)

    # System graph
    if st.checkbox("Show System Dependency Graph"):
        systems_agent.visualize_system()

    # Perspectives
    st.subheader("Perspectives Analysis (P from DSRP)")
    perspectives_results = systems_agent.analyze_perspectives("systems_model.json")
    perspective_options = ["All Perspectives"] + list(perspectives_results.keys())
    selected_perspective = st.selectbox("Select Perspective", perspective_options)

    if selected_perspective == "All Perspectives":
        st.json(perspectives_results)
    else:
        st.json({selected_perspective: perspectives_results[selected_perspective]})

# Chaos Theory
if "Chaos Theory" in selected_agents:
    st.header("🌪 Chaos Theory Agent")
    chaos_agent = ChaosTheoryAgent()
    chaos_agent.load_system(flat_graph)
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
    karma_agent.load_system(flat_graph)
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
    previous_json = st.text_area("Paste previous flat graph JSON", height=200, value=json.dumps(flat_graph, indent=2))
    try:
        previous_graph = json.loads(previous_json)
    except json.JSONDecodeError:
        st.error("Invalid JSON")
        previous_graph = {}

    sentinel = ComplexitySentinelAgent()
    sentinel_results = sentinel.detect_changes(previous_graph, flat_graph)
    st.subheader("Detected Changes")
    st.json(sentinel_results)
