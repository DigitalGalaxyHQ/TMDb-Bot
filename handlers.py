from telegram import Update, InputMediaPhoto
from telegram.ext import CommandHandler, ContextTypes
import requests
from config import TMDB_API_KEY

async def tmdb_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a movie or series name. Example:\n/tmdb Avengers Endgame")
        return

    query = " ".join(context.args)
    search_url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(search_url).json()

    if not response.get("results"):
        await update.message.reply_text("No results found.")
        return

    # Pick first result
    item = response["results"][0]
    item_id = item["id"]
    media_type = item.get("media_type", "movie")

    # Get images (poster, backdrop, logo)
    images_url = f"https://api.themoviedb.org/3/{media_type}/{item_id}/images?api_key={TMDB_API_KEY}"
    images = requests.get(images_url).json()

    poster_path = images["posters"][0]["file_path"] if images.get("posters") else None
    backdrop_path = images["backdrops"][0]["file_path"] if images.get("backdrops") else None
    logo_path = images["logos"][0]["file_path"] if images.get("logos") else None

    base_url = "https://image.tmdb.org/t/p/original"

    photos = []
    if poster_path:
        photos.append(InputMediaPhoto(base_url + poster_path))
    if backdrop_path:
        photos.append(InputMediaPhoto(base_url + backdrop_path))
    if logo_path:
        photos.append(InputMediaPhoto(base_url + logo_path))

    if not photos:
        await update.message.reply_text("Images not found for this title.")
        return

    # Send as album with caption
    photos[0].caption = item.get("title") or item.get("name") or "Unknown Title"
    await update.message.reply_media_group(media=photos)

def setup_handlers(application):
    application.add_handler(CommandHandler("tmdb", tmdb_command))