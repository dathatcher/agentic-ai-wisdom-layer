# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Production Agent – Complexity Sentinel (LLM-Powered)

from agents.agent_base import AgentBase
from utils.model_filter import summarize_model_for_agent
import json

class ComplexitySentinelAgentLLM(AgentBase):
    def __init__(self, system_context="IT Organization"):
        super().__init__(role="Complexity Sentinel Agent", system_context=system_context)

    def smart_prompt(self, current_model, previous_model, meta_context, user_query):
        if previous_model is None:
            return "🕰️ No previous model loaded. Please upload a second model to compare system evolution."

        lite_current = flatten_for_diff(current_model)
        lite_previous = flatten_for_diff(previous_model)
        diff_summary = compute_diff_summary(lite_current, lite_previous)

        instructions = f"""
You are the Complexity Sentinel Agent. You detect **structural changes** and **emerging complexity** in a system's evolution.

You are provided two models:
- `previous`: the earlier mental model snapshot
- `current`: the new snapshot
Each is organized by system categories (e.g., Infrastructure, Applications, Teams). Each contains arrays of structured data and optional reasoning.

You are also given a machine-generated `diff_summary` array containing changes.

Your tasks:
1. Summarize and interpret the differences.
2. Detect any fragility:
   - e.g., new nodes with many dependencies, removals breaking existing links
3. Highlight complexity or risk signals:
   - Increased node count, entropy, missing connections
4. Return a structured analysis in this JSON format:

{{
  "change_summary": [...],
  "fragile_areas": [...],
  "complexity_risks": [...],
  "insights": [...],
  "llm_reasoning": "..."
}}

System context: {self.system_context}
User question: {user_query}
"""

        return self.prompt({
            "previous": lite_previous,
            "current": lite_current,
            "diff_summary": diff_summary,
            "meta": meta_context
        }, instructions)

def flatten_for_diff(model):
    clean = {}
    for category, items in model.items():
        clean[category] = []
        for item in items:
            if isinstance(item, dict) and "data" in item:
                clean[category].append(item["data"])
            else:
                clean[category].append(item)
    return clean

def compute_diff_summary(current, previous):
    summary = []

    for category in current:
        current_items = {json.dumps(e, sort_keys=True) for e in current.get(category, [])}
        previous_items = {json.dumps(e, sort_keys=True) for e in previous.get(category, [])}

        added = current_items - previous_items
        removed = previous_items - current_items

        for item in added:
            summary.append({"type": "added_node", "entity": json.loads(item)})
        for item in removed:
            summary.append({"type": "removed_node", "entity": json.loads(item)})

    return summary
