# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Production Agent – Complexity Sentinel (LLM-Powered)

from agents.agent_base import AgentBase

class ComplexitySentinelAgentLLM(AgentBase):
    def __init__(self, system_context="IT Organization"):
        super().__init__(role="Complexity Sentinel Agent", system_context=system_context)

    def smart_prompt(self, current_model, previous_model, meta_context, user_query):
        instructions = f"""
You are the Complexity Sentinel Agent. Your role is to:
  1. Detect and interpret **structural changes** between a previous and current system model.
  2. Identify **fragility zones** caused by added or removed nodes and relationships.
  3. Highlight **emergent complexity patterns** or entropy spikes.
  4. Integrate both **mental model data** and **meta reasoning** for a holistic view.

Use this structure in JSON output:
{{
  "change_summary": [{{"type": "added_node|removed_node|added_edge|removed_edge", "entity": "..."}}],
  "fragile_areas": ["..."],
  "complexity_risks": ["..."],
  "insights": ["..."],
  "llm_reasoning": "..."
}}

Your system context is: {self.system_context}.
The user question is: {user_query}
"""
        return self.prompt({
            "previous": previous_model,
            "current": current_model,
            "meta": meta_context
        }, instructions)
