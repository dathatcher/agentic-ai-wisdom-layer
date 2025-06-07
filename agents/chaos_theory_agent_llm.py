# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Production Framework – Chaos Theory Agent with Ripple Playback

from agents.agent_base import AgentBase
from utils.model_filter import summarize_model_for_agent
import openai
import os
import json
import re
import copy

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

        try:
            match = re.search(r'{.*}', raw, re.DOTALL)
            json_text = match.group(0) if match else raw
            return json_text
        except Exception as e:
            return json.dumps({
                "volatility_nodes": [],
                "feedback_loops": [],
                "emergent_risks": [],
                "fragile_paths": [],
                "llm_reasoning": f"Failed to parse response as JSON. Raw output:\n{raw}"
            }, indent=2)

    def simulate_ripple_step(self, model, event, step):
        updated_model = copy.deepcopy(model)
        ripple_log = updated_model.get("ripple_history", [])

        targets = event["target"] if isinstance(event["target"], list) else [event["target"]]
        affected_nodes = set()

        if event["type"] == "remove_person":
            for section in updated_model:
                if isinstance(updated_model[section], list):
                    for obj in list(updated_model[section]):
                        if "data" in obj:
                            values_copy = list(obj["data"].values())
                            for value in values_copy:
                                if isinstance(value, list):
                                    if any(t in value for t in targets):
                                        obj["data"]["status"] = "ripple_affected"
                                        affected_nodes.add(obj["data"].get("name") or obj["data"].get("hostname") or obj["data"].get("id"))
                                elif value in targets:
                                    obj["data"]["status"] = "ripple_affected"
                                    affected_nodes.add(obj["data"].get("name") or obj["data"].get("hostname") or obj["data"].get("id"))

        # Simple severity scoring based on affected count (out of 100)
        score = min(100, len(affected_nodes) * 10)

        ripple_log.append({
            "step": step,
            "event": event,
            "summary": f"{', '.join(targets)} removed. Ripple affected: {', '.join(sorted(affected_nodes)) or 'None'}",
            "severity_score": score,
            "llm_analysis": ""  # placeholder, will be updated by summarize_timestep
        })
        updated_model["ripple_history"] = ripple_log
        return updated_model

    def simulate_multi_step_ripple(self, model, origin_event, max_steps=3):
        current_model = copy.deepcopy(model)
        affected_this_round = set()
        all_affected = set()

        for step in range(1, max_steps + 1):
            step_summary = []
            ripple_event = {
                "type": origin_event["type"],
                "target": origin_event["target"] if step == 1 else list(affected_this_round)
            }
            current_model = self.simulate_ripple_step(current_model, ripple_event, step)
            affected_this_round.clear()

            for section in current_model:
                if isinstance(current_model[section], list):
                    for obj in current_model[section]:
                        if "data" in obj and obj["data"].get("status") == "ripple_affected":
                            node_id = obj["data"].get("name") or obj["data"].get("hostname") or obj["data"].get("id")
                            if node_id and node_id not in all_affected:
                                affected_this_round.add(node_id)
                                all_affected.add(node_id)

            # generate LLM summary for this step
            summary = self.summarize_timestep(current_model, step)
            current_model["ripple_history"][-1]["llm_analysis"] = summary

        return current_model

    def summarize_timestep(self, model, step):
        last_event = model.get("ripple_history", [])[-1]
        affected = []
        for section in model:
            if isinstance(model[section], list):
                for obj in model[section]:
                    if isinstance(obj, dict) and "data" in obj and isinstance(obj["data"], dict):
                        if obj["data"].get("status") == "ripple_affected":
                            affected.append(
                                obj["data"].get("name") or
                                obj["data"].get("hostname") or
                                obj["data"].get("id") or
                                "unknown"
                            )

        prompt = f"""
Ripple Simulation - Step {step}
Event: {last_event['event']}
Affected Nodes: {affected}

Summarize the emergent chaos effects and fragility from this event propagation.
Explain how the affected nodes are connected, what this implies about system vulnerability,
and what types of failure scenarios or systemic risks could emerge if these nodes fail together.
"""
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a chaos theory analyst summarizing system fragility and chaos evolution."},
                {"role": "user", "content": prompt.strip()}
            ],
            temperature=0.4
        )
        return response.choices[0].message.content.strip()
