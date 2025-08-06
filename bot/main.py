import logging
from telegram.ext import Updater
from .handlers import setup_handlers
from config import TELEGRAM_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start_bot():
    """Start the Telegram bot."""
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    
    # Setup all handlers
    setup_handlers(dispatcher)
    
    # Start the Bot
    updater.start_polling()
    logger.info("Bot started and running...")
    updater.idle()

if __name__ == '__main__':
    start_bot()
