# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Production Framework – Systems Thinking Agent

from agents.agent_base import AgentBase
from utils.model_filter import summarize_model_for_agent
import openai
import os
import json

class SystemsThinkingAgentLLM(AgentBase):
    def __init__(self, system_context="IT Organization"):
        super().__init__(role="Systems Thinking Agent", system_context=system_context)

    def analyze(self, system_model):
        custom_instructions = """
- Your task is to analyze the structure of the system and identify:
  1. 🔗 Bottlenecks: nodes/entities with many inbound dependencies
  2. 🧍 Isolated Nodes: entities with no significant relationships
  3. 🧠 Perspective Conflicts: areas where different roles or teams perceive the same entity differently
  4. 🔁 Feedback Loops: evidence of cycles or circular dependencies

- Output must be in JSON with the following structure:

{
  "bottlenecks": [...],
  "isolated_nodes": [...],
  "perspective_conflicts": [...],
  "feedback_loops": [...]
}
"""
        return self.prompt(system_model, custom_instructions)

    def smart_prompt(self, system_model, meta_context, user_question, diff_summary=None):
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        lite_model = summarize_model_for_agent(system_model, agent_type="systems", max_per_category=20)
        system_facts = json.dumps(lite_model, indent=2)
        meta_facts = json.dumps(meta_context, indent=2)
        diff_facts = json.dumps(diff_summary, indent=2) if diff_summary else "[]"

        full_prompt = f"""
You are a Systems Thinking Agent analyzing an IT organization.

Here is the current systems model:
{system_facts}

Here is the meta-context:
{meta_facts}

Recent structural changes (diff_summary):
{diff_facts}

Now, answer the following question:
{user_question}

Use DSRP (Distinctions, Systems, Relationships, Perspectives) if applicable.
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a systems thinking assistant analyzing complex adaptive systems."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
