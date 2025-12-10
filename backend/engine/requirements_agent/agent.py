from typing import Any, Dict, List
import json

from backend.engine.requirements_agent.spec_schema import SPEC_SCHEMA
from backend.engine.requirements_agent.spec_model import SpecificationModel
from backend.llm.llm_manager import LLM
from backend.utils.logger import debug


class RequirementsAgent:
    """
    Requirements collection agent that:
    - Enforces SPEC_SCHEMA strictly
    - Asks only one question at a time
    - Suggests missing information proactively
    - Helps the user refine vague specs
    """

    def __init__(self):
        pass

    # =====================================================================
    # PUBLIC ENTRY POINT
    # =====================================================================
    def run(
        self,
        user_message: str,
        current_spec: Any,
        history: List[Dict[str, str]],
    ) -> Dict[str, Any]:

        debug("RequirementsAgent.run() called")
        debug(f"User message: {user_message}")

        # Normalize spec -> model
        spec_model = self._build_spec_model(current_spec)
        spec_dict = spec_model.to_dict()
        missing_required = spec_model.missing_required_fields()

        debug(f"Current spec:\n{json.dumps(spec_dict, indent=2)}")
        debug(f"Missing required fields: {missing_required}")

        # PROACTIVE ANALYSIS
        proactive_suggestion = self._infer_suggestions(spec_dict)

        # Build strict prompt
        prompt = self._build_prompt(
            user_message, spec_dict, history, missing_required, proactive_suggestion
        )
        debug(f"RequirementsAgent prompt:\n{prompt}")

        # Call LLM
        llm_output = LLM.generate_json(prompt)
        debug(f"Raw LLM JSON output: {llm_output}")

        updated_fields = llm_output.get("updated_fields", {}) or {}
        reply = llm_output.get("reply")
        follow_up = llm_output.get("follow_up_question")

        # fallback logic
        if not reply and follow_up:
            reply = follow_up
        if not reply:
            reply = "Could you clarify what you want next?"

        needs_more = bool(follow_up or updated_fields or missing_required)

        cleaned_updates = self._clean_updates(updated_fields)
        debug(f"Cleaned updated_fields: {json.dumps(cleaned_updates, indent=2)}")
        debug(f"Reply to user: {reply}")
        debug(f"Needs_more: {needs_more}")

        return {
            "reply": reply,
            "updated_fields": cleaned_updates,
            "needs_more": needs_more,
        }

    # =====================================================================
    # INTERNAL HELPERS
    # =====================================================================

    def _build_spec_model(self, current_spec: Any) -> SpecificationModel:
        model = SpecificationModel()
        if isinstance(current_spec, SpecificationModel):
            model.update(current_spec.to_dict())
        elif isinstance(current_spec, dict):
            model.update(current_spec)
        return model

    # ------------------------------------------------------------------
    # PROACTIVE SUGGESTION ENGINE (NO ONTOLOGY NEEDED)
    # ------------------------------------------------------------------
    def _infer_suggestions(self, spec: Dict[str, Any]) -> List[str]:
        suggestions = []

        # If agents exist but roles are empty
        if spec.get("agents") and not spec.get("agent_purposes"):
            suggestions.append(
                "You added agents but not their roles. Would you like to define what each agent type does?"
            )

        # If many agents but no communication defined
        if spec.get("agents") and not spec.get("communication"):
            suggestions.append(
                "Since your system has multiple agents, you may want to define how they communicate."
            )

        # If topology is missing
        if spec.get("agents") and not spec.get("topology"):
            suggestions.append(
                "Agent topology is missing. Should agents be connected in a hierarchy, peer-to-peer, or something else?"
            )

        # If memory missing
        if not spec.get("memory"):
            suggestions.append(
                "Would you like the system to use memory? (None, shared memory, or per-agent memory.)"
            )

        # If planning missing
        if not spec.get("planning"):
            suggestions.append(
                "Some multi-agent systems include a planning component. Should your system include planning?"
            )

        return suggestions

    # ------------------------------------------------------------------
    # FIELD SCHEMA DESCRIPTION FOR LLM
    # ------------------------------------------------------------------
    def _schema_field_description(self, name: str, meta: Dict[str, Any]) -> str:
        required = "required" if meta.get("required") else "optional"
        ftype = meta.get("type")
        desc = meta.get("description", "")
        ask = meta.get("ask_user", "")
        example = meta.get("example", "")

        text = [
            f"- {name} ({required}, type={ftype}): {desc}",
            f"  Ask user: {ask}",
        ]
        if example:
            text.append(f"  Example: {example}")

        if "structure" in meta:
            struct = meta["structure"]
            keys = list(struct.keys())

            ex_obj = {
                k: ("<string>" if t == "string" else 0)
                for k, t in struct.items()
            }

            if ftype == "list":
                text.append(f"  This is a LIST of OBJECTS with keys: {keys}")
                text.append(f"  Example: [ {json.dumps(ex_obj)} ]")
            else:
                text.append(f"  This is an OBJECT with keys: {keys}")
                text.append(f"  Example: {json.dumps(ex_obj)}")

        return "\n".join(text)

    def _schema_summary(self) -> str:
        return "\n\n".join(
            self._schema_field_description(name, meta)
            for name, meta in SPEC_SCHEMA.items()
        )

    # ------------------------------------------------------------------
    # STRICT JSON PROMPT
    # ------------------------------------------------------------------
    def _build_prompt(
        self,
        user_message: str,
        spec_dict: Dict[str, Any],
        history: List[Dict[str, str]],
        missing_required: List[str],
        proactive_suggestions: List[str],
    ) -> str:

        # Build history snippet
        history_text = ""
        for msg in history[-6:]:
            role = "User" if msg["role"] == "user" else "Assistant"
            history_text += f"{role}: {msg['content']}\n"

        schema_text = self._schema_summary()
        suggestion_text = "\n".join(f"- {s}" for s in proactive_suggestions)

        return f"""
You are the Requirements Agent.

Your JSON output MUST strictly follow the schema.

===================================================
SCHEMA YOU MUST FOLLOW:
===================================================
{schema_text}

===================================================
CURRENT SPEC:
{json.dumps(spec_dict, indent=2)}

MISSING REQUIRED:
{missing_required}

PROACTIVE SUGGESTIONS:
{suggestion_text}

CONVERSATION HISTORY:
{history_text}

USER MESSAGE:
{user_message}

===================================================
NOW OUTPUT STRICT JSON ONLY:
{{
  "updated_fields": {{
      // Only fields from SPEC_SCHEMA
  }},
  "reply": "Friendly natural-language reply that may include one suggestion.",
  "follow_up_question": "ONE question that moves the spec forward. Use proactive suggestions when helpful."
}}
===================================================
""".strip()

    # ------------------------------------------------------------------
    def _clean_updates(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(updates, dict):
            return {}
        return {k: v for k, v in updates.items() if k in SPEC_SCHEMA}
