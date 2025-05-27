# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Production Framework – Karma Agent

from agents.agent_base import AgentBase
from utils.model_filter import summarize_model_for_agent
import openai
import os
import json
import re

class KarmaAgentLLM(AgentBase):
    def __init__(self, system_context="IT Organization"):
        super().__init__(role="Karma Agent", system_context=system_context)

    def smart_prompt(self, system_model, meta_context, user_query, diff_summary=None):
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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

Respond strictly in this JSON format:
{{
  "ethical_actors": [...],
  "fragile_roles": [...],
  "intent_impact_gaps": [...],
  "moral_feedback_loops": [...],
  "llm_reasoning": "..."
}}
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a karma analyst evaluating ethical risk, intent, and impact in IT systems."},
                {"role": "user", "content": instructions}
            ],
            temperature=0.3
        )

        raw = response.choices[0].message.content.strip()

        # Extract valid JSON block or fallback
        try:
            match = re.search(r'{.*}', raw, re.DOTALL)
            json_text = match.group(0) if match else raw
            return json_text
        except Exception as e:
            return json.dumps({
                "ethical_actors": [],
                "fragile_roles": [],
                "intent_impact_gaps": [],
                "moral_feedback_loops": [],
                "llm_reasoning": f"Failed to parse JSON. Raw LLM output: {raw}"
            }, indent=2)
