
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
import json

class SystemsThinkingAgent:
    def __init__(self):
        self.graph = nx.DiGraph()

    def load_from_json(self, filepath):
        with open(filepath) as f:
            data = json.load(f)
        self.load_from_dict(data)

    def load_from_dict(self, data):
        self.graph.clear()

        # Tools
        for tool in data.get("tools", []):
            tool_name = tool["name"]
            self.graph.add_node(tool_name)
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
            for server in app.get("deployed_on", []):
                self.graph.add_edge(app_name, server)

        # People
        for person in data.get("people", []):
            person_name = person["name"]
            self.graph.add_node(person_name)
            for tool in person.get("uses_tools", []):
                self.graph.add_edge(person_name, tool)

        # Servers
        for server in data.get("servers", []):
            server_name = server["hostname"]
            self.graph.add_node(server_name)
            for app in server.get("runs", []):
                self.graph.add_edge(server_name, app)

    def analyze_dependencies(self):
        bottlenecks = [node for node, deg in self.graph.in_degree() if deg > 1]
        isolated = [node for node in self.graph.nodes if self.graph.degree(node) == 0]
        return {
            "total_nodes": self.graph.number_of_nodes(),
            "bottlenecks": bottlenecks,
            "isolated_nodes": isolated
        }

    def visualize_system(self):
        pos = nx.spring_layout(self.graph)
        fig, ax = plt.subplots()
        nx.draw(
            self.graph,
            pos,
            with_labels=True,
            node_color='skyblue',
            edge_color='gray',
            node_size=2000,
            font_size=10,
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
