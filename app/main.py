import os
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from dotenv import load_dotenv

load_dotenv()

# Adapting logging configuration for initialization
logger = logging.getLogger("uvicorn.error")

# Initialize the Slack AsyncApp with the bot token from environment variables
slack_app = AsyncApp(token=os.environ.get("SLACK_BOT_TOKEN"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    app_token = os.environ.get("SLACK_APP_TOKEN")
    logger.info(f"🐛 DEBUG: SLACK_APP_TOKEN exists: {bool(app_token)}")
    
    if app_token:
        try:
            handler = AsyncSocketModeHandler(slack_app, app_token)
            asyncio.create_task(handler.start_async())
            logger.info("✅ Slack Socket Mode handler: running")
        except Exception as e:
            logger.error(f"❌ Error starting Slack handler: {e}")
    else:
        logger.warning("SLACK_APP_TOKEN is not set in environment!")
    yield

# Actual FastAPI application instance
app = FastAPI(
    title="SAP Support RAG Agent",
    version="1.0.0",
    lifespan=lifespan
)

# Initial Slack chatbot test message to indicate that the bot is running
@slack_app.event("app_mention")
async def handle_mention(event, say):
    """React to mentions of the bot (@SAP Support RAG Agent)."""
    user = event.get("user")
    await say(f"Hi <@{user}>! I'm here. My RAG brain is currently loading...")

@app.get("/health")
async def health_check():
    """Health-check endpoint for checking the status of the container."""
    return {"status": "healthy", "service": "SAP-Support-RAG-Agent"}