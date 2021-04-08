import logging

import telegram

from remy import telegram_helper


def main():
    """Runs our bot."""
    updater = telegram_helper.UPDATER

    logging.info("Starting the bot!")

    try:
        updater.start_polling()
        updater.idle()
    except telegram.error.TelegramError as e:
        logging.error(f"Something went wrong! {e}")
        raise e

    logging.info("Bot shutting down. See ya next time!")

if __name__ == "__main__":
    main()
