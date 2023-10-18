![](Cover.png)

# HomeAI
A python-based offline AI assistant program, built to replace Alexa for daily tasks

## Issuing Queries
All queries are initiated with a query string and should begin with referring to the AI by name. By default, it's name is "Frank", so a query like "Can you hear me" would be issued by saying "Frank. Can you hear me?"

### Known Query Strings
* **"Can you hear me"** - Will answer with an affirmative if the program is online and listening properly
* **"What time is it"** - Will answer with the current time. By default, this is in Eastern Standard Time, but you can change this setting in code
* **"Give me the headlines"** - Will answer with the top headlines from the Associated Press news feed (if Open News API key is provided in _env.py)
* **"Get crypto prices"** - Will give the current exchange rates between asset pairs (if a list of CRYPTO_ASSET_PAIRS and a COIN_API_KEY has been provided in _env.py)
* **"Send a test email"** - Will send an email from your GMAIL_EMAIL to your GMAIL_EMAIL with a test subject and message. You may customize this as you wish.
* **"Shut down"** - Will shut down the program

### Command Alternates
A number of commands have common mistranslations, so this project includes a number of command alternates in CommandAlternates.py which map back to the actual command. You may add more as needed. This file also includes AI name alternates, so if you change the AI name, you may want to add some alternate values for that as well.


### Initial Setup
If you'd like the full functionality of the bot, you'll need to sign up for a few free services and put some information into the _env.py file.
- For the news headlines, you'll need to sign up for a free API key at https://newsapi.org/
- For the ability to send an email, you'll need a Gmail account you can access and in the settings for it, you'll need to generate an API Password and supply both in _env.py
- For cryptocurrency prices, you'll need to sign up for a free API key at https://www.coinapi.io/
    - Note: This is not the same as signing up for a full account and then selecting the free tier. Just go to the main page and select free without an account to generate a key.
- You'll want to assign any crypto pairs you want to check the price of. For starters, I've put in BTC->USD but you can put in whatever you'd like. I've included a few commented out to try.
- If you want to refer to your HomeAI instance by a name other than "Frank", you can set that in _env.py, but you should also alter the AINameAlternates list in CommandAlternates.py