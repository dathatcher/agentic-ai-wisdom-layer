# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Production Framework – Systems Thinking Agent

from agents.agent_base import AgentBase
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

Be as specific and structured as possible.
"""
        return self.prompt(system_model, custom_instructions)

    def smart_prompt(self, system_model, meta_context, user_question):
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        system_facts = json.dumps(system_model, indent=2)
        meta_facts = json.dumps(meta_context, indent=2)

        system_context = f"""
You are a Systems Thinking Agent analyzing an IT organization.
Below is the structured systems model:
{system_facts}

And here is metadata describing architectural context and domain-specific heuristics:
{meta_facts}
"""

        full_prompt = f"""{system_context}

Now, answer the following question:
{user_question}

Provide a clear and structured response. If applicable, include:
- Key nodes or subsystems involved
- Reasoning using distinctions, relationships, or perspectives (DSRP)
- Any implications for systems design or behavior
Return the result as formatted JSON or bullet points where applicable.
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": "You are a systems thinking assistant analyzing complex adaptive systems."
            }, {
                "role": "user",
                "content": full_prompt
            }],
            temperature=0.3
        )

        return response.choices[0].message.content.strip()
