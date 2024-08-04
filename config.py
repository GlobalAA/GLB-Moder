from os import getenv

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
OWNER_ID = int(getenv("OWNER_ID"))
CHAT_ID = int(getenv("CHAT_ID"))