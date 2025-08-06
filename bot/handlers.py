from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,  # Changed from CallbackContext
    MessageHandler,
    filters  # Changed from Filters
)
from .tmdb_api import search_tmdb, get_media_details, get_poster_urls

def setup_handlers(dispatcher):
    """Setup all Telegram bot handlers."""
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('tmdb', tmdb_search))
    dispatcher.add_handler(CallbackQueryHandler(handle_button_press))
    dispatcher.add_error_handler(error_handler)

def start(update: Update, context: CallbackContext) -> None:
    """Send welcome message."""
    update.message.reply_text(
        '🎬 Welcome to TMDB Poster Bot!\n\n'
        'Search for movies/TV shows and get their posters.\n\n'
        'Usage: /tmdb <query>\n'
        'Example: /tmdb The Dark Knight'
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Send help message."""
    update.message.reply_text(
        '🔍 TMDB Poster Bot Help:\n\n'
        '/tmdb <query> - Search for movies or TV shows\n'
        'Example: /tmdb Inception\n\n'
        'The bot will show available posters in both landscape and portrait formats.'
    )

def tmdb_search(update: Update, context: CallbackContext) -> None:
    """Handle /tmdb command to search for media."""
    query = ' '.join(context.args)
    if not query:
        update.message.reply_text('Please provide a search query. Example: /tmdb Inception')
        return
    
    results = search_tmdb(query)
    if not results:
        update.message.reply_text('No results found for your search.')
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
    
    update.message.reply_text(
        'Please select the correct title:',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def handle_button_press(update: Update, context: CallbackContext) -> None:
    """Handle button presses from inline keyboards."""
    query = update.callback_query
    query.answer()
    
    if query.data.startswith('select_'):
        _, media_type, tmdb_id = query.data.split('_')
        details = get_media_details(tmdb_id, media_type)
        
        if not details:
            query.edit_message_text('Sorry, there was an error fetching details.')
            return
        
        title = details.get('title') or details.get('name')
        year = details.get('release_date', details.get('first_air_date', '')).split('-')[0]
        display_text = f"{'🎬' if media_type == 'movie' else '📺'} {title}"
        if year:
            display_text += f" ({year})"
        
        # Get all poster URLs
        poster_urls = get_poster_urls(tmdb_id, media_type)
        
        # Edit the original message to remove buttons
        query.edit_message_text(f"Fetching posters for: {display_text}")
        
        # Send all available posters
        send_posters(update, display_text, poster_urls)

def send_posters(update: Update, title: str, poster_urls: dict):
    """Send all available posters to the chat."""
    # English posters
    if poster_urls['english']['landscape']:
        update.callback_query.message.reply_photo(
            photo=poster_urls['english']['landscape'],
            caption=f"{title} - English Landscape"
        )
    
    if poster_urls['english']['portrait']:
        update.callback_query.message.reply_photo(
            photo=poster_urls['english']['portrait'],
            caption=f"{title} - English Portrait"
        )
    
    # Hindi posters
    if poster_urls['hindi']['landscape']:
        update.callback_query.message.reply_photo(
            photo=poster_urls['hindi']['landscape'],
            caption=f"{title} - Hindi Landscape"
        )
    
    if poster_urls['hindi']['portrait']:
        update.callback_query.message.reply_photo(
            photo=poster_urls['hindi']['portrait'],
            caption=f"{title} - Hindi Portrait"
        )

def error_handler(update: Update, context: CallbackContext) -> None:
    """Log errors caused by updates."""
    from telegram.error import TelegramError
    import traceback
    
    logger.error('Exception while handling an update:', exc_info=context.error)
    
    if update and update.effective_message:
        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
        tb_string = ''.join(tb_list)
        
        # Notify user about the error
        update.effective_message.reply_text(
            'An error occurred while processing your request. '
            'The developer has been notified.'
        )
        
        # Log the full error
        logger.error(f"Update {update} caused error {context.error}\n{tb_string}")
