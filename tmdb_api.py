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
    """Get all available poster URLs with proper image sizes."""
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
    
    result = {
        'english': {
            'landscape': [],
            'portrait': []
        },
        'hindi': {
            'landscape': [],
            'portrait': []
        }
    }
    
    # Process backdrops (landscape)
    for backdrop in images_data.get('backdrops', []):
        if backdrop.get('iso_639_1') in ('en', None) and backdrop.get('aspect_ratio', 0) >= 1.7:
            result['english']['landscape'].append(f"{TMDB_IMAGE_BASE_URL}/w1280{backdrop['file_path']}")
        elif backdrop.get('iso_639_1') == 'hi' and backdrop.get('aspect_ratio', 0) >= 1.7:
            result['hindi']['landscape'].append(f"{TMDB_IMAGE_BASE_URL}/w1280{backdrop['file_path']}")
    
    # Process posters (portrait)
    for poster in images_data.get('posters', []):
        if poster.get('iso_639_1') in ('en', None) and poster.get('aspect_ratio', 1) < 1.0:
            result['english']['portrait'].append(f"{TMDB_IMAGE_BASE_URL}/w780{poster['file_path']}")
        elif poster.get('iso_639_1') == 'hi' and poster.get('aspect_ratio', 1) < 1.0:
            result['hindi']['portrait'].append(f"{TMDB_IMAGE_BASE_URL}/w780{poster['file_path']}")
    
    # Remove duplicates
    for lang in result:
        for img_type in result[lang]:
            seen = set()
            result[lang][img_type] = [x for x in result[lang][img_type] if not (x in seen or seen.add(x))][:10]
    
    return result

def get_logos(tmdb_id: str, media_type: str) -> list:
    """Get logo images if available."""
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
            logos.append(f"{TMDB_IMAGE_BASE_URL}/w300{logo['file_path']}")
    
    return list(dict.fromkeys(logos))[:5]  # Remove duplicates, max 5 logos