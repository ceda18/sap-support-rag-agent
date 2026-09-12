from functools import lru_cache

from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

from core.config import settings

# SUMMARY:
# Builds the chat prompt: the agent rules are loaded from agent_rules.txt and sent as a
# system message, the retrieved context and the user question are sent as a human message.
# The system message is marked with cache_control so Anthropic caches it across requests.

USER_TEMPLATE = """<context>
{context}
</context>

Question from Slack user: {question}

Answer using only the context above, following your rules."""


@lru_cache
def load_agent_rules() -> str:
    """Read the rules file once per process."""
    with open(settings.RULES_PATH, "r", encoding="utf-8") as f:
        return f.read()


def build_prompt() -> ChatPromptTemplate:
    """System message (cached) + human message with the context and the question."""

    # A plain SystemMessage is used instead of a template so the text stays identical on
    # every request. Any change before the cache_control marker invalidates the cache.
    system_message = SystemMessage(
        content=[
            {
                "type": "text",
                "text": load_agent_rules(),
                "cache_control": {"type": "ephemeral"},
            }
        ]
    )

    return ChatPromptTemplate.from_messages(
        [system_message, HumanMessagePromptTemplate.from_template(USER_TEMPLATE)]
    )