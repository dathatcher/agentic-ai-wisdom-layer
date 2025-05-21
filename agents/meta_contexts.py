# agents/meta_contexts.py

def get_meta_context(system_model):
    return {
        "description": "System model representing an IT organization including people, tools, apps, and infrastructure.",
        "components": list(system_model.keys()),
        "note": "Used to assist LLM agents in contextual reasoning across systems."
    }
