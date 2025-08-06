import pytest
from unittest.mock import patch
from bot.tmdb_api import search_tmdb, get_media_details, get_poster_urls

@patch('bot.tmdb_api.requests.get')
def test_search_tmdb(mock_get):
    mock_response = type('MockResponse', (), {
        'status_code': 200,
        'json': lambda self: {
            'results': [
                {'media_type': 'movie', 'id': 123, 'title': 'Test Movie'},
                {'media_type': 'tv', 'id': 456, 'name': 'Test TV Show'}
            ]
        }
    })
    mock_get.return_value = mock_response()
    
    results = search_tmdb('test')
    assert len(results) == 2
    assert results[0]['title'] == 'Test Movie'
    assert results[1]['name'] == 'Test TV Show'

@patch('bot.tmdb_api.requests.get')
def test_get_media_details(mock_get):
    mock_response = type('MockResponse', (), {
        'status_code': 200,
        'json': lambda self: {'title': 'Test Movie', 'overview': 'Test overview'}
    })
    mock_get.return_value = mock_response()
    
    details = get_media_details('123', 'movie')
    assert details['title'] == 'Test Movie'
    assert details['overview'] == 'Test overview'

@patch('bot.tmdb_api.requests.get')
def test_get_poster_urls(mock_get):
    mock_response = type('MockResponse', (), {
        'status_code': 200,
        'json': lambda self: {
            'backdrops': [
                {'file_path': '/test_en.jpg', 'iso_639_1': 'en', 'aspect_ratio': 1.78},
                {'file_path': '/test_hi.jpg', 'iso_639_1': 'hi', 'aspect_ratio': 1.78}
            ],
            'posters': [
                {'file_path': '/poster_en.jpg', 'iso_639_1': 'en', 'aspect_ratio': 0.67},
                {'file_path': '/poster_hi.jpg', 'iso_639_1': 'hi', 'aspect_ratio': 0.67}
            ]
        }
    })
    mock_get.return_value = mock_response()
    
    urls = get_poster_urls('123', 'movie')
    assert 'english' in urls
    assert 'hindi' in urls
    assert 'landscape' in urls['english']
    assert 'portrait' in urls['english']
