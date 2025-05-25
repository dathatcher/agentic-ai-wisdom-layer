# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Production Framework – Chaos Theory Agent

from agents.agent_base import AgentBase
from utils.model_filter import summarize_model_for_agent
import json

class ChaosTheoryAgentLLM(AgentBase):
    def __init__(self, system_context="IT Organization"):
        super().__init__(role="Chaos Theory Agent", system_context=system_context)

    def smart_prompt(self, system_model, meta_context, user_query, diff_summary=None):
        lite_model = summarize_model_for_agent(system_model, agent_type="chaos", max_per_category=20)
        meta_facts = json.dumps(meta_context, indent=2)
        diff_facts = json.dumps(diff_summary, indent=2) if diff_summary else "[]"

        instructions = f"""
As the Chaos Theory Agent, your task is to assess systemic volatility, feedback amplification, and tipping points.

Consider:
- Propagation of failure or stress
- Small causes with large effects
- Node volatility and ripple potential
- Hidden interdependencies and chaos amplifiers

System Model:
{json.dumps(lite_model, indent=2)}

Meta Context:
{meta_facts}

Recent Changes (diff_summary):
{diff_facts}

Now answer:
{user_query}
"""
        return self.prompt(lite_model, instructions)
