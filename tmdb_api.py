import requests
from config import TMDB_API_KEY, TMDB_BASE_URL, TMDB_IMAGE_BASE_URL

def search_tmdb(query: str) -> list:
    """Search TMDB for movies and TV shows."""
    search_url = f'{TMDB_BASE_URL}/search/multi?api_key={TMDB_API_KEY}&query={query}&language=en-US'
    response = requests.get(search_url)
    return response.json().get('results', []) if response.status_code == 200 else []

def get_media_details(tmdb_id: str, media_type: str) -> dict:
    """Get details for a specific movie or TV show."""
    endpoint = 'movie' if media_type == 'movie' else 'tv'
    details_url = f'{TMDB_BASE_URL}/{endpoint}/{tmdb_id}?api_key={TMDB_API_KEY}'
    response = requests.get(details_url)
    return response.json() if response.status_code == 200 else {}

def get_poster_urls(tmdb_id: str, media_type: str) -> dict:
    """Get all available image URLs without size modifications."""
    endpoint = 'movie' if media_type == 'movie' else 'tv'
    images_url = f'{TMDB_BASE_URL}/{endpoint}/{tmdb_id}/images?api_key={TMDB_API_KEY}'
    response = requests.get(images_url)
    
    if response.status_code != 200:
        return {'english': {'landscape': [], 'portrait': []}, 'hindi': {'landscape': [], 'portrait': []}}

    images_data = response.json()
    result = {
        'english': {'landscape': [], 'portrait': []},
        'hindi': {'landscape': [], 'portrait': []}
    }

    # Process images
    for backdrop in images_data.get('backdrops', []):
        if backdrop.get('aspect_ratio', 0) >= 1.7:  # Landscape
            lang = backdrop.get('iso_639_1')
            url = f"{TMDB_IMAGE_BASE_URL}/{backdrop['file_path']}"
            if lang == 'en' or lang is None:
                result['english']['landscape'].append(url)
            elif lang == 'hi':
                result['hindi']['landscape'].append(url)

    for poster in images_data.get('posters', []):
        if poster.get('aspect_ratio', 1) < 1.0:  # Portrait
            lang = poster.get('iso_639_1')
            url = f"{TMDB_IMAGE_BASE_URL}/{poster['file_path']}"
            if lang == 'en' or lang is None:
                result['english']['portrait'].append(url)
            elif lang == 'hi':
                result['hindi']['portrait'].append(url)

    # Remove duplicates and limit counts
    for lang in result:
        for img_type in result[lang]:
            result[lang][img_type] = list(dict.fromkeys(result[lang][img_type]))[:10]
    
    return result

def get_logos(tmdb_id: str, media_type: str) -> list:
    """Get logo URLs without size modifications."""
    endpoint = 'movie' if media_type == 'movie' else 'tv'
    images_url = f'{TMDB_BASE_URL}/{endpoint}/{tmdb_id}/images?api_key={TMDB_API_KEY}'
    response = requests.get(images_url)
    
    if response.status_code != 200:
        return []
    
    logos = []
    for logo in response.json().get('logos', []):
        if logo.get('iso_639_1') in ('en', None):  # English or language-neutral
            logos.append(f"{TMDB_IMAGE_BASE_URL}/{logo['file_path']}")
    
    return list(dict.fromkeys(logos))[:5]  # Remove duplicates, max 5 logos