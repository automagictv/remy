"""Module to hold custom remy error objects."""


class QuotaError(Exception):
    """Error to handle quota issues."""
    pass


class MissingIngredientError(Exception):
    """Error when a /recipe call is made without ingredients."""
    pass


class RecipesNotFoundError(Exception):
    """Error if no recipes are found in Spoonacular."""
    pass


class InvalidRandomTagError(Exception):
    """Error if an invalid tag is passed to the /random command."""
    pass
