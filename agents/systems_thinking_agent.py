
# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Simulation Framework
# For license and reuse contact: david.austin.thatcher@gmail.com

import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
import json

class SystemsThinkingAgent:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.node_types = {}

    def load_from_json(self, filepath):
        with open(filepath) as f:
            data = json.load(f)
        self.load_from_dict(data)

    def load_from_dict(self, data):
        self.graph.clear()
        self.node_types.clear()

        def unwrap(entry):
            return entry.get("data", entry)

        print("✅ Building graph from mental model...")

        # Tools
        for raw in data.get("tools", []):
            tool = unwrap(raw)
            name = tool.get("name")
            if not name:
                continue
            self.graph.add_node(name)
            self.node_types[name] = "tool"
            for app in tool.get("relationships", {}).get("monitors_applications", []):
                self.graph.add_edge(name, app)
            for team in tool.get("relationships", {}).get("used_by_teams", []):
                self.graph.add_edge(team, name)
            for integration in tool.get("relationships", {}).get("integrates_with", []):
                self.graph.add_edge(name, integration)

        # Applications
        for raw in data.get("applications", []):
            app = unwrap(raw)
            name = app.get("name")
            if not name:
                continue
            self.graph.add_node(name)
            self.node_types[name] = "application"
            for server in app.get("deployed_on", []):
                self.graph.add_edge(name, server)
            for monitor in app.get("monitored_by", []):
                self.graph.add_edge(monitor, name)

        # People
        for raw in data.get("people", []):
            person = unwrap(raw)
            name = person.get("name")
            if not name:
                continue
            self.graph.add_node(name)
            self.node_types[name] = "person"
            for tool in person.get("uses_tools", []):
                self.graph.add_edge(name, tool)
            for team in person.get("teams", []):
                self.graph.add_edge(name, team)

        # Servers
        for raw in data.get("servers", []):
            server = unwrap(raw)
            name = server.get("hostname")
            if not name:
                continue
            self.graph.add_node(name)
            self.node_types[name] = "server"
            for app in server.get("runs", []):
                self.graph.add_edge(name, app)

        # Teams
        for raw in data.get("teams", []):
            team = unwrap(raw)
            name = team.get("name")
            if not name:
                continue
            self.graph.add_node(name)
            self.node_types[name] = "team"
            for member in team.get("members", []):
                self.graph.add_edge(name, member)
            for tool in team.get("responsibilities", {}).get("owns_tools", []):
                self.graph.add_edge(name, tool)
            for app in team.get("responsibilities", {}).get("monitors_apps", []):
                self.graph.add_edge(name, app)
            for integration in team.get("responsibilities", {}).get("integrates_with", []):
                self.graph.add_edge(name, integration)
            for app in team.get("responsibilities", {}).get("owns_apps", []):
                self.graph.add_edge(name, app)
            for tool in team.get("responsibilities", {}).get("uses_tools", []):
                self.graph.add_edge(name, tool)
            for app in team.get("responsibilities", {}).get("responds_to", []):
                self.graph.add_edge(name, app)

        # Events
        for raw in data.get("events", []):
            event = unwrap(raw)
            name = event.get("id")
            if not name:
                continue
            self.graph.add_node(name)
            self.node_types[name] = "event"
            if "initiator" in event:
                self.graph.add_edge(event["initiator"], name)
            if "related_to" in event:
                related = event["related_to"]
                if isinstance(related, list):
                    for target in related:
                        self.graph.add_edge(name, target)
                else:
                    self.graph.add_edge(name, related)
            for sub in event.get("sub_events", []):
                self.graph.add_edge(name, sub)

        print(f"✅ Graph built: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges")

    def analyze_dependencies(self):
        bottlenecks = [node for node, deg in self.graph.in_degree() if deg > 1]
        isolated = [node for node in self.graph.nodes if self.graph.degree(node) == 0]
        return {
            "total_nodes": self.graph.number_of_nodes(),
            "bottlenecks": bottlenecks,
            "isolated_nodes": isolated
        }

    def visualize_system(self):
        pos = nx.kamada_kawai_layout(self.graph)
        fig, ax = plt.subplots(figsize=(12, 8))

        color_map = {
            "tool": "dodgerblue",
            "application": "lightgray",
            "person": "lightgreen",
            "server": "plum",
            "team": "orange",
            "event": "gold"
        }
        node_colors = [color_map.get(self.node_types.get(node, ""), "skyblue") for node in self.graph.nodes]

        nx.draw(
            self.graph,
            pos,
            with_labels=True,
            node_color=node_colors,
            edge_color='gray',
            node_size=2500,
            font_size=10,
            font_weight='bold',
            arrows=True,
            ax=ax
        )
        st.pyplot(fig)

    def analyze_perspectives_from_dict(self, data):
        perspectives_analysis = {}
        for raw in data.get("tools", []):
            tool = raw.get("data", raw)
            for perspective, evaluation in tool.get("perspectives", {}).items():
                perspectives_analysis.setdefault(perspective, []).append({
                    "component": tool["name"],
                    "type": "Tool",
                    "evaluation": evaluation
                })

        for raw in data.get("people", []):
            person = raw.get("data", raw)
            role_perspective = person.get("role", "General")
            perspectives_analysis.setdefault(role_perspective, []).append({
                "component": person["name"],
                "type": "Person",
                "uses_tools": person.get("uses_tools", [])
            })

        return perspectives_analysis
