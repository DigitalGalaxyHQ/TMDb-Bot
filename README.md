# TMDB Telegram Bot

A Telegram bot that searches TMDB and displays movie/TV show posters in landscape and portrait formats.

## Features

- Search for movies and TV shows using `/tmdb` command
- Display posters in both landscape and portrait formats
- Support for multiple languages (English and Hindi)
- Clean interface with emoji indicators

## Setup

1. Clone this repository
2. Create a `.env` file based on `.env.example`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the bot: `python -m bot.main`

## Commands

- `/start` - Show welcome message
- `/help` - Show help information
- `/tmdb <query>` - Search for movies/TV shows

## Configuration

Edit `config.py` or `.env` file to change settings:

- `TELEGRAM_TOKEN` - Your Telegram bot token
- `TMDB_API_KEY` - Your TMDB API key

## Deployment

The bot can be deployed on any server with Python 3.7+. For production, consider using:

- Docker
- Systemd service
- Cloud platforms like Heroku or AWS
