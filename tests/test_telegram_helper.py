import telegram

from remy import config
from remy import telegram_helper
from remy import spoonacular_helper as sp


FAKE_RECIPE = {
    "id": 1,
    "title": "FAKE",
    "extendedIngredients": [
        {"originalString": "ing1"},
        {"originalString": "ing2"},
    ],
    "readyInMinutes": 10,
    "instructions": "Do some stuff.",
    "sourceUrl": "www.fake.com",
}


def test_format_message_and_get_parse_mode_returns_html_tuple():
    """Tests that we return proper tuple."""
    expected_msg = sp.SpoonacularFacade.format_recipe_data_as_html(
        FAKE_RECIPE
    )
    output = telegram_helper.format_message_and_get_parse_mode(FAKE_RECIPE)
    
    assert output[0] == expected_msg
    assert output[1] == telegram.ParseMode.HTML


def test_format_message_and_get_parse_mode_returns_markdown_tuple():
    """Tests that we return proper tuple."""
    md_msg = sp.SpoonacularFacade.format_recipe_title_link_as_markdown(
        FAKE_RECIPE
    )

    expected_msg = (
        f"This recipe was too long to send here\! Here's the "
        f"link instead: {md_msg}"
    )

    r_input = FAKE_RECIPE.copy()
    r_input["instructions"] = "a" * (config.TELEGRAM_MESSAGE_CHAR_LIMIT + 1)
    output = telegram_helper.format_message_and_get_parse_mode(r_input)

    assert output[0] == expected_msg
    assert output[1] == telegram.ParseMode.MARKDOWN_V2
