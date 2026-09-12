import asyncio
import re
from functools import lru_cache

from langchain_core.documents import Document

from rag.generator import build_llm, parse_answer
from rag.prompts import build_prompt
from rag.retriever import build_retriever, format_docs

# SUMMARY:
# Connects the pieces into one RAG call: retrieve chunks, render them into the prompt,
# send it to Claude, parse the answer. answer_question() is the only function the Slack
# layer needs to know about.


@lru_cache
def get_retriever():
    """Built once per process, since it loads the chunks file and the embedding model."""
    return build_retriever()


@lru_cache
def get_chain():
    """The LCEL chain: prompt -> Claude."""
    return build_prompt() | build_llm()


CITATION_PATTERN = re.compile(r"p\.\s*(\d+)")


def list_sources(docs: list[Document], answer: str) -> list[dict]:
    """Only the pages actually cited in the answer, not every page that was retrieved."""
    cited = {int(p) for p in CITATION_PATTERN.findall(answer)}
    seen = []
    for d in docs:
        if d.metadata.get("page") not in cited:
            continue
        item = {"source": d.metadata.get("source", "unknown"), "page": d.metadata.get("page")}
        if item not in seen:
            seen.append(item)
    return seen


async def answer_question(question: str) -> dict:
    """Run the full RAG flow for a single question."""
    # PGVector runs on a sync driver (psycopg2), so the search goes to a thread
    # instead of ainvoke, which would require an async engine.
    docs = await asyncio.to_thread(get_retriever().invoke, question)
    message = await get_chain().ainvoke({"context": format_docs(docs), "question": question})

    result = parse_answer(message)
    result["sources"] = list_sources(docs, result["answer"])

    # TODO: add token usage and cost here (extract_usage / estimate_cost) before the n8n phase.

    return result