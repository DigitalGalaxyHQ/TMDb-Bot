from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineQueryResultPhoto
)
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    InlineQueryHandler,
    filters
)
from tmdb_api import search_tmdb, get_media_details, get_poster_urls, get_logo_url
import logging
import uuid

logger = logging.getLogger(__name__)

def setup_handlers(application):
    """Register all bot handlers."""
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("tmdb", tmdb_search))
    application.add_handler(CallbackQueryHandler(handle_button_press))
    application.add_handler(InlineQueryHandler(inline_search))   # 🔥 Inline mode
    application.add_error_handler(error_handler)

# ──────────────────────────────── BASIC COMMANDS ────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 *Welcome to TMDB Bot!* \n\n"
        "Type `/tmdb <movie or series name>` to search.\n"
        "Or use me inline anywhere like:\n"
        "`@YourBotUsername Interstellar`",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 *Help Menu*\n\n"
        "Commands:\n"
        "/tmdb <query> – Search TMDB\n"
        "/help – This message\n\n"
        "You can also use me inline by typing:\n"
        "`@YourBotUsername Avengers`",
        parse_mode="Markdown"
    )

# ──────────────────────────────── SEARCH HANDLER ────────────────────────────────
async def tmdb_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("⚠️ Please provide a movie or TV show name.")
        return

    results = search_tmdb(query)
    if not results:
        await update.message.reply_text("❌ No results found.")
        return

    buttons = []
    for r in results[:5]:
        title = r.get("title") or r.get("name")
        media_type = r.get("media_type", "movie")
        buttons.append([
            InlineKeyboardButton(title, callback_data=f"{media_type}:{r['id']}")
        ])

    await update.message.reply_text(
        f"🔍 Results for *{query}*:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ──────────────────────────────── CALLBACK HANDLER ────────────────────────────────
async def handle_button_press(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    media_type, tmdb_id = query.data.split(":")
    details = get_media_details(tmdb_id, media_type)
    title = details.get("title") or details.get("name")
    overview = details.get("overview", "No description available.")
    poster_data = get_poster_urls(tmdb_id, media_type)
    poster_path = None

    if poster_data.get("posters"):
        poster_path = poster_data["posters"][0]["file_path"]

    text = f"*{title}*\n\n_{overview}_"
    if poster_path:
        image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        await query.message.reply_photo(photo=image_url, caption=text, parse_mode="Markdown")
    else:
        await query.message.reply_text(text, parse_mode="Markdown")

# ──────────────────────────────── INLINE MODE 🔥 ────────────────────────────────
async def inline_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip()
    if not query:
        return
    results = search_tmdb(query)
    articles = []

    for item in results[:15]:
        title = item.get("title") or item.get("name")
        overview = item.get("overview", "")[:150]
        media_type = item.get("media_type", "movie")
        logo_url = get_logo_url(item.get("id"), media_type)

        if logo_url:
            articles.append(
                InlineQueryResultPhoto(
                    id=str(uuid.uuid4()),
                    photo_url=logo_url,
                    thumb_url=logo_url,
                    caption=f"🎬 *{title}*\n_{overview}_",
                    parse_mode="Markdown"
                )
            )
        else:
            articles.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title=title,
                    description=overview,
                    input_message_content=InputTextMessageContent(
                        message_text=f"🎬 *{title}*\n{overview}",
                        parse_mode="Markdown"
                    )
                )
            )

    await update.inline_query.answer(articles, cache_time=1)

# ──────────────────────────────── ERROR LOGGER ────────────────────────────────
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Exception while handling update:", exc_info=context.error)