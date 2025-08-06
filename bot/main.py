import logging
from telegram.ext import Application
from .handlers import setup_handlers
from config import TELEGRAM_TOKEN
from aiohttp import web
import os
import asyncio

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def health_check(request):
    return web.Response(text="Bot is running")

async def run_bot():
    """Run the Telegram bot"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    setup_handlers(application)
    
    await application.initialize()
    await application.start()
    logger.info("Bot started in polling mode")
    
    # Start polling
    await application.updater.start_polling()
    return application

async def run_server():
    """Run the HTTP server for Render"""
    app = web.Application()
    app.router.add_get("/", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"HTTP server started on port {port}")
    return runner

async def main():
    """Main entry point"""
    bot = await run_bot()
    server = await run_server()
    
    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await server.cleanup()
        await bot.stop()

if __name__ == '__main__':
    asyncio.run(main())