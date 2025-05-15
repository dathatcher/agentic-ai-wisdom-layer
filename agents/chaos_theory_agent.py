
import networkx as nx
import random

class ChaosTheoryAgent:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.volatility = {}  # Volatility score for each node (0 to 1)

    def load_system(self, components, decay_factor=0.6):
        """
        Loads a graph of system components and assigns volatility scores
        with ripple effects from connected nodes.
        """
        self.graph.clear()
        self.volatility.clear()

        # Build the graph
        for node, deps in components.items():
            for dep in deps:
                self.graph.add_edge(dep, node)

        # Step 1: Assign base volatility randomly
        base_volatility = {
            node: random.uniform(0.0, 1.0)
            for node in self.graph.nodes
        }

        # Step 2: Propagate volatility through ripple effect
        propagated_volatility = base_volatility.copy()
        for source, target in self.graph.edges:
            ripple = base_volatility[source] * decay_factor
            propagated_volatility[target] += ripple

        # Step 3: Normalize and round volatility scores
        for node, score in propagated_volatility.items():
            self.volatility[node] = round(min(score, 1.0), 2)

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
