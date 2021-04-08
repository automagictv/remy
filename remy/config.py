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

ALLOWED_TAGS = [
    # Diets https://spoonacular.com/food-api/docs#Diets
    "gluten free",
    "ketogenic",
    "vegetarian",
    "lacto-vegetarian",
    "ovo-vegetarian",
    "vegan",
    "pescetarian",
    "paleo",
    "primal",
    "whole30",
    # Intolerances https://spoonacular.com/food-api/docs#Intolerances
    "dairy",
    "egg",
    "gluten",
    "grain",
    "peanut",
    "seafood",
    "sesame",
    "shellfish",
    "soy",
    "sulfite",
    "tree nut",
    "wheat",
    # Cuisines https://spoonacular.com/food-api/docs#Cuisines
    "African",
    "American",
    "British",
    "Cajun",
    "Caribbean",
    "Chinese",
    "Eastern European",
    "European",
    "French",
    "German",
    "Greek",
    "Indian",
    "Irish",
    "Italian",
    "Japanese",
    "Jewish",
    "Korean",
    "Latin American",
    "Mediterranean",
    "Mexican",
    "Middle Eastern",
    "Nordic",
    "Southern",
    "Spanish",
    "Thai",
    "Vietnamese",
    # Meal types https://spoonacular.com/food-api/docs#Meal-Types
    "main course",
    "side dish",
    "dessert",
    "appetizer",
    "salad",
    "bread",
    "breakfast",
    "soup",
    "beverage",
    "sauce",
    "marinade",
    "fingerfood",
    "snack",
    "drink",
    "",
]
