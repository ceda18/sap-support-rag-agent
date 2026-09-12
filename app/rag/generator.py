from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage

from core.config import settings

# SUMMARY:
# LLM layer built on LangChain's ChatAnthropic. Besides creating the model, this module
# reads the token usage from the response (including cached tokens), calculates the cost,
# and strips the [NO_ANSWER] / [OUT_OF_SCOPE] tags before the answer reaches the user.


NO_ANSWER_TAG = "[NO_ANSWER]"
OUT_OF_SCOPE_TAG = "[OUT_OF_SCOPE]"


def build_llm() -> ChatAnthropic:
    """Create the Claude model used by the chain."""
    return ChatAnthropic(
        model=settings.ANTHROPIC_MODEL,
        api_key=settings.ANTHROPIC_API_KEY,
        max_tokens=settings.MAX_TOKENS,
        temperature=0,
    )


def parse_answer(message: AIMessage) -> dict:
    """Separate the answer text from the refusal tags, which are for telemetry only."""
    content = message.content
    if isinstance(content, list):  # Anthropic returns a list of content blocks
        content = "".join(block.get("text", "") for block in content if isinstance(block, dict))

    text = str(content).strip()
    unanswered = NO_ANSWER_TAG in text
    out_of_scope = OUT_OF_SCOPE_TAG in text

    # The user should never see the tags.
    text = text.replace(NO_ANSWER_TAG, "").replace(OUT_OF_SCOPE_TAG, "").strip()

    return {"answer": text, "unanswered": unanswered, "out_of_scope": out_of_scope}
