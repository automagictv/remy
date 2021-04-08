import os
import logging

LOGFILE = os.environ.get("LOGFILE", "/tmp/remy.log")

logging.basicConfig(
    filename=LOGFILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

SPOONACULAR_KEY = os.environ.get("SPOONACULAR_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

RECIPE_LIMIT = 3

# Current message character limit is 4096
# https://core.telegram.org/method/messages.sendMessage 
# https://limits.tginfo.me/en
TELEGRAM_MESSAGE_CHAR_LIMIT = 4096
