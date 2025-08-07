from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from .tmdb_api import search_tmdb, get_media_details, get_poster_urls
import logging

logger = logging.getLogger(__name__)

def setup_handlers(application):
    """Setup all Telegram bot handlers."""
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('tmdb', tmdb_search))
    application.add_handler(CallbackQueryHandler(handle_button_press))
    application.add_error_handler(error_handler)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message."""
    await update.message.reply_text(
        '🎬 Welcome to TMDB Poster Bot!\n\n'
        'Search for movies/TV shows and get their posters.\n\n'
        'Usage: /tmdb <query>\n'
        'Example: /tmdb The Dark Knight'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help message."""
    await update.message.reply_text(
        '🔍 TMDB Poster Bot Help:\n\n'
        '/tmdb <query> - Search for movies or TV shows\n'
        'Example: /tmdb Inception\n\n'
        'The bot will show available posters in both landscape and portrait formats.'
    )

async def tmdb_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /tmdb command to search for media."""
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text('Please provide a search query. Example: /tmdb Inception')
        return
    
    results = search_tmdb(query)
    if not results:
        await update.message.reply_text('No results found for your search.')
        return
    
    keyboard = []
    for result in results[:10]:  # Show first 10 results
        media_type = '🎬' if result['media_type'] == 'movie' else '📺'
        title = result.get('title') or result.get('name')
        year = result.get('release_date', result.get('first_air_date', '')).split('-')[0]
        display_text = f"{media_type} {title}"
        if year:
            display_text += f" ({year})"
        
        keyboard.append([InlineKeyboardButton(
            display_text,
            callback_data=f"select_{result['media_type']}_{result['id']}"
        )])
    
    await update.message.reply_text(
        'Please select the correct title:',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_button_press(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses from inline keyboards."""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith('select_'):
        _, media_type, tmdb_id = query.data.split('_')
        details = get_media_details(tmdb_id, media_type)
        
        if not details:
            await query.edit_message_text('Sorry, there was an error fetching details.')
            return
        
        title = details.get('title') or details.get('name')
        year = details.get('release_date', details.get('first_air_date', '')).split('-')[0]
        display_text = f"{'🎬' if media_type == 'movie' else '📺'} {title}"
        if year:
            display_text += f" ({year})"
        
        # Get all poster URLs
        poster_urls = get_poster_urls(tmdb_id, media_type)
        
        # Edit the original message to remove buttons
        await query.edit_message_text(f"Fetching posters for: {display_text}")
        
        # Send all available posters
        await send_posters(update, display_text, poster_urls)

async def send_posters(update: Update, title: str, poster_urls: dict):
    """Send all available posters to the chat."""
    # English posters
    if poster_urls['english']['landscape']:
        await update.callback_query.message.reply_photo(
            photo=poster_urls['english']['landscape'],
            caption=f"{title} - English Landscape"
        )
    
    if poster_urls['english']['portrait']:
        await update.callback_query.message.reply_photo(
            photo=poster_urls['english']['portrait'],
            caption=f"{title} - English Portrait"
        )
    
    # Hindi posters
    if poster_urls['hindi']['landscape']:
        await update.callback_query.message.reply_photo(
            photo=poster_urls['hindi']['landscape'],
            caption=f"{title} - Hindi Landscape"
        )
    
    if poster_urls['hindi']['portrait']:
        await update.callback_query.message.reply_photo(
            photo=poster_urls['hindi']['portrait'],
            caption=f"{title} - Hindi Portrait"
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error('Exception while handling an update:', exc_info=context.error)
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            'An error occurred while processing your request. '
            'The developer has been notified.'
      )
