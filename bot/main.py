import logging
from telegram.ext import Application
from .handlers import setup_handlers
from config import TELEGRAM_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start_bot():
    """Start the Telegram bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Setup all handlers
    setup_handlers(application)
    
    # Start the Bot
    logger.info("Bot starting...")
    application.run_polling()

if __name__ == '__main__':
    start_bot()