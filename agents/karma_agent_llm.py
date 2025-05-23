# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Production Framework – Karma Agent

from agents.agent_base import AgentBase
from utils.model_filter import summarize_model_for_agent
import json

class KarmaAgentLLM(AgentBase):
    def __init__(self, system_context="IT Organization"):
        super().__init__(role="Karma Agent", system_context=system_context)

    def smart_prompt(self, system_model, meta_context, user_query):
        # Reduce input for token-safe operation
        lite_model = summarize_model_for_agent(system_model, agent_type="karma", max_per_category=10)
        lite_meta = json.dumps(meta_context, indent=2)

        instructions = f"""
- As the Karma Agent, your task is to evaluate the ethical and systemic consequences of actions within the organization.
- Analyze actors (teams, individuals) and their roles in:
  1. 📌 High-impact actions (positive or negative)
  2. ⚠️ Ethical fragility: when influence is high but actions lack oversight or moral weight
  3. ⚖️ Intent vs. Impact: good intentions may have harmful consequences, or vice versa
  4. 🌀 Moral feedback loops: recurring decisions that amplify effects over time

- Consider both the system model and meta-context below when forming your answer.
- If events exist, assess their origin, associated actors, and ripple effects.

System Model:
{json.dumps(lite_model, indent=2)}

Meta-Context:
{lite_meta}

Now answer the user question:
{user_query}
"""

        return self.prompt(lite_model, instructions)
