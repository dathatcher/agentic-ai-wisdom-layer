# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Production Framework – Karma Agent

from agents.agent_base import AgentBase
from utils.model_filter import summarize_model_for_agent
import json

class KarmaAgentLLM(AgentBase):
    def __init__(self, system_context="IT Organization"):
        super().__init__(role="Karma Agent", system_context=system_context)

    def smart_prompt(self, system_model, meta_context, user_query, diff_summary=None):
        lite_model = summarize_model_for_agent(system_model, agent_type="karma", max_per_category=20)
        lite_meta = json.dumps(meta_context, indent=2)
        diff_facts = json.dumps(diff_summary, indent=2) if diff_summary else "[]"

        instructions = f"""
As the Karma Agent, your task is to evaluate the ethical and systemic consequences of actions within the organization.

Analyze:
  1. 📌 High-impact actions (positive or negative)
  2. ⚠️ Ethical fragility: high influence, low oversight
  3. ⚖️ Intent vs. Impact: good intentions with harm, or bad ones with unintended benefit
  4. 🌀 Moral feedback loops: ethical spirals over time

System Model:
{json.dumps(lite_model, indent=2)}

Meta-Context:
{lite_meta}

Recent Changes (diff_summary):
{diff_facts}

Now answer:
{user_query}
"""
        return self.prompt(lite_model, instructions)
