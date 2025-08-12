# 🎬 TMDB Telegram Bot

A Telegram bot that searches TMDB and displays movie/TV show posters in landscape and portrait formats.

[![DigitalGalaxyHQ Channel](https://img.shields.io/badge/Join-Telegram-Channel-blue)](https://t.me/DigitalGalaxyHQ)

## ✨ Features

- Search for movies and TV shows using `/tmdb` command
- Display posters in both landscape and portrait formats
- Support for multiple languages (English and Hindi)
- Clean interface with emoji indicators

## 🛠️ Setup

1. Clone this repository
2. Create a `.env` file based on `.env.example`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the bot: `python bot.py`

```bash
git clone https://github.com/yourusername/tmdb-telegram-bot.git
cd tmdb-telegram-bot
cp .env.example .env
pip install -r requirements.txt
python bot.py
```

## ⌨️ Commands

- `/start` - Show welcome message
- `/help` - Show help information
- `/tmdb <query>` - Search for movies/TV shows

## ⚙️ Configuration

Edit `config.py` or `.env` file:

```ini
TELEGRAM_TOKEN=your_bot_token
TMDB_API_KEY=your_tmdb_api_key
```

## 🚀 Deployment

### Render.com (Recommended)
- Set start command: `python bot.py`
- Web Service type
- Port: 8080

### Other Platforms:
- **Docker**: `docker build -t tmdb-bot . && docker run tmdb-bot`
- **Systemd**: Create a service file with `ExecStart=python /path/to/bot.py`
- **Heroku/AWS**: Set start command to `python bot.py`

## 💙 Credits

**Developed by:** [DigitalGalaxyHQ](https://GitHub.com/DigitalGalaxyHQ)  
**Official Telegram Channel:** [DigitalGalaxyHQ](https://t.me/DigitalGalaxyHQ)  

[![DigitalGalaxyHQ](https://img.shields.io/badge/Join-Telegram-Channel-blue)](https://t.me/DigitalGalaxyHQ)
```
 