
# complexity_sentinel_agent.py

import json
import difflib

class ComplexitySentinelAgent:
    def __init__(self):
        self.previous_snapshot = {}

    def load_snapshot(self, current_snapshot):
        """
        Accepts a new system snapshot (flattened dict of components and connections)
        """
        changes = self.detect_emergent_changes(current_snapshot)
        self.previous_snapshot = current_snapshot
        return changes

    def detect_emergent_changes(self, current_snapshot):
        """
        Compares current snapshot with previous and returns emergent differences
        """
        changes = {
            "new_nodes": [],
            "removed_nodes": [],
            "changed_relationships": []
        }

        prev_nodes = set(self.previous_snapshot.keys())
        curr_nodes = set(current_snapshot.keys())

        changes["new_nodes"] = list(curr_nodes - prev_nodes)
        changes["removed_nodes"] = list(prev_nodes - curr_nodes)

        for node in curr_nodes & prev_nodes:
            prev_conns = set(self.previous_snapshot.get(node, []))
            curr_conns = set(current_snapshot.get(node, []))
            if prev_conns != curr_conns:
                changes["changed_relationships"].append({
                    "node": node,
                    "before": list(prev_conns),
                    "after": list(curr_conns)
                })

        return changes
