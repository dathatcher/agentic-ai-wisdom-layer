import streamlit as st
import matplotlib.pyplot as plt
import json
from agents.systems_thinking_agent import SystemsThinkingAgent
from agents.chaos_theory_agent import ChaosTheoryAgent
from agents.karma_agent import KarmaAgent  # ✅ NEW import

st.title("Agentic AI Demo: Systems Thinking + Chaos Theory + Karma")

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

def plot_volatility_scores(volatility_scores):
    st.subheader("Volatility Score Chart")
    labels = list(volatility_scores.keys())
    values = list(volatility_scores.values())

    colors = [
        "red" if v > 0.7 else "orange" if v > 0.4 else "green"
        for v in values
    ]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(labels, values, color=colors)
    ax.set_xlabel("Volatility Score")
    ax.set_xlim(0, 1)
    ax.set_title("Chaos Theory Agent: Volatility Scores")
    st.pyplot(fig)

plot_volatility_scores(chaos_results["volatility_scores"])

#if st.button("Visualize Volatility Graph"):
 #   st.warning("Visualization not yet implemented for volatility scores.")

# --- Karma Agent ---
st.header("Karma Agent")
st.caption("Evaluates ethical impact based on intention and outcome.")
karma_agent = KarmaAgent()
karma_agent.load_system(flat_graph)
karma_results = karma_agent.report()
st.subheader("Karma Agent Results")
st.json(karma_results)

def plot_karma_ratings(karma_ledger):
    st.subheader("Karma Score Chart")
    labels = list(karma_ledger.keys())
    scores = [v["impact_score"] for v in karma_ledger.values()]
    ratings = [v["karma_rating"] for v in karma_ledger.values()]

    color_map = {"Positive": "blue", "Neutral": "gray", "Negative": "red"}
    colors = [color_map.get(rating, "gray") for rating in ratings]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(labels, scores, color=colors)
    ax.set_xlabel("Impact Score")
    ax.set_xlim(0, 1)
    ax.set_title("Karma Agent: Ethical Impact Ratings")
    st.pyplot(fig)

plot_karma_ratings(karma_results)
