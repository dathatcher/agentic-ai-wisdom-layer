
import random

class KarmaAgent:
    def __init__(self):
        self.impact_scores = {}

    def load_system(self, graph, events=None):
        self.impact_scores.clear()
        event_counts = {}

        # Count how many times a node appears in events
        if events:
            for event in events:
                initiator = event.get("initiator")
                if initiator:
                    event_counts[initiator] = event_counts.get(initiator, 0) + 1
                related = event.get("related_to")
                if related:
                    event_counts[related] = event_counts.get(related, 0) + 1
                for sub in event.get("sub_events", []):
                    event_counts[sub] = event_counts.get(sub, 0) + 1

        for node, edges in graph.items():
            node_type = self.infer_type(node, edges)
            base_intention = random.choice(["Positive", "Neutral", "Negative"])
            base_impact = random.uniform(0.1, 1.0)

            # Teams get higher impact if connected to many critical nodes
            if node_type == "team":
                connection_weight = len(edges)
                base_impact += 0.05 * connection_weight

            # Adjust impact based on event participation
            if node in event_counts:
                base_impact += 0.05 * min(event_counts[node], 6)  # cap bonus at +0.3

            impact = min(base_impact, 1.0)
            rating = self.score_to_rating(base_intention, impact)

            self.impact_scores[node] = {
                "type": node_type,
                "intention": base_intention,
                "impact_score": round(impact, 2),
                "karma_rating": rating
            }

    def infer_type(self, node, edges):
        if "Team" in node or "team" in node:
            return "team"
        elif "App" in node or "Service" in node:
            return "application"
        elif "VM" in node:
            return "server"
        elif " " in node:
            return "person"
        elif node.startswith(("JIRA-", "COMMIT", "JENKINS", "RELEASE")):
            return "event"
        else:
            return "tool"

    def score_to_rating(self, intention, impact):
        if intention == "Positive" and impact > 0.6:
            return "Positive"
        elif intention == "Negative" and impact > 0.4:
            return "Negative"
        else:
            return "Neutral"

    def report(self):
        return self.impact_scores
