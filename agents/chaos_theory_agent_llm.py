# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Production Framework – Chaos Theory Agent

from agents.agent_base import AgentBase
from utils.model_filter import summarize_model_for_agent
import openai
import os
import json
import re

class ChaosTheoryAgentLLM(AgentBase):
    def __init__(self, system_context="IT Organization"):
        super().__init__(role="Chaos Theory Agent", system_context=system_context)

    def smart_prompt(self, system_model, meta_context, user_query, diff_summary=None):
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        lite_model = summarize_model_for_agent(system_model, agent_type="chaos", max_per_category=20)
        system_facts = json.dumps(lite_model, indent=2)
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
{system_facts}

Meta Context:
{meta_facts}

Recent Changes (diff_summary):
{diff_facts}

Now answer:
{user_query}

Respond only in JSON format with structure like:
{{
  "volatility_nodes": [...],
  "feedback_loops": [...],
  "emergent_risks": [...],
  "fragile_paths": [...],
  "llm_reasoning": "..."
}}
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a chaos theory analyst detecting instability and volatility in complex adaptive systems."},
                {"role": "user", "content": instructions}
            ],
            temperature=0.3
        )

        raw = response.choices[0].message.content.strip()

        # Try to extract valid JSON using regex
        try:
            match = re.search(r'{.*}', raw, re.DOTALL)
            json_text = match.group(0) if match else raw
            return json_text  # Let the dashboard handle final parsing
        except Exception as e:
            # Fallback JSON shell
            return json.dumps({
                "volatility_nodes": [],
                "feedback_loops": [],
                "emergent_risks": [],
                "fragile_paths": [],
                "llm_reasoning": f"Failed to parse response as JSON. Raw output:\n{raw}"
            }, indent=2)
