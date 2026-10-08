"""Small helpers shared by every eval script that calls an LLM."""
import json


def message_text(message) -> str:
    """Return only the text of a reply (same logic as parse_answer in app/rag/generator.py).

    Anthropic can return a list of content blocks (thinking + text); thinking blocks
    have no "text" key, so they are dropped here.
    """
    content = message.content
    if isinstance(content, list):
        content = "".join(b.get("text", "") for b in content if isinstance(b, dict))
    return str(content).strip()


def parse_json_reply(text: str) -> dict:
    """Parse the JSON object in a reply, ignoring ```json fences or stray text around it."""
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON object found in the reply")
    return json.loads(text[start:end + 1])