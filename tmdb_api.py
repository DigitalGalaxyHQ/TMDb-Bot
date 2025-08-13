import requests
from config import TMDB_API_KEY, TMDB_BASE_URL, TMDB_IMAGE_BASE_URL

def search_tmdb(query: str) -> list:
    """Search TMDB for movies and TV shows."""
    search_url = f'{TMDB_BASE_URL}/search/multi?api_key={TMDB_API_KEY}&query={query}'
    response = requests.get(search_url)
    return response.json().get('results', []) if response.status_code == 200 else []

def get_media_details(tmdb_id: str, media_type: str) -> dict:
    """Get details including official title."""
    endpoint = 'movie' if media_type == 'movie' else 'tv'
    details_url = f'{TMDB_BASE_URL}/{endpoint}/{tmdb_id}?api_key={TMDB_API_KEY}'
    response = requests.get(details_url)
    return response.json() if response.status_code == 200 else {}

def get_poster_urls(tmdb_id: str, media_type: str, title: str) -> dict:
    """Get image URLs with official posters first and formatted in bold."""
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

    # Process backdrops (landscape)
    official_landscape = []
    other_landscape = []
    
    for backdrop in images_data.get('backdrops', []):
        if backdrop.get('aspect_ratio', 0) >= 1.7:
            url = f"**{TMDB_IMAGE_BASE_URL}/{backdrop['file_path']}**"
            if backdrop.get('vote_average', 0) > 5:  # Prioritize higher-rated official images
                official_landscape.append(url)
            else:
                other_landscape.append(url)
    
    # Process posters (portrait)
    official_portrait = []
    other_portrait = []
    
    for poster in images_data.get('posters', []):
        if poster.get('aspect_ratio', 1) < 1.0:
            url = f"**{TMDB_IMAGE_BASE_URL}/{poster['file_path']}**"
            if poster.get('vote_average', 0) > 5:  # Prioritize higher-rated official images
                official_portrait.append(url)
            else:
                other_portrait.append(url)
    
    # Combine official and other images
    result['english']['landscape'] = official_landscape[:3] + other_landscape[:7]  # 3 official + 7 others
    result['english']['portrait'] = official_portrait[:3] + other_portrait[:7]
    
    return result

def get_logos(tmdb_id: str, media_type: str) -> list:
    """Get logo URLs in bold."""
    endpoint = 'movie' if media_type == 'movie' else 'tv'
    images_url = f'{TMDB_BASE_URL}/{endpoint}/{tmdb_id}/images?api_key={TMDB_API_KEY}'
    response = requests.get(images_url)
    
    if response.status_code != 200:
        return []
    
    logos = []
    for logo in response.json().get('logos', []):
        logos.append(f"**{TMDB_IMAGE_BASE_URL}/{logo['file_path']}**")
    
    return logos[:5]