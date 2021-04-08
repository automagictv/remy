from io import StringIO
from html.parser import HTMLParser
import logging
import re

from spoonacular import API
from telegram.utils.helpers import escape_markdown

from remy import config


class HTMLStripper(HTMLParser):
    """Created by Eloff: https://stackoverflow.com/a/925630"""

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, data):
        self.text.write(data)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    """Strips text of HTML tags to avoid telegram errors.

    Args:
        html: string, representing recipe data.
    Returns:
        Cleaned string sans html.
    """
    if not html:
        return
    stripper = HTMLStripper()
    stripper.feed(html)
    return stripper.get_data()


class QuotaError(Exception):
    """Custom error to handle quota issues."""
    pass


class SpoonacularFacade(object):

    def __init__(self, api_key=config.SPOONACULAR_KEY):
        """Constructs a SpoonacularFacade object.

        Args:
            api_key: str, the API key to authorize the connection.
        """
        self.client = API(api_key)
        logging.info("Spoonacular client created.")

    def check_status_and_raise(self, response):
        """Checks to see if we've hit our points quota for the day.
        
        The primary purpose of this method is to raise a custom status that we
        can handle so our bot doesn't crash.

        An error status would look something like this: {
            'status': 'failure',
            'code': 402,
            'message': 'Your daily points limit of 150 has been reached...'
        }
        
        Any other format (e.g. a list) indicates that we did not get a quota
        error.

        Args:
            response: A Spoonacular response object.
        Returns:
            None
        Raises:
            QuotaError if we have exceeded our quota.
        """
        content = response.json()
        if isinstance(content, list):
            return

        status = content.get("status")
        code = content.get("code")
        message = content.get("message")

        if status == "failure" and code == 402:
            raise QuotaError(message)

    def get_recipe_ids_for_ingredients(self, ingredients,
                                       limit=config.RECIPE_LIMIT):
        """Returns recipe ids from the Spoonacular API given ingredients.

        Enforces the RECIPE_LIMIT parameter in the config file. Or the one
        passed to the limit argument here.

        Args:
            ingredients: str, a comma separated list of ingredient strings.
            limit: int, max recipe ids to return.
        Returns:
            A list of Spoonacular recipe ids.
        """
        logging.info(
            f"Calling Spoonacular to search by ingredients: {ingredients}")
        response = self.client.search_recipes_by_ingredients(ingredients)
        self.check_status_and_raise(response)
        recipe_data = response.json()
        logging.info(f"Retrieved {len(recipe_data)} recipes."
                     f" Limit of {limit} will be enforced.")
        return [recipe["id"] for recipe in recipe_data[:limit]]

    def get_random_recipe(self, tags=None):
        """Returns a random recipe from the Spoonacular API.

        Args:
            tags: str, a comma separated list of tags. Valid tags can be any
                from the following Spoonacular sets:
                    - Meal Types: https://spoonacular.com/food-api/docs#Meal-Types
                    - Diets: https://spoonacular.com/food-api/docs#Diets
                    - Cuisines: https://spoonacular.com/food-api/docs#Cuisines
                    - Intolerances: https://spoonacular.com/food-api/docs#Intolerances

        Returns:
            A dictionary (json-like) containing the data for the random recipe.
        """
        logging.info(f"Calling Spoonacular to get a random recipe with tags"
                     f" {tags}")
        response = self.client.get_random_recipes(tags=tags)
        self.check_status_and_raise(response)
        return response.json()["recipes"][0]

    def get_random_alcoholic_beverage_recipe_id(self):
        """Returns a single random alcoholic beverage recipe id from the API.

        Returns:
            A single int Spoonacular recipe id.
        """
        logging.info(f"Calling Spoonacular to get a random cocktail.")
        response = self.client.search_recipes_complex(
            "",
            type="drink",
            minAlcohol=7,
            sort="random",
            number=1
        )
        self.check_status_and_raise(response)
        return response.json()["results"][0]["id"]

    def get_recipes_for_ids(self, ids):
        """Gets recipes from the API given a set of ids.

        Args:
            ids: list of one or more Spoonacular recipe ids.
        Returns:
            A list of dictionaries (json-like) containing the data for
            each recipe.
        """
        logging.info(f"Getting recipes for the following ids: {ids}")
        ids_param = ','.join([str(_id) for _id in ids])
        response = self.client.get_recipe_information_bulk(ids_param)
        self.check_status_and_raise(response)
        recipes = response.json()
        logging.info(f"Retrieved data for {len(recipes)} recipes.")
        return recipes

    @classmethod
    def format_recipe_title_link_as_markdown(cls, recipe_data):
        """Formats a json-like dictionary of recipe data as a markdown link.

        Expects that recipe data matches the Spoonacular JSON response
        structure as seen here:
            https://spoonacular.com/food-api/docs#Search-Recipes-by-Ingredients

        Args:
            recipe_data: dict of recipe data from the Spoonacular API.
        Returns:
            String representation of the recipe markdown link.
        """
        title = escape_markdown(strip_tags(recipe_data["title"]).strip(), 2)
        return f"**[{title}]({recipe_data['sourceUrl']})**"

    @classmethod
    def format_recipe_data_as_html(cls, recipe_data):
        """Formats a json-like dictionary of recipe data as HTML.

        Expects that recipe data matches the Spoonacular JSON response
        structure as seen here:
            https://spoonacular.com/food-api/docs#Search-Recipes-by-Ingredients

        Args:
            recipe_data: dict of recipe data from the Spoonacular API.
        Returns:
            String representation of the recipe formatted as an HTML object.
        """
        ingredients = "\n".join([
            strip_tags(ingredient["originalString"]) for ingredient
            in recipe_data["extendedIngredients"]
        ])

        raw_instructions = recipe_data['instructions']
        if not raw_instructions:
            instructions = "This recipe didn't have instructions! =O"
        else:
            # Clean up instructions
            instructions = re.sub(
                " +", " ",
                strip_tags(raw_instructions)).strip()

        formatted = (
            f"<b>{strip_tags(recipe_data['title'])}</b>\n"
            f"Cooktime: {recipe_data['readyInMinutes']} minutes\n\n"
            f"<u>Ingredients</u>\n"
            f"{ingredients}\n\n"
            f"<u>Instructions</u>\n"
            f"{instructions}"
        )

        return formatted
