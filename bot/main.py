import logging
from telegram.ext import Application
from .handlers import setup_handlers
from config import TELEGRAM_TOKEN
from aiohttp import web
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def health_check(request):
    """Basic health check endpoint for Render.com"""
    return web.Response(text="Bot is running")

async def start_server_and_bot():
    """Start both the Telegram bot and a minimal HTTP server"""
    # Create Telegram bot application
    bot_app = Application.builder().token(TELEGRAM_TOKEN).build()
    setup_handlers(bot_app)

    # Start the bot in polling mode (non-blocking)
    await bot_app.initialize()
    await bot_app.start()
    logger.info("Bot started in polling mode")

    # Create a minimal HTTP server for Render
    app = web.Application()
    app.router.add_get("/", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Bind to Render's provided port
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"HTTP server started on port {port}")

    # Keep both running
    while True:
        await asyncio.sleep(3600)  # Sleep forever while keeping the bot alive

if __name__ == '__main__':
    import asyncio
    asyncio.run(start_server_and_bot())