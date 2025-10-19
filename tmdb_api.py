import requests
from config import TMDB_API_KEY, TMDB_BASE_URL, TMDB_IMAGE_BASE_URL

def search_tmdb(query: str) -> list:
    """Search TMDB for movies and TV shows."""
    search_url = f"{TMDB_BASE_URL}/search/multi?api_key={TMDB_API_KEY}&query={query}&language=en-US"
    response = requests.get(search_url)
    if response.status_code != 200:
        return []
    return response.json().get("results", [])

def get_media_details(tmdb_id: str, media_type: str) -> dict:
    """Get details for a specific movie or TV show."""
    if media_type == "movie":
        details_url = f"{TMDB_BASE_URL}/movie/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US"
    else:
        details_url = f"{TMDB_BASE_URL}/tv/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(details_url)
    if response.status_code != 200:
        return {}
    return response.json()

def get_poster_urls(tmdb_id: str, media_type: str) -> dict:
    """Get all available poster images."""
    url = f"{TMDB_BASE_URL}/{media_type}/{tmdb_id}/images?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return {}
    return response.json()

def get_logo_url(tmdb_id: str, media_type: str) -> str:
    """Fetch the official logo image (if available) from TMDB."""
    url = f"{TMDB_BASE_URL}/{media_type}/{tmdb_id}/images?api_key={TMDB_API_KEY}&include_image_language=en,null"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    logos = data.get("logos") or []
    if logos:
        return f"{TMDB_IMAGE_BASE_URL}{logos[0]['file_path']}"
    return None