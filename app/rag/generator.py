from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage

from core.config import settings

# SUMMARY:
# LLM layer built on LangChain's ChatAnthropic. Besides creating the model, this module
# reads the token usage from the response (including cached tokens), calculates the cost,
# and strips the [NO_ANSWER] / [OUT_OF_SCOPE] tags before the answer reaches the user.

NO_ANSWER_TAG = "[NO_ANSWER]"
OUT_OF_SCOPE_TAG = "[OUT_OF_SCOPE]"

# LLM Management

def build_llm() -> ChatAnthropic:
    """Create the Claude model used by the chain."""
    return ChatAnthropic(
        model=settings.ANTHROPIC_MODEL,
        api_key=settings.ANTHROPIC_API_KEY,
        max_tokens=settings.MAX_TOKENS,
        #temperature=0,
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

# Cost Estimation Helpers

# USD per 1M tokens. Cache writes cost 1.25x input, cache reads cost 0.1x input.
PRICING = {
    "claude-sonnet-5": {"input": 2.00, "output": 10.00},
    "claude-opus-5": {"input": 5.00, "output": 25.00},
    "claude-haiku-4-5-20251001": {"input": 1.00, "output": 5.00},
}
DEFAULT_PRICING = {"input": 2.00, "output": 10.00}

def extract_usage(message: AIMessage) -> dict:
    """Read the token counts from the response. Cached tokens prove the prompt cache was hit."""
    usage = message.response_metadata.get("usage", {})

    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    cache_creation = usage.get("cache_creation_input_tokens", 0)
    cache_read = usage.get("cache_read_input_tokens", 0)
    total_input = input_tokens + cache_creation + cache_read

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_creation_tokens": cache_creation,
        "cache_read_tokens": cache_read,
        "total_input_tokens": total_input,
        "cache_hit_ratio": round(cache_read / total_input, 2) if total_input else 0.0,
    }


def estimate_cost(usage: dict, model: str) -> float:
    """Estimate the cost of a single request in USD."""
    price = PRICING.get(model, DEFAULT_PRICING)

    cost = (
        usage["input_tokens"] * price["input"]
        + usage["cache_creation_tokens"] * price["input"] * 1.25
        + usage["cache_read_tokens"] * price["input"] * 0.1
        + usage["output_tokens"] * price["output"]
    ) / 1_000_000

    return round(cost, 6)