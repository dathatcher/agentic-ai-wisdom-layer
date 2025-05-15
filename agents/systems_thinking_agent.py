
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
import json

class SystemsThinkingAgent:
    def __init__(self):
        self.graph = nx.DiGraph()

    def load_from_json(self, filepath):
        """
        Builds the system graph from a JSON schema
        """
        with open(filepath) as f:
            data = json.load(f)

        self.graph.clear()

        # Tools relationships
        for tool in data.get("tools", []):
            tool_name = tool["name"]
            for app in tool["relationships"].get("monitors_applications", []):
                self.graph.add_edge(tool_name, app)

            for team in tool["relationships"].get("used_by_teams", []):
                self.graph.add_edge(team, tool_name)

            for integration in tool["relationships"].get("integrates_with", []):
                self.graph.add_edge(tool_name, integration)

        for app in data.get("applications", []):
            for server in app.get("deployed_on", []):
                self.graph.add_edge(app["name"], server)

        for person in data.get("people", []):
            for tool in person.get("uses_tools", []):
                self.graph.add_edge(person["name"], tool)

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

        perspectives_analysis = {}

        # Perspectives from tools
        for tool in data.get("tools", []):
            for perspective, evaluation in tool.get("perspectives", {}).items():
                perspectives_analysis.setdefault(perspective, []).append({
                    "component": tool["name"],
                    "type": "Tool",
                    "evaluation": evaluation
                })

        # Perspectives from people based on role
        for person in data.get("people", []):
            role_perspective = person.get("role", "General")
            perspectives_analysis.setdefault(role_perspective, []).append({
                "component": person["name"],
                "type": "Person",
                "uses_tools": person.get("uses_tools", [])
            })

        return perspectives_analysis
