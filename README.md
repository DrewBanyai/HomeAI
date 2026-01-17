# HomeAI: Your Offline Personal Assistant

![](Cover.png)

HomeAI is a Python-based, privacy-focused offline AI assistant designed to handle daily tasks and provide information without relying on cloud-based smart speakers. It features a custom terminal interface, voice recognition, and text-to-speech capabilities.

---

## 🚀 Getting Started

### Prerequisites
Before running HomeAI, ensure you have Python installed. You will also need a working microphone and speakers.

### Initial Installation
1. Clone the repository to your local machine.
2. Install the required dependencies using pip:
   ```bash
   pip install -r Requirements.txt
   ```

### Configuration (`_env.py`)
To enable full functionality, you must configure the `_env.py` file with your preferences and API keys:

- **AI Name**: Change `AI_NAME` (default is "Frank") to your preferred wake word.
- **News**: Get a free API key from [newsapi.org](https://newsapi.org/) and set `NEWS_API_KEY`.
- **Crypto**: Get a free API key from [coinapi.io](https://www.coinapi.io/) and set `COIN_API_KEY`. Define your pairs in `CRYPTO_ASSET_PAIRS`.
- **Email**: To use the email feature, provide your Gmail address and an [App Password](https://myaccount.google.com/apppasswords) in `GMAIL_EMAIL` and `GMAIL_APP_PASSWORD`.
- **Weather**: Update the `WEATHER_API` URLs with your local latitude and longitude coordinates.

---

## 🗣️ How to Interact

HomeAI listens for its name (the wake word) followed by a command.

**Example:**
> *"Frank, what time is it?"*

### The UI
When you run `HomeAI.py`, a terminal-based UI will launch, showing:
- **Status**: Current state (Listening, Thinking, Speaking).
- **History**: A log of your commands and the AI's responses.
- **Weather**: A visual ASCII forecast (if weather commands are used).

---

## 📋 Available Commands

| Command Category | Primary Command | Description |
| :--- | :--- | :--- |
| **System** | "Can you hear me" | Verifies the AI is active and listening. |
| **Time** | "What time is it" | Tells the current local time. |
| **News** | "Give me the headlines" | Reads the top headlines from the Associated Press. |
| **Crypto** | "Get crypto prices" | Provides exchange rates for your configured asset pairs. |
| **Email** | "Send a test email" | Sends a test message to your configured Gmail account. |
| **Alarms** | "Set an alarm for XXX" | Sets a reminder (e.g., "Set an alarm for 7:15 PM"). |
| **Weather** | "Weather forecast" | Displays and reads a 7-day weather forecast. |
| **Weather** | "What's the weather today" | Gives a detailed report for the current day. |
| **System** | "Shut down" | Safely closes the application. |

---

## 🔄 Command Alternates & "Frank"
Speech recognition isn't always perfect. HomeAI includes a robust system in `CommandAlternates.py` to handle variations and common misspellings.

- **Dynamic Wake Word**: If you change the name in `_env.py`, make sure to update `AINameAlternates` in `CommandAlternates.py` to help the AI recognize its new name even if it's slightly misheard (e.g., "Frank" vs "Rank").
- **Flexible Phrases**: Commands like "Get the news" or "What's the weather" automatically map to their primary functions, making the interaction feel more natural.

---

## 🛠️ Project Structure
- `HomeAI.py`: The main entry point.
- `TerminalUI.py`: Manages the visual interface.
- `Commands.py`: Logic for executing specific tasks.
- `Helper.py`: Core utility functions.
- `WeatherForecast.py`: Integrates with weather APIs.
- `SpeechDetector.py` & `TextToSpeech.py`: Handle audio I/O.