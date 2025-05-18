# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Simulation Framework
# For license and reuse contact: david.austin.thatcher@gmail.com

import networkx as nx
import random

class ChaosTheoryAgent:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.volatility = {}

    def load_system(self, components, decay_factor=0.6):
     import random
     self.graph.clear()
     self.volatility.clear()

     # Build graph edges
     for node, deps in components.items():
        for dep in deps:
            if isinstance(dep, list):
                for d in dep:
                    self.graph.add_edge(d, node)
            else:
                self.graph.add_edge(dep, node)

    # Assign base volatility (boost for events/releases)
     base_volatility = {}
     for node in self.graph.nodes:
        if "RELEASE" in node or node.startswith(("JIRA-", "COMMIT", "JENKINS", "INC-")):
            base_volatility[node] = random.uniform(0.6, 1.0)
        else:
            base_volatility[node] = random.uniform(0.0, 1.0)

     propagated_volatility = base_volatility.copy()

    # Propagate ripple (with decay, normalized by fan-out)
     reverse_graph = nx.reverse_view(self.graph)
     for source, target in self.graph.edges:
        out_degree = len(list(reverse_graph.successors(source))) or 1
        ripple = (base_volatility[source] * decay_factor) / out_degree
        propagated_volatility[target] += ripple

    # Normalize and clamp
     for node, score in propagated_volatility.items():
        self.volatility[node] = round(min(score, 1.0), 2)

    def detect_feedback_loops(self):
        return list(nx.simple_cycles(self.graph))

    def analyze_instability(self):
        unstable_nodes = [node for node, score in self.volatility.items() if score > 0.7]
        feedback_loops = self.detect_feedback_loops()
        return {
            "volatile_nodes": unstable_nodes,
            "feedback_loops": feedback_loops,
            "volatility_scores": self.volatility
        }
