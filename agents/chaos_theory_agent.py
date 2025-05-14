# chaos_theory_agent.py

import networkx as nx
import random

class ChaosTheoryAgent:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.volatility = {}  # Volatility score for each node (0 to 1)

    def load_system(self, components):
        """
        Loads a graph of system components and assigns random volatility scores.
        """
        self.graph.clear()
        self.volatility.clear()
        for node, deps in components.items():
            for dep in deps:
                self.graph.add_edge(dep, node)

        # Assign random volatility scores between 0 and 1
        for node in self.graph.nodes:
            self.volatility[node] = round(random.uniform(0.0, 1.0), 2)

    def detect_feedback_loops(self):
        """
        Detects cycles (feedback loops) in the system.
        """
        return list(nx.simple_cycles(self.graph))

    def analyze_instability(self):
        """
        Returns nodes with high volatility and feedback loops.
        """
        unstable_nodes = [node for node, score in self.volatility.items() if score > 0.7]
        feedback_loops = self.detect_feedback_loops()
        return {
            "volatile_nodes": unstable_nodes,
            "feedback_loops": feedback_loops,
            "volatility_scores": self.volatility
        }
