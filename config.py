from os import environ

API_ID = int(environ.get("API_ID", ""))
API_HASH = environ.get("API_HASH", "")
BOT_TOKEN = environ.get("BOT_TOKEN", "")
ADMIN = int(environ.get("ADMIN", ""))          
CAPTION = environ.get("CAPTION", "")
SOURCE_CHANNEL = -1001234567890  # Replace with your source channel ID
TARGET_CHANNEL = -1009876543210  # Replace with your target channel ID

# for thumbnail ( back end is MrMKN brain 😉)
DOWNLOAD_LOCATION = "./DOWNLOADS"

