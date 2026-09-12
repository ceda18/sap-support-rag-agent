import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

from core.config import settings
from rag.chain import answer_question, get_retriever

logger = logging.getLogger("uvicorn.error")

slack_app = AsyncApp(token=settings.SLACK_BOT_TOKEN)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Build the retriever now so the first Slack question is not slowed down by it.
    await asyncio.to_thread(get_retriever)
    logger.info("✅ Retriever ready")

    if settings.SLACK_APP_TOKEN:
        handler = AsyncSocketModeHandler(slack_app, settings.SLACK_APP_TOKEN)
        asyncio.create_task(handler.start_async())
        logger.info("✅ Slack Socket Mode handler: running")
    else:
        logger.warning("SLACK_APP_TOKEN is not set in environment!")
    yield


app = FastAPI(
    title="SAP Support RAG Agent",
    version="1.0.0",
    lifespan=lifespan
)


def format_sources(sources: list[dict]) -> str:
    """One line listing the pages the answer came from."""
    if not sources:
        return ""
    pages = sorted({s["page"] for s in sources}, key=lambda p: (not str(p).isdigit(), str(p).zfill(6)))
    return f"\n\n_📄 {sources[0]['source']} — pages: {', '.join(str(p) for p in pages)}_"


async def handle_question(text: str, say):
    """Shared logic for mentions and direct messages."""
    question = text.split(">", 1)[-1].strip()  # drop the leading <@BOT_ID> from mentions
    if not question:
        await say("Ask me something about SAP PaPM.")
        return

    try:
        result = await answer_question(question)
        await say(result["answer"] + format_sources(result["sources"]))
    except Exception as e:
        logger.error(f"❌ Error answering question: {e}")
        await say("Something went wrong while answering. Check the API logs.")


@slack_app.event("app_mention")
async def handle_mention(event, say):
    """React to mentions of the bot (@SAP Support RAG Agent)."""
    await handle_question(event.get("text", ""), say)


@slack_app.event("message")
async def handle_direct_message(event, say):
    """React to direct messages, ignoring the bot's own messages."""
    if event.get("channel_type") != "im" or event.get("bot_id"):
        return
    await handle_question(event.get("text", ""), say)


@app.get("/health")
async def health_check():
    """Health-check endpoint for checking the status of the container."""
    return {"status": "healthy", "service": "SAP-Support-RAG-Agent"}