"""
AWS Cloud Practitioner Certification Prep Agent using Strands SDK
"""
import re
import json
from strands import Agent

SYSTEM_PROMPT = """You are an AWS Cloud Practitioner certification exam question generator.

CRITICAL: Return ONLY the JSON object below. Do NOT include any explanations, commentary, or additional fields.

Required JSON format (nothing else):
{
  "question": "string",
  "options": {
    "A": "string",
    "B": "string",
    "C": "string",
    "D": "string"
  },
  "correct_answer": "A"
}

FORBIDDEN:
- Do NOT add "explanation" field
- Do NOT add any other fields
- Do NOT include markdown formatting
- Do NOT include any text outside the JSON

Generate realistic AWS Cloud Practitioner exam questions with exactly 4 multiple choice options."""

def create_agent() -> Agent:
    # Create Strands Agent with specified system prompt and model
    return Agent(
        model="amazon.nova-pro-v1:0",
        system_prompt=SYSTEM_PROMPT)

def _parse_agent_output(output) -> dict:
    """
    Parse agent output and STRICTLY enforce schema.
    Extra fields (like 'explanation') are discarded.
    """

    import json
    import re

    # Extract text from Strands envelope
    if isinstance(output, dict) and "content" in output:
        content = output.get("content", [])
        text = content[0].get("text", "") if content else ""
    elif isinstance(output, str):
        text = output
    elif isinstance(output, dict):
        text = json.dumps(output)
    else:
        text = str(output)

    # Remove markdown
    text = re.sub(r"```json|```", "", text).strip()

    # Extract first JSON object only
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found in agent output:\n{text}")

    parsed = json.loads(match.group(0))

    # ✅ HARD SCHEMA ENFORCEMENT
    required_keys = {"question", "options", "correct_answer"}

    cleaned = {
        "question": parsed.get("question"),
        "options": parsed.get("options"),
        "correct_answer": parsed.get("correct_answer")
    }

    # Validate structure
    if not cleaned["question"] or not isinstance(cleaned["options"], dict):
        raise ValueError(f"Invalid question format:\n{parsed}")

    if set(cleaned["options"].keys()) != {"A", "B", "C", "D"}:
        raise ValueError("Options must contain exactly A, B, C, D")

    if cleaned["correct_answer"] not in {"A", "B", "C", "D"}:
        raise ValueError("correct_answer must be A, B, C, or D")

    return cleaned

def generate_question(agent: Agent) -> dict:
    response = agent("Generate one AWS Cloud Practitioner practice question.")
    
    return _parse_agent_output(response)
    