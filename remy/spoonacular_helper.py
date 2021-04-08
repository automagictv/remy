import logging

from spoonacular import API

from remy import config


class SpoonacularFacade(object):

    def __init__(self, api_key=config.SPOONACULAR_KEY):
        """Constructs a SpoonacularFacade object.
        Args:
            api_key: str, the API key to authorize the connection.
        """
        self.client = API(api_key)

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
        raise NotImplementedError

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
        raise NotImplementedError

    def get_random_alcoholic_beverage_recipe_id(self):
        """Returns a single random alcoholic beverage recipe id from the API.
        Returns:
            A single int Spoonacular recipe id.
        """
        raise NotImplementedError

    def get_recipes_for_ids(self, ids):
        """Gets recipes from the API given a set of ids.
        Args:
            ids: list of one or more Spoonacular recipe ids.
        Returns:
            A list of dictionaries (json-like) containing the data for
            each recipe.
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError
