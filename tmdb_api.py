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
    """Get all available poster URLs with multiple images for each type."""
    if media_type == 'movie':
        images_url = f'{TMDB_BASE_URL}/movie/{tmdb_id}/images?api_key={TMDB_API_KEY}'
    else:
        images_url = f'{TMDB_BASE_URL}/tv/{tmdb_id}/images?api_key={TMDB_API_KEY}'
    
    response = requests.get(images_url)
    if response.status_code != 200:
        return {
            'english': {'landscape': [], 'portrait': []},
            'hindi': {'landscape': [], 'portrait': []}
        }
    
    images_data = response.json()
    
    return {
        'english': {
            'landscape': get_all_images(images_data.get('backdrops', []), 'en', 'landscape'),
            'portrait': get_all_images(images_data.get('posters', []), 'en', 'portrait')
        },
        'hindi': {
            'landscape': get_all_images(images_data.get('backdrops', []), 'hi', 'landscape'),
            'portrait': get_all_images(images_data.get('posters', []), 'hi', 'portrait')
        }
    }

def get_logos(tmdb_id: str, media_type: str) -> list:
    """Get all logo images for a movie/TV show."""
    if media_type == 'movie':
        images_url = f'{TMDB_BASE_URL}/movie/{tmdb_id}/images?api_key={TMDB_API_KEY}'
    else:
        images_url = f'{TMDB_BASE_URL}/tv/{tmdb_id}/images?api_key={TMDB_API_KEY}'
    
    response = requests.get(images_url)
    if response.status_code != 200:
        return []
    
    logos = []
    for logo in response.json().get('logos', []):
        if logo.get('iso_639_1') in ('en', None):  # English or language-neutral
            logos.append(f"{TMDB_IMAGE_BASE_URL}/original{logo['file_path']}")
    
    return logos[:5]  # Return max 5 logos

def get_all_images(images: list, language: str, image_type: str) -> list:
    """Get all images of specified type and language."""
    result = []
    for image in images:
        # Include language-specific or language-neutral images
        if image.get('iso_639_1') in (language, None):
            if image_type == 'landscape' and image.get('aspect_ratio', 0) >= 1.7:
                result.append(f"{TMDB_IMAGE_BASE_URL}/original{image['file_path']}")
            elif image_type == 'portrait' and image.get('aspect_ratio', 1) < 1.0:
                result.append(f"{TMDB_IMAGE_BASE_URL}/original{image['file_path']}")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_images = []
    for url in result:
        if url not in seen:
            seen.add(url)
            unique_images.append(url)
    
    return unique_images[:10]  # Return max 10 images