from  fastapi.testclient import TestClient
from  main import app

client = TestClient(app)
data = ("/recipes?"
        "title=Торт%20Шоколадный&"
        "cooking_time=60&"
        "ingredients=Шоколад%2C%20Мука%2C%20Сахар%2C%20Яйца&"
        "description=Вкусный%20шоколадный%20торт")

# data = {
#         "title": "Торт Шоколадный",
#         "cooking_time": 60,
#         "ingredients": "Шоколад, Мука, Сахар, Яйца",
#         "description": "Вкусный шоколадный торт"
#     }

def test_add_recipe():
    response = client.post(data)
    print(response.json())
    assert response.status_code == 200
    response_data = response.json()
    recipe_id = response_data.get("recipe_id")
    assert response.json() == {
        "msg": "Рецепт добавлен",
        "recipe_title": "Торт Шоколадный",
        "recipe_id": recipe_id
    }
    print(f"Рецепт добавлен с ID: {recipe_id}")


def test_get_recipes():
    response = client.get("/recipes")
    print(response.json())
    assert response.status_code == 200


def test_get_recipe_by_id():
    response_add = client.post(data)
    recipe_title = response_add.json().get("recipe_title")

    # Извлекаем ID добавленного рецепта
    recipe_id = response_add.json().get("recipe_id")

    # Получаем рецепт по ID
    response = client.get(f"/recipes/{recipe_id}")

    # Проверяем, что полученный рецепт соответствует добавленному
    assert response.status_code == 200
    assert response.json().get("title") == recipe_title
    assert response.json().get("description") == "Вкусный шоколадный торт"