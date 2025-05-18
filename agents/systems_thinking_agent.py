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

        # Tools
        for tool in data.get("tools", []):
            tool_name = tool["name"]
            self.graph.add_node(tool_name)
            self.node_types[tool_name] = "tool"
            for app in tool["relationships"].get("monitors_applications", []):
                self.graph.add_edge(tool_name, app)
            for team in tool["relationships"].get("used_by_teams", []):
                self.graph.add_edge(team, tool_name)
            for integration in tool["relationships"].get("integrates_with", []):
                self.graph.add_edge(tool_name, integration)

        # Applications
        for app in data.get("applications", []):
            app_name = app["name"]
            self.graph.add_node(app_name)
            self.node_types[app_name] = "application"
            for server in app.get("deployed_on", []):
                self.graph.add_edge(app_name, server)
            for monitor in app.get("monitored_by", []):
                self.graph.add_edge(monitor, app_name)

        # People
        for person in data.get("people", []):
            person_name = person["name"]
            self.graph.add_node(person_name)
            self.node_types[person_name] = "person"
            for tool in person.get("uses_tools", []):
                self.graph.add_edge(person_name, tool)
            for team in person.get("teams", []):
                self.graph.add_edge(person_name, team)

        # Servers
        for server in data.get("servers", []):
            server_name = server["hostname"]
            self.graph.add_node(server_name)
            self.node_types[server_name] = "server"
            for app in server.get("runs", []):
                self.graph.add_edge(server_name, app)

        # Teams
        for team in data.get("teams", []):
            team_name = team["name"]
            self.graph.add_node(team_name)
            self.node_types[team_name] = "team"
            for member in team.get("members", []):
                self.graph.add_edge(team_name, member)
            for tool in team.get("responsibilities", {}).get("owns_tools", []):
                self.graph.add_edge(team_name, tool)
            for app in team.get("responsibilities", {}).get("monitors_apps", []):
                self.graph.add_edge(team_name, app)
            for integration in team.get("responsibilities", {}).get("integrates_with", []):
                self.graph.add_edge(team_name, integration)
            for app in team.get("responsibilities", {}).get("owns_apps", []):
                self.graph.add_edge(team_name, app)
            for used_tool in team.get("responsibilities", {}).get("uses_tools", []):
                self.graph.add_edge(team_name, used_tool)
            for responded_app in team.get("responsibilities", {}).get("responds_to", []):
                self.graph.add_edge(team_name, responded_app)

        # Events
        for event in data.get("events", []):
            event_id = event["id"]
            self.graph.add_node(event_id)
            self.node_types[event_id] = "event"
            if "initiator" in event:
                self.graph.add_edge(event["initiator"], event_id)
            if "related_to" in event:
              related = event["related_to"]
            if isinstance(related, list):
                for target in related:
                 self.graph.add_edge(event_id, target)
            else:
               self.graph.add_edge(event_id, related)
            for sub in event.get("sub_events", []):
                self.graph.add_edge(event_id, sub)

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

    def analyze_perspectives(self, json_filepath):
        with open(json_filepath) as f:
            data = json.load(f)
        return self.analyze_perspectives_from_dict(data)

    def analyze_perspectives_from_dict(self, data):
        perspectives_analysis = {}

        for tool in data.get("tools", []):
            for perspective, evaluation in tool.get("perspectives", {}).items():
                perspectives_analysis.setdefault(perspective, []).append({
                    "component": tool["name"],
                    "type": "Tool",
                    "evaluation": evaluation
                })

        for person in data.get("people", []):
            role_perspective = person.get("role", "General")
            perspectives_analysis.setdefault(role_perspective, []).append({
                "component": person["name"],
                "type": "Person",
                "uses_tools": person.get("uses_tools", [])
            })

        return perspectives_analysis
