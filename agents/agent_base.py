
# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Production Framework
# BaseAgent class for all LLM-powered cognitive agents

import openai
import os
import json
from typing import Any, Dict

class AgentBase:
    def __init__(self, role: str, system_context: str = "IT Organization"):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.role = role
        self.system_context = system_context

    def prompt(self, system_model: Dict[str, Any], custom_instructions: str = "") -> str:
        base_prompt = f"""You are a Wisdom Layer Agent assigned the role: {self.role}.

The system being modeled is: {self.system_context}

You will be given a structured mental model (in JSON) representing entities, relationships, roles, and events.

Instructions:
- Think in terms of Systems Thinking, Chaos Theory, Karma, or Complexity (depending on your agent role).
- Use distinctions, dependencies, feedback loops, and ripple effects as needed.
- Return only JSON or clearly formatted explanation with headings.

{custom_instructions}

Here is the current mental model:
{json.dumps(system_model, indent=2)}

Respond below with your full analysis.
"""

        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": f"You are the {self.role} of an agentic AI system."},
                {"role": "user", "content": base_prompt}
            ]
        )

        return response.choices[0].message.content.strip()
