from typing import Optional, Dict, Any

def format_media_title(result: Dict[str, Any]) -> str:
    """Format media title with emoji and year."""
    media_type = '🎬' if result['media_type'] == 'movie' else '📺'
    title = result.get('title') or result.get('name')
    year = result.get('release_date', result.get('first_air_date', '')).split('-')[0]
    
    formatted = f"{media_type} {title}"
    if year:
        formatted += f" ({year})"
    
    return formatted

def validate_tmdb_response(response) -> bool:
    """Validate TMDB API response."""
    return response.status_code == 200 and response.json().get('results') is not None
