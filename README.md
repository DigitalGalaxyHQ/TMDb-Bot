# 🌌 **DigitalGalaxyHQ™ – TMDb Movie & Series Poster Bot**

A next-gen Telegram bot by **DigitalGalaxyHQ** that lets you explore your favorite movies and TV shows directly from **The Movie Database (TMDb)**.  
It delivers **high-quality posters**, **cinematic backdrops**, and **official logos** — all in one stylish view.

---

## 👨‍💻 **Developed & Powered by**
**DigitalGalaxyHQ**  
Where entertainment meets innovation ⚡  

---

## ✨ **Key Features**

- 🔍 **Smart TMDb Search** – Instantly find any movie or TV show.  
- 🖼 **Visual Display Mode** – Returns **poster**, **landscape backdrop**, and **logo** for every title.  
- 🌐 **Multilingual Metadata** – Supports English, Hindi, Tamil, Telugu, and Bengali.  
- 🎛 **Interactive Buttons** – Navigate between posters, cast, and details.  
- ⚙️ **High-Resolution Images** – Automatically fetches the best available quality.  
- 🧠 **AI-Enhanced Search** *(Coming Soon)* – Suggests trending or related titles based on your queries.

---

## 🔧 **Configuration**

### 🎬 **Get Your TMDb API Key**
1. Visit [TMDb](https://www.themoviedb.org/).  
2. Go to your [Account Settings → API](https://www.themoviedb.org/settings/api).  
3. Request a **Developer API key** (v3 auth).  
4. Copy your TMDb API key for setup.

### 🤖 **Get Your Telegram Bot Token**
1. Chat with [@BotFather](https://t.me/BotFather).  
2. Send `/newbot` and follow the steps.  
3. Save the token you receive — it’s your bot’s unique access key.

### ⚙️ **Configuration File (`config.py`)**
Stores:
- API Keys (from `.env`)
- TMDb base URLs and image sizes
- Supported languages  

You can modify it to add new languages or tweak image resolutions.

---

## 🚀 **Setup**

### 🧩 **Local Setup**
1. Clone this repository:  
   ```bash
   git clone https://github.com/DigitalGalaxyHQ/TMDb-Bot.git
   cd TMDb-Bot

2. Install dependencies:

pip install -r requirements.txt


3. Create a .env file with your TMDb and Telegram tokens.


4. Run your bot:

python bot.py



☁️ Deploy to Heroku

Click below to deploy directly:



For advanced deployment steps, see DEPLOYMENT.md.


---

💬 Commands

Command	Description

/start	Displays a welcome message and quick guide
/tmdb <title>	Search any movie or show and get Poster + Backdrop + Logo
/trndb <title>	Alternative TMDb search command



---

🪄 Coming Soon

🎥 Instant trailer preview buttons

🧩 Genre-based auto-recommendations

🔗 Telegram-to-TMDb profile linking



---

📜 License

Maintained under @DigitalGalaxyHQ