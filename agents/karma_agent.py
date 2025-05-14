# karma_agent.py

import random

class KarmaAgent:
    def __init__(self):
        self.karma_ledger = {}  # Stores karma score for each component

    def load_system(self, components):
        """
        Loads a flattened graph model (same format as chaos agent).
        Calculates karma based on synthetic intention and impact patterns.
        """
        self.karma_ledger.clear()
        for node, connections in components.items():
            intent = self.simulate_intention(node)
            impact = self.simulate_impact(node)
            karma_score = self.calculate_karma(intent, impact)
            self.karma_ledger[node] = {
                "intention": intent,
                "impact_score": impact,
                "karma_rating": karma_score
            }

    def simulate_intention(self, node):
        """
        Assigns a placeholder intention (could be learned later)
        """
        return random.choice(["Efficiency", "Monitoring", "Compliance", "Collaboration", "Resilience"])

    def simulate_impact(self, node):
        """
        Simulates an ethical or operational impact score (0 to 1)
        """
        return round(random.uniform(0.0, 1.0), 2)

    def calculate_karma(self, intention, impact_score):
        """
        Simple logic: If impact is high and intention is 'positive', karma is good.
        """
        if impact_score >= 0.7:
            return "Positive"
        elif 0.4 <= impact_score < 0.7:
            return "Neutral"
        else:
            return "Negative"

    def report(self):
        """
        Returns full karma ratings for all nodes
        """
        return self.karma_ledger
