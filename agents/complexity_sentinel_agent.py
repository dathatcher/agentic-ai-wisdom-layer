# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Simulation Framework
# For license and reuse contact: david.austin.thatcher@gmail.com

# complexity_sentinel_agent.py

def flatten(values):
    for v in values:
        if isinstance(v, list):
            yield from flatten(v)
        else:
            yield v

class ComplexitySentinelAgent:
    def __init__(self):
        self.changes = {}

    def detect_changes(self, old_graph, new_graph):
        old_nodes = set(old_graph.keys())
        new_nodes = set(new_graph.keys())

        added_nodes = list(new_nodes - old_nodes)
        removed_nodes = list(old_nodes - new_nodes)

        added_edges = []
        removed_edges = []

        for node in new_graph:
            new_targets = set(flatten(new_graph.get(node, [])))
            old_targets = set(flatten(old_graph.get(node, [])))
            for t in new_targets - old_targets:
                added_edges.append((node, t))
            for t in old_targets - new_targets:
                removed_edges.append((node, t))

        self.changes = {
            "added_nodes": added_nodes,
            "removed_nodes": removed_nodes,
            "added_edges": added_edges,
            "removed_edges": removed_edges
        }

        return self.changes
