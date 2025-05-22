# © 2025 David Thatcher. All rights reserved.
# Wisdom Layer Production Framework – Karma Agent (LLM Powered)

from agents.agent_base import AgentBase

class KarmaAgentLLM(AgentBase):
    def __init__(self, system_context="IT Organization"):
        super().__init__(role="Karma Agent", system_context=system_context)

    def smart_prompt(self, system_model, meta_context, user_query):
        instructions = f"""
You are the Karma Agent in a Wisdom Layer AI system.

Your job is to assess the moral alignment, ethical fragility, and underutilized intentions across this system.

---

### 👁 Guidance for Karma Evaluation:

1. **Intent vs. Impact**
   - Positive intent + low impact = underleveraged
   - Negative intent + high impact = ethically risky
   - No intent data = flag as missing or misclassified

2. **Moral Feedback Loops**
   - Does an actor repeatedly trigger high-impact changes?
   - Could small actions lead to systemic consequences?

3. **Relationship-Based Influence**
   - If a TEAM owns a TOOL, and that TOOL affects APPLICATIONS → the TEAM inherits moral responsibility.
   - If a PERSON uses a TOOL that is critical or volatile → they may have invisible leverage.

4. **Call Out Anomalies**
   - Missing monitoring links (e.g., team owns tool, but isn’t using it)
   - Silos or duplication
   - Orphans with high influence but no traceable ownership

---

### 🧭 Output Format (if appropriate):
- Actor: [Name]
- Role/Type: [Team, Person, Tool...]
- Intent: [Positive/Neutral/Negative]
- Impact Summary: [Short reasoning]
- Ethical Rating: [High/Low Risk or Positive/Neutral/Negative]
- Comments: [Optional recommendations or concerns]

---

Use both the `system_model` and `meta_context` (mental model metadata) when answering.

Now evaluate:
{user_query}
"""
        return self.prompt(system_model, instructions)
