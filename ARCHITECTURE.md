# Requirements

 - Accept a list of ingredients
 - Return a recipe(s) using as many of those ingredients as possible
 - Accassible on any device
 - Always available to accept/return recipes
 - Utilize a bot/interactive interface
 - Return random recipes
 - Return random cocktail recipes
 - Give us tacos

# Object Model

 - Spoonacular API Facade
   - Get recipes from ingredients
   - Get random recipe
   - Get random drinks
   - Parse / format recipe results
 - Telegram Utility
   - Updater
   - Dispatcher
   - Handlers
   - Helper functions
 - Config
   - Keys / tokens
   - Constants
 - Runner
   - Logging
   - Main / listener
 - Tests

# Expansion Ideas

 - Use telegram’s [Job Queue](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-JobQueue) to send yourself weekly [meal plans](https://spoonacular.com/food-api/docs#Generate-Meal-Plan) 
 - Can extend the above to also send yourself a [shopping list](https://spoonacular.com/food-api/docs#Compute-Shopping-List) for the weekly meal plan
 - Add “get something similar” [functionality](https://spoonacular.com/food-api/docs#Get-Similar-Recipes)
 - Add functionality to adjust meal plan settings in telegram
 - Add a SQL database to remember recipes you’ve tried and liked
 - Add sharing functionality so you can share recipes in telegram
