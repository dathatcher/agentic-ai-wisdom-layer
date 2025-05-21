
# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer LLM-Powered Dashboard – Refactored

import streamlit as st
import json
import os
import re
from agents.systems_thinking_agent_llm import SystemsThinkingAgentLLM
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="LLM Wisdom Layer Dashboard", layout="wide")
st.title("🧠 LLM-Powered Wisdom Layer Dashboard")

# Upload or load default mental model
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

# Initialize agent
agent = SystemsThinkingAgentLLM(system_context="IT Organization")

# Run Systems Thinking Agent
if st.button("Run Systems Thinking Agent"):
    with st.spinner("Running agent with GPT-4..."):
        output = agent.analyze(system_model)

    st.subheader("🧠 Agent Output (Parsed)")
    cleaned_output = re.sub(r"^```json\n?|```$", "", output.strip(), flags=re.MULTILINE)

    try:
        parsed = json.loads(cleaned_output)
        st.json(parsed)
    except Exception as e:
        st.warning(f"Agent response is not valid JSON. Showing raw output.\n{e}")
        st.text(output)

# Optional: Visualize structure as graph

def build_graph_from_model(system_model):
    import streamlit as st
    import networkx as nx

    G = nx.DiGraph()

    def unwrap(e):
        return e.get("data", e) if isinstance(e, dict) else {}

    st.write("🔍 Building graph from top-level distinctions...")

    for category, entities in system_model.items():
        if not isinstance(entities, list):
            continue
        for raw in entities:
            item = unwrap(raw)

            # Try to get an identifier for the node
            name = (
                item.get("name") or
                item.get("hostname") or
                item.get("id")
            )
            if not name:
                st.write(f"⚠️ Skipping unnamed entry in {category}: {item}")
                continue

            G.add_node(name, type=category)
         #   st.write(f"✅ Added node [{category}]: {name}")

            # Edges from nested maps (e.g. relationships, responsibilities)
            for k in ("relationships", "responsibilities"):
                for rels in item.get(k, {}).values():
                    for t in rels:
                        G.add_edge(name, t)

            # Edges from known relationship lists or strings
            for key in ("monitored_by", "uses_tools", "teams", "runs", "deployed_on", "owned_by"):
                targets = item.get(key)
                if isinstance(targets, list):
                    for t in targets:
                        G.add_edge(name, t)
                elif isinstance(targets, str):
                    G.add_edge(name, targets)

            # Special: Events (initiator, related_to, sub_events)
            if "initiator" in item and "id" in item:
                G.add_edge(item["initiator"], item["id"])
            if "related_to" in item and "id" in item:
                related = item["related_to"]
                if isinstance(related, list):
                    for r in related:
                        G.add_edge(item["id"], r)
                else:
                    G.add_edge(item["id"], related)
            if "sub_events" in item and "id" in item:
                for sub in item.get("sub_events", []):
                    G.add_edge(item["id"], sub)

    st.write(f"✅ Graph complete: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.")
    return G

if st.checkbox("🔗 Show System Graph"):
    st.markdown("This view shows all connected components from your mental model.")
    G = build_graph_from_model(system_model)
    st.write(f"Graph contains {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    if G.number_of_nodes() == 0:
        st.warning("No nodes found. Ensure your model is structured and populated correctly.")
    else:
        pos = nx.kamada_kawai_layout(G)
        node_types = nx.get_node_attributes(G, "type")
        colors = {
            "tool": "dodgerblue", "application": "lightgray", "person": "lightgreen",
            "server": "plum", "team": "orange", "event": "gold"
        }
        node_colors = [colors.get(node_types.get(n, ""), "skyblue") for n in G.nodes]

        fig, ax = plt.subplots(figsize=(12, 8))
        nx.draw(G, pos, ax=ax, with_labels=True, node_color=node_colors,
                node_size=2500, font_size=9, arrows=True)
        st.pyplot(fig)
