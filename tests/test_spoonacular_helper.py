from unittest import mock

from remy import spoonacular_helper


class FakeResponse:

    def __init__(self, jsondict):
        self.jsondict = jsondict

    def json(self):
        return self.jsondict


def test_strip_tags_strips():
    """Confirm that we actually strip HTML tags."""
    html = "<p>naked</p>"
    stripped = spoonacular_helper.strip_tags(html)
    assert stripped == "naked"


class TestSpoonacularFacade:
    """General note: the spoonacular.API constructor does not call the API.
    So it doesn't need to be mocked for all test api calls. We only have to 
    mock the methods that actually call the API.
    """

    @mock.patch.object(spoonacular_helper, "API", autospec=True)
    def test_spoonacular_constructor_creates_client(self, mock_api):
        """We call the api when we construct our SpoonacularFacade object."""
        fkey = "TEST"
        _ = spoonacular_helper.SpoonacularFacade(fkey)
        spoonacular_helper.API.assert_called_once_with(fkey)

    @mock.patch.object(spoonacular_helper, "API", autospec=True)
    def test_get_recipe_ids_for_ingredients_calls_proper_api(self, mock_api):
        """Tests that we call the search_recipes_by_ingredients api."""
        helper = spoonacular_helper.SpoonacularFacade("FAKEKEY")
        ingredients = "fake,list"
        _ = helper.get_recipe_ids_for_ingredients(ingredients)

        helper.client.search_recipes_by_ingredients.assert_called_once_with(
            ingredients
        )

    def test_get_recipe_ids_for_ingredients_returns_correct_list(self,
                                                                 monkeypatch):
        """Tests that we return proper data."""
        def fake_search(unusedself, unusedarg):
            return FakeResponse([
                {"id": 1},
                {"id": 2},
                {"id": 3},
            ])

        monkeypatch.setattr(
            spoonacular_helper.API,
            "search_recipes_by_ingredients",
            fake_search)

        helper = spoonacular_helper.SpoonacularFacade("FAKEKEY")
        output = helper.get_recipe_ids_for_ingredients("fake,stuff")

        assert sorted(output) == [1, 2, 3]

    def test_get_recipe_ids_for_ingredients_limits_recipes(self, monkeypatch):
        """Tests that we return proper data."""
        def fake_search(unusedself, unusedarg):
            return FakeResponse([
                {"id": 1},
                {"id": 2},
                {"id": 3},
            ])

        monkeypatch.setattr(
            spoonacular_helper.API,
            "search_recipes_by_ingredients",
            fake_search)

        helper = spoonacular_helper.SpoonacularFacade("FAKEKEY")
        output = helper.get_recipe_ids_for_ingredients("fake,stuff", 2)

        assert sorted(output) == [1, 2]

    @mock.patch.object(spoonacular_helper, "API", autospec=True)
    def test_get_random_recipe_with_tags_calls_proper_api(self, mock_api):
        """Tests that we call the proper api."""
        helper = spoonacular_helper.SpoonacularFacade("FAKEKEY")
        tags = "fake,list"
        _ = helper.get_random_recipe(tags=tags)

        helper.client.get_random_recipes.assert_called_once_with(tags=tags)

    @mock.patch.object(spoonacular_helper, "API", autospec=True)
    def test_get_random_recipe_no_tags_calls_proper_api(self, mock_api):
        """Tests that we call the proper api."""
        helper = spoonacular_helper.SpoonacularFacade("FAKEKEY")
        _ = helper.get_random_recipe()

        helper.client.get_random_recipes.assert_called_once_with(tags=None)

    def test_get_random_recipe_returns_correct_dict(self, monkeypatch):
        """Tests that we return proper data."""
        FAKE_REC = { "id": 1, "title": "fake"}
        def fake_getter(unusedself, tags=None):
            return FakeResponse({
                "recipes": [FAKE_REC]
            })

        monkeypatch.setattr(
            spoonacular_helper.API,
            "get_random_recipes",
            fake_getter 
        )

        helper = spoonacular_helper.SpoonacularFacade("FAKEKEY")
        output = helper.get_random_recipe()

        assert output == FAKE_REC

    @mock.patch.object(spoonacular_helper, "API", autospec=True)
    def test_get_random_alcoholic_beverage_recipe_id_calls_proper_apis(
        self, mock_api):
        """Tests that we call the proper api."""
        helper = spoonacular_helper.SpoonacularFacade("FAKEKEY")
        _kwargs = {
            "type": "drink",
            "minAlcohol": 7,
            "sort": "random",
            "number": 1,
        }
        _ = helper.get_random_alcoholic_beverage_recipe_id()

        helper.client.search_recipes_complex.assert_called_once_with(
            "", **_kwargs)

    def test_get_random_alc_bev_returns_correct_dict(self, monkeypatch):
        """Tests that we return proper data."""
        result_data = {
            "results": [
                {"id": 1, "title": "test"}
            ]
        }
        
        def fake_search(
            unusedself,
            query,
            type=None,
            minAlcohol=None,
            sort=None,
            number=None):
            return FakeResponse(result_data)

        monkeypatch.setattr(
            spoonacular_helper.API,
            "search_recipes_complex",
            fake_search
        )

        helper = spoonacular_helper.SpoonacularFacade("FAKEKEY")
        output = helper.get_random_alcoholic_beverage_recipe_id()
        assert output == result_data["results"][0]["id"]

    @mock.patch.object(spoonacular_helper, "API", autospec=True)
    def test_get_recipes_for_ids_calls_proper_api(self, mock_api):
        """Tests that we call the proper api."""
        helper = spoonacular_helper.SpoonacularFacade("FAKEKEY")
        fake_ids = [1, 2, 3]
        _ = helper.get_recipes_for_ids(fake_ids)

        helper.client.get_recipe_information_bulk.assert_called_once_with(
            ",".join([str(x) for x in fake_ids])
        )

    def test_get_recipes_for_ids_returns_proper_list(self, monkeypatch):
        """Tests that we return proper data."""
        result_data = [
            {"id": 1, "title": "test"},
            {"id": 2, "title": "fake2"},
        ]
        
        def fake_get_bulk(unusedself, ids):
            return FakeResponse(result_data)

        monkeypatch.setattr(
            spoonacular_helper.API,
            "get_recipe_information_bulk",
            fake_get_bulk 
        )

        helper = spoonacular_helper.SpoonacularFacade("FAKEKEY")
        output = helper.get_recipes_for_ids([1, 2])
        assert output == result_data

    def test_format_recipe_data_as_html_formats_properly(self):
        """Tests that we return properly formatted html."""
        fake_input = {
            "title": "Fake Recipe",
            "extendedIngredients": [
                {"id": 1, "originalString": "Fake ingredient"},
                {"id": 1, "originalString": "Fake ingredient1"},
            ],
            "instructions": "Fake",
            "readyInMinutes": 10,
        }

        expected_output = (
            f"<b>{fake_input['title']}</b>\n"
            f"Cooktime: {fake_input['readyInMinutes']} minutes\n\n"
            f"<u>Ingredients</u>\n"
            f"Fake ingredient\nFake ingredient1\n\n"
            f"<u>Instructions</u>\n"
            f"{fake_input['instructions']}"
        )

        output = spoonacular_helper.SpoonacularFacade.format_recipe_data_as_html(
            fake_input
        )

        assert output == expected_output
