def summarize_model_for_agent(system_model, agent_type="default", max_per_category=5, max_relationships=50):
    """
    Reduce the size of the system model passed to LLM agents to avoid token limits.

    Args:
        system_model (dict): Full mental model loaded from JSON.
        agent_type (str): Placeholder for future agent-specific filters.
        max_per_category (int): Max entries to keep per top-level distinction.
        max_relationships (int): Max relationships to retain.

    Returns:
        dict: A summarized version of the system model.
    """
    summary = {}
    for category, entries in system_model.items():
        if not isinstance(entries, list):
            continue

        if category == "relationships":
            summary[category] = entries[:max_relationships]
        else:
            filtered = []
            for entry in entries[:max_per_category]:
                data = entry.get("data", entry)  # fallback if already reduced
                if isinstance(data, dict):
                    filtered.append(data)
            summary[category] = filtered

    return summary
