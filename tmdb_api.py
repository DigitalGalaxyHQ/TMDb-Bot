import requests
from config import TMDB_API_KEY, TMDB_BASE_URL, TMDB_IMAGE_BASE_URL

def search_tmdb(query: str) -> list:
    """Search TMDB for movies and TV shows."""
    search_url = f'{TMDB_BASE_URL}/search/multi?api_key={TMDB_API_KEY}&query={query}&language=en-US'
    response = requests.get(search_url)
    
    if response.status_code != 200:
        return []
    
    data = response.json()
    return data.get('results', [])

def get_media_details(tmdb_id: str, media_type: str) -> dict:
    """Get details for a specific movie or TV show."""
    if media_type == 'movie':
        details_url = f'{TMDB_BASE_URL}/movie/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US'
    else:
        details_url = f'{TMDB_BASE_URL}/tv/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US'
    
    response = requests.get(details_url)
    if response.status_code != 200:
        return {}
    
    return response.json()

def get_poster_urls(tmdb_id: str, media_type: str) -> dict:
    """Get all available poster URLs for a movie/TV show."""
    if media_type == 'movie':
        images_url = f'{TMDB_BASE_URL}/movie/{tmdb_id}/images?api_key={TMDB_API_KEY}'
    else:
        images_url = f'{TMDB_BASE_URL}/tv/{tmdb_id}/images?api_key={TMDB_API_KEY}'
    
    response = requests.get(images_url)
    if response.status_code != 200:
        return {
            'english': {'landscape': None, 'portrait': None},
            'hindi': {'landscape': None, 'portrait': None}
        }
    
    images_data = response.json()
    return {
        'english': {
            'landscape': find_landscape_image(images_data.get('backdrops', []), 'en'),
            'portrait': find_portrait_image(images_data.get('posters', []), 'en')
        },
        'hindi': {
            'landscape': find_landscape_image(images_data.get('backdrops', []), 'hi'),
            'portrait': find_portrait_image(images_data.get('posters', []), 'hi')
        }
    }

def find_landscape_image(images: list, language: str) -> str:
    """Find a landscape image (backdrop) for the specified language."""
    for image in images:
        if image.get('iso_639_1') == language and image.get('aspect_ratio', 0) >= 1.7:
            return f"{TMDB_IMAGE_BASE_URL}{image['file_path']}"
    return None

def find_portrait_image(images: list, language: str) -> str:
    """Find a portrait image (poster) for the specified language."""
    for image in images:
        if image.get('iso_639_1') == language and image.get('aspect_ratio', 1) < 1.0:
            return f"{TMDB_IMAGE_BASE_URL}{image['file_path']}"
    return None