# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Production Framework – Chaos Theory Agent

from agents.agent_base import AgentBase
import openai
import os
import json

class ChaosTheoryAgentLLM(AgentBase):
    def __init__(self, system_context="IT Organization"):
        super().__init__(role="Chaos Theory Agent", system_context=system_context)

    def analyze(self, system_model):
        custom_instructions = """
- Your role is to apply principles of Chaos Theory to assess systemic fragility, instability, and feedback loops.
- You should evaluate:
  1. 🌪 Volatility Nodes: elements where small changes could cause ripple effects
  2. ♻️ Feedback Loops: cycles of influence or dependency
  3. ⚠️ Fragile Points: nodes or connections highly susceptible to perturbation

- Use terms from complex adaptive systems, including non-linearity, sensitivity to initial conditions, and path dependency.

- Output must be in structured JSON with:
{
  "volatile_nodes": [...],
  "feedback_loops": [...],
  "fragile_points": [...]
}

Be specific and justify results.
"""
        return self.prompt(system_model, custom_instructions)

    def smart_prompt(self, system_model, meta_context, user_question):
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        system_facts = json.dumps(system_model, indent=2)
        meta_facts = json.dumps(meta_context, indent=2)

        system_context = f"""
You are a Chaos Theory Agent analyzing a complex adaptive system in an IT organization.
This agent focuses on instability, ripple risk, nonlinear feedback, and emergent behavior.

System model:
{system_facts}

Metadata (heuristics, domain assumptions, volatility markers):
{meta_facts}
"""

        full_prompt = f"""{system_context}

Now answer this question:
{user_question}

Return a structured answer in JSON or bullet points. Explain ripple risk and systemic instability if applicable.
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Chaos Theory analyst for complex IT systems, modeling volatility, nonlinearity, and ripple propagation."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.4
        )

        return response.choices[0].message.content.strip()
