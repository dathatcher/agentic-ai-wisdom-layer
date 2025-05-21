
# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Production Framework – Systems Thinking Agent

from agents.agent_base import AgentBase

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
