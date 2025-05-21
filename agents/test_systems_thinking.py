# test_systems_thinking.py

from systems_thinking_agent_llm import SystemsThinkingAgentLLM
import json

# Load the classified mental model
with open("../systems_model.json") as f:
    system_model = json.load(f)

# Create the agent
agent = SystemsThinkingAgentLLM(system_context="IT Organization")

# Run analysis
results = agent.analyze(system_model)

# Print results
print("🧠 Systems Thinking Agent Results:")
print(results)
