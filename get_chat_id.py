import requests

# Your bot token
bot_token = "8373892671:AAEIEUBRzW8s2B0dagfmUENaprmgWajcNvY"

# Get updates from bot
url = f"https://api.telegram.org/bot{bot_token}/getUpdates"

try:
    response = requests.get(url)
    data = response.json()
    print(data)  # This shows all messages received by the bot
except Exception as e:
    print(f"Error: {e}")
