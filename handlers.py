from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from tmdb_api import search_tmdb, get_media_details, get_poster_urls, get_logos
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
        'Help: /help \n'
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
        logos = get_logos(tmdb_id, media_type)
        
        # Edit the original message to remove buttons
        await query.edit_message_text(f"🎬 *{display_text}*", parse_mode='Markdown')
        
        # Send all available posters as direct links
        await send_links(update, display_text, poster_urls, logos)

async def send_links(update: Update, title: str, poster_urls: dict, logos: list):
    """Send all available image links to the chat."""
    message = f"🎬 *{title}*\n\n"
    
    # English Landscapes
    if poster_urls['english']['landscape']:
        message += "*English Landscapes:*\n"
        for url in poster_urls['english']['landscape'][:10]:
            message += f"{url}\n"
        message += "\n"
    
    # English Portraits
    if poster_urls['english']['portrait']:
        message += "*English Posters:*\n"
        for url in poster_urls['english']['portrait'][:10]:
            message += f"{url}\n"
        message += "\n"
    
    # Hindi Landscapes
    if poster_urls['hindi']['landscape']:
        message += "*Hindi Landscapes:*\n"
        for url in poster_urls['hindi']['landscape'][:10]:
            message += f"{url}\n"
        message += "\n"
    
    # Hindi Portraits
    if poster_urls['hindi']['portrait']:
        message += "*Hindi Posters:*\n"
        for url in poster_urls['hindi']['portrait'][:10]:
            message += f"{url}\n"
        message += "\n"
    
    # Logos
    if logos:
        message += "*English Logos:*\n"
        for url in logos[:5]:
            message += f"{url}\n"
    
    await update.callback_query.message.reply_text(
        text=message,
        parse_mode='Markdown'
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error('Exception while handling an update:', exc_info=context.error)
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            'An error occurred while processing your request. '
            'The developer has been notified.'
        )