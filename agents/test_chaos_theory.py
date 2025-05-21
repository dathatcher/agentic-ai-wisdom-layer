# test_chaos_theory.py
# © 2025 David Thatcher. All rights reserved.

from chaos_theory_agent_llm import ChaosTheoryAgentLLM
import json
import os

# Ensure your API key is set in the environment
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "your-api-key-here"  # Replace or set via terminal

# Load the classified mental model
with open("../systems_model.json") as f:
    system_model = json.load(f)

# Load metadata if available
meta_context = {}
try:
    with open("../meta.json") as f:
        meta_context = json.load(f)
except FileNotFoundError:
    print("[Warning] meta.json not found — proceeding without metadata.\n")

# Create Chaos Theory Agent
agent = ChaosTheoryAgentLLM(system_context="IT Organization")

# Run default chaos analysis
print("\n🔍 Chaos Theory Agent — Structural Analysis:\n")
chaos_results = agent.analyze(system_model)
print(chaos_results)

# Run Smart Prompt query
print("\n🤖 Smart Prompt Query:\n")
question = "What areas of our system have high volatility or are fragile to small changes?"
smart_result = agent.smart_prompt(system_model, meta_context, question)
print(smart_result)
