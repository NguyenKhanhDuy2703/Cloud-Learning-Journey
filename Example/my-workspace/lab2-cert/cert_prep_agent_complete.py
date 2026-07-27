import json
import re
from strands import Agent
from mcp import StdioServerParameters, stdio_client
from strands.tools.mcp import MCPClient

knowledge_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx",
            args= ["awslabs.aws-documentation-mcp-server@latest"]
        )
    )
)

SYSTEM_PROMPT = """You are an AWS Cloud Practitioner certification exam assistant.

Follow these rules strictly:
1. FIRST generate the question from your own knowledge (do NOT use tools).
2. AFTER the question is generated, use knowledge tools to:
   - Validate the correct answer
   - Fetch official AWS documentation URLs
   - Find additional learning resources
3. ALWAYS return VALID JSON ONLY in the format below.
4. DO NOT include markdown, commentary, or extra text.

Create comprehensive explanations that help users learn by including:
- Why the correct answer is right
- Why each incorrect answer is wrong
- Key concepts and definitions
- Real-world use cases and examples
- Best practices and common pitfalls
- Official AWS documentation links
- Related services and concepts to explore

Output format:
{
  "question": "string",
  "options": {
    "A": "string",
    "B": "string",
    "C": "string",
    "D": "string"
  },
  "correct_answer": "A",
  "explanation": "Comprehensive explanation covering: 1) Why the correct answer is right with specific details, 2) Why each incorrect option is wrong, 3) Key concepts and definitions, 4) Real-world use cases, 5) Best practices, 6) Common mistakes to avoid, 7) Official AWS documentation links from docs.aws.amazon.com, 8) Related services to explore for deeper learning"
}
"""
def create_agent() -> Agent:
    with knowledge_client:
        return Agent(
            model="amazon.nova-pro-v1:0",
            tools=knowledge_client.list_tools_sync(),
            system_prompt=SYSTEM_PROMPT
        )
def _parse_agent_output(output) -> dict:
    """
    Handles Strands agent outputs:
    - dict (already parsed JSON)
    - assistant message envelope
    - raw string
    - markdown-wrapped JSON
    """

    # Case 1: Already a parsed dict
    if isinstance(output, dict) and "question" in output:
        return output

    text = None

    # Case 2: Strands message envelope
    if isinstance(output, dict) and "content" in output:
        content = output.get("content", [])
        if content and isinstance(content, list):
            text = content[0].get("text")

    # Case 3: String output
    elif isinstance(output, str):
        text = output

    # Case 4: Fallback to string conversion
    else:
        text = str(output)

    if not isinstance(text, str):
        raise ValueError(f"Agent returned non-text output: {type(text)}")

    # Strip markdown fences if present
    text = re.sub(r"```json|```", "", text).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from agent output:\n{text}") from e


def generate_question(agent: Agent) -> dict:
    with knowledge_client:
        response = agent(
            "Generate one AWS Cloud Practitioner practice question and explanations linking documentation."
        )

    return _parse_agent_output(response)
