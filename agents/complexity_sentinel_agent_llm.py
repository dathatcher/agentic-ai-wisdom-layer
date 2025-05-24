# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Production Agent – Complexity Sentinel (LLM-Powered)

from agents.agent_base import AgentBase
from utils.model_filter import summarize_model_for_agent
import json

class ComplexitySentinelAgentLLM(AgentBase):
    def __init__(self, system_context="IT Organization"):
        super().__init__(role="Complexity Sentinel Agent", system_context=system_context)

    def smart_prompt(self, current_model, previous_model, meta_context, user_query):
        # ✅ Handle first-run when no previous model is available
        if previous_model is None:
            return "🕰️ No previous model loaded. Please upload a second model to compare system evolution."

        # ✅ Safely summarize both models to avoid token overflow
        lite_current = summarize_model_for_agent(current_model, agent_type="sentinel", max_per_category=10)
        lite_previous = summarize_model_for_agent(previous_model, agent_type="sentinel", max_per_category=10)

        instructions = f"""
You are the Complexity Sentinel Agent. You detect **structural changes** and **emerging complexity** in a system's evolution.

You are provided two models:
- `previous`: the earlier mental model snapshot
- `current`: the new snapshot
Each is organized by system categories (e.g., Infrastructure, Applications, Teams). Each contains arrays of structured data and optional reasoning.

Your tasks:
1. Compare both models and identify structural diffs:
   - Nodes added or removed in any category
   - Changes in relationships or properties
2. Detect any fragility:
   - e.g., new nodes with many dependencies, removals breaking existing links
3. Highlight complexity or risk signals:
   - Increased node count, entropy, missing connections
4. Combine findings into this JSON structure:

{{
  "change_summary": [{{"type": "added_node|removed_node|added_edge|removed_edge", "entity": "..."}}],
  "fragile_areas": ["..."],
  "complexity_risks": ["..."],
  "insights": ["..."],
  "llm_reasoning": "..."
}}

System context: {self.system_context}
User question: {user_query}
"""

        return self.prompt({
            "previous": lite_previous,
            "current": lite_current,
            "meta": meta_context
        }, instructions)
