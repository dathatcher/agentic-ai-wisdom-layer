import json
from agents.chaos_theory_agent_llm import ChaosTheoryAgentLLM

# Load the current model from your file
with open("systems_model.json") as f:
    model = json.load(f)

# Initialize the agent
chaos_agent = ChaosTheoryAgentLLM()

# Define a sample ripple event (remove Jane Doe)
event = {
    "type": "remove_person",
    "target": "Jane Doe"
}

# Simulate ripple step
step = 1
updated_model = chaos_agent.simulate_ripple_step(model, event, step=step)

# Print affected nodes for sanity check
print(f"\nRipple History:\n{updated_model.get('ripple_history', [])}")

# Get LLM summary
summary = chaos_agent.summarize_timestep(updated_model, step=step)

print("\n🔍 Chaos Agent Summary:")
print(summary)

# Optional: Save the result to see model evolution
with open("systems_model_ripple_step1.json", "w") as f:
    json.dump(updated_model, f, indent=2)
