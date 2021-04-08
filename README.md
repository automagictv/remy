# remy
A [Telegram](https://telegram.org/) bot that will send you recipes for the ingredients in your fridge. This was built for a video tutorial [here]().

<img src="https://static.wikia.nocookie.net/pixar/images/5/56/Ratatouille-remy2.jpg/revision/latest/scale-to-width-down/619?cb=20110512131040" width="180" height="200" />

Image from [Ratatouille film](https://en.wikipedia.org/wiki/Ratatouille_(film)).

The bot has a few commands:

 - `/recipe [ingredients]` Will retrieve recipes that contain the ingredients supplied.
 - `/happyhour` Will return a random cocktail recipe.
 - `/random [optional:tags]` Will retrieve a random recipe. Available tags can be found on the Spoonacular site ([diets](https://spoonacular.com/food-api/docs#Diets), [intolerances](https://spoonacular.com/food-api/docs#Intolerances), [cuisines](https://spoonacular.com/food-api/docs#Cuisines), [meal types](https://spoonacular.com/food-api/docs#Meal-Types)).
 - `/taco` Will return a random taco recipe.
 - `/help` Will show available commands.
 - `/start` Will start the bot.

Examples in Telegram:

 - `/recipe ribeye, eggs, shallots, carrots`
 - `/happyhour`
 - `/random`
 - `/random breakfast`

## Setup

Clone the repo and install requirements. This uses [pipenv](https://pipenv.pypa.io/en/latest/) to manage the environment so make sure that's installed:

```
git clone https://github.com/automagictv/remy.git
cd remy
pipenv install --ignore-pipfile
```

Get your [Spoonacular](https://spoonacular.com/food-api) and [Telegram](https://telegram.org/) API keys and save them as environment variables.

## Running the Bot Server

The bot server can be started with the following command:

```
cd /path/to/remy
export SPOONACULAR_KEY="YOURKEY"
export TELEGRAM_TOKEN="YOURTOKEN"
export PYTHONPATH=$PYTHONPATH:$(pwd)
pipenv run python remy/runner.py
```

Then message your bot to start cooking!

## Testing

The tests can be run with [pytest](https://docs.pytest.org/en/stable/) via:

```
pipenv run python -m pytest
```

Or to test an individual module, run:

```
pipenv run python -m pytest tests/[test_module].py
```

Enjoy!
