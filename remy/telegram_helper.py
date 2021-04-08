import logging

import telegram
from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    Updater
)

from remy import config
from remy import spoonacular_helper as sp


spoon = sp.SpoonacularFacade()

logging.info("Creating updaters and dispatchers...")

UPDATER = Updater(token=config.TELEGRAM_TOKEN)
DISPATCHER = UPDATER.dispatcher

logging.info("Updater and Dispatcher created.")


def format_message_and_get_parse_mode(recipe):
    """Formats a message and returns the proper parse mode.
    
    Args:
        recipe: json-like dict of recipe data.
    Returns:
        Tuple of formatted message and parse mode
    """
    logging.info(
        f"Formatting the recipe: {recipe['title']} | id: {recipe['id']}")
    parse_mode = telegram.ParseMode.HTML
    message = sp.SpoonacularFacade.format_recipe_data_as_html(recipe)

    if len(message) > config.TELEGRAM_MESSAGE_CHAR_LIMIT:
        logging.info("Recipe too long! Formatting a link instead.")
        link = sp.SpoonacularFacade.format_recipe_title_link_as_markdown(recipe)
        message = (
            f"This recipe was too long to send here! Here's the "
            f"link instead: {link}"
        )
        parse_mode = telegram.ParseMode.MARKDOWN_V2

    return message, parse_mode


def start(update, context):
    """Start bot command function."""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "We're up! You can use the following commands to talk to me:\n"
            "/recipe [ingredients,to,search]\n"
            "/random\n"
            "/happyhour\n"
            "/taco\nMake something delicious!"
        )
    )


def recipes_for_ingredients(update, context):
    """Returns html formatted recipes given the input string."""
    ingredients = ''.join(context.args).lower()
    recipe_ids = spoon.get_recipe_ids_for_ingredients(ingredients)
    recipes = spoon.get_recipes_for_ids(recipe_ids)

    for recipe in recipes:
        message, parse_mode = format_message_and_get_parse_mode(recipe) 
        logging.info("Sending...")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode=parse_mode
        )
        logging.info("Recipe sent!")


def random_recipe(update, context):
    """Returns html formatted random recipe."""
    tags = ','.join(context.args).lower()
    recipe = spoon.get_random_recipe(tags=tags)
    message, parse_mode = format_message_and_get_parse_mode(recipe)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        parse_mode=parse_mode
    )


def random_alcoholic_beverage(update, context):
    """Returns html formatted random alcoholic beverage recipe."""
    recipe_id = spoon.get_random_alcoholic_beverage_recipe_id()
    recipe = spoon.get_recipes_for_ids([recipe_id])
    message, parse_mode = format_message_and_get_parse_mode(recipe[0])

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        parse_mode=telegram.ParseMode.HTML
    )


def _help(update, context):
    """Returns list of commands."""
    message = (
        "Commands:\n"
        "\t/recipe [ingredients,to,search] -> separted by commas, no brackets\n"
        "\t/random [optional:tags] -> returns a random recipe\n"
        "\t/happyhour -> returns a random cocktail recipe\n"
        "\t/taco -> returns a random taco recipe"
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message
    )


def get_a_taco(update, context):
    """Returns a random taco!"""
    taco = "[Taco\!](https://taco-randomizer.herokuapp.com)"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=taco,
        parse_mode=telegram.ParseMode.MARKDOWN_V2
    )


def unknown(update, context):
    """Handles unknown commands."""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm sorry, I don't understand. Please use /help to see commands."
    )


def error_handler(update, object, context):
    """Handles errors we get while executing commands."""
    logging.error(
        msg="Something went wrong when trying to handle an update.",
        exc_info=context.error)

    message = "Something went wrong with that last one! Try again or use /help"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message
    )


START_HANDLER = CommandHandler('start', start)
RECIPE_INGREDIENTS_HANDLER = CommandHandler('recipe', recipes_for_ingredients)
RANDOM_RECIPE_HANDLER = CommandHandler('random', random_recipe)
HAPPY_HOUR_HANDLER = CommandHandler('happyhour', random_alcoholic_beverage)
TACO_HANDLER = CommandHandler('taco', get_a_taco)
UNKNOWN_HANDLER = MessageHandler(Filters.command, unknown)
HELP_HANDLER = CommandHandler('help', _help)

handlers = [
    START_HANDLER,
    HELP_HANDLER,
    RECIPE_INGREDIENTS_HANDLER,
    RANDOM_RECIPE_HANDLER,
    HAPPY_HOUR_HANDLER,
    TACO_HANDLER,
    # Unknown handler must be last
    UNKNOWN_HANDLER
]

for handler in handlers:
    logging.info(f"Adding the handler: {handler}")
    DISPATCHER.add_handler(handler)

logging.info(f"Adding our error handler.")
DISPATCHER.add_error_handler(error_handler)
