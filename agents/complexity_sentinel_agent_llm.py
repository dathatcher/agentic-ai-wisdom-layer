# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Production Agent – Complexity Sentinel (LLM-Powered)

from agents.agent_base import AgentBase
import json
import os
import re
import openai

class ComplexitySentinelAgentLLM(AgentBase):
    def __init__(self, system_context="IT Organization"):
        super().__init__(role="Complexity Sentinel Agent", system_context=system_context)

    def smart_prompt(self, current_model, previous_model, meta_context, user_query):
        if previous_model is None:
            return "🕰️ No previous model loaded. Please upload a second model to compare system evolution."

        lite_current = flatten_for_diff(current_model)
        lite_previous = flatten_for_diff(previous_model)
        diff_summary = compute_diff_summary(lite_current, lite_previous)

        print("[🧠 DEBUG] DIFF SUMMARY:")
        print(json.dumps(diff_summary, indent=2))

        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        full_prompt = f"""
You are the Complexity Sentinel Agent. You detect **structural changes** and **emerging complexity** in a system's evolution.

You are provided two models:
- `previous`: the earlier mental model snapshot
- `current`: the new snapshot
Each is organized by system categories (e.g., Infrastructure, Applications, Teams). Each contains arrays of structured data and optional reasoning.

You are also given a machine-generated `diff_summary` array containing changes:
{json.dumps(diff_summary, indent=2)}

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

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a Complexity Sentinel Agent for system evolution detection."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.3
            )

            raw = response.choices[0].message.content.strip()
            match = re.search(r'{.*}', raw, re.DOTALL)
            json_text = match.group(0) if match else raw
            return json_text

        except Exception as e:
            return json.dumps({
                "change_summary": [],
                "fragile_areas": [],
                "complexity_risks": [],
                "insights": [],
                "llm_reasoning": f"LLM failure: {str(e)}"
            }, indent=2)

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

    for category in set(current.keys()).union(previous.keys()):
        current_items = {json.dumps(e, sort_keys=True) for e in current.get(category, [])}
        previous_items = {json.dumps(e, sort_keys=True) for e in previous.get(category, [])}

        added = current_items - previous_items
        removed = previous_items - current_items

        for item in added:
            summary.append({"type": "added_node", "entity": json.loads(item)})
        for item in removed:
            summary.append({"type": "removed_node", "entity": json.loads(item)})

    return summary
