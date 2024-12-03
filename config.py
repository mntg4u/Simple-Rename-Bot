import os

# Mandatory environment variables
try:
    API_ID = int(os.environ["API_ID"])
    API_HASH = os.environ["API_HASH"]
    BOT_TOKEN = os.environ["BOT_TOKEN"]
except KeyError as e:
    raise KeyError(f"Missing mandatory environment variable: {e}")

# Optional environment variables
ADMIN = list(map(int, os.environ.get("ADMIN", "").split()))  # Allow multiple admins (comma-separated IDs)
CAPTION = os.environ.get("CAPTION", "Your file is ready!")  # Default caption if not provided
DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS")  # Default download location
TARGET_CHANNEL = int(os.environ.get("TARGET_CHANNEL", "0"))  # Default to 0 if not provided (invalid channel ID)

# Debugging logs
print(f"Configuration Loaded:\nAPI_ID: {API_ID}\nAPI_HASH: {API_HASH}\nBOT_TOKEN: {BOT_TOKEN}\nADMIN: {ADMIN}\nCAPTION: '{CAPTION}'\nDOWNLOAD_LOCATION: {DOWNLOAD_LOCATION}\nTARGET_CHANNEL: {TARGET_CHANNEL}")

