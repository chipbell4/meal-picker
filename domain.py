from dataclasses import dataclass
import json
import random


@dataclass
class Meal(object):
    name: str
    ingredients: list[str]
    pantry: list[str]
    leftovers: int

    @staticmethod
    def from_json(name: str, properties: dict):
        return Meal(
            name=name,
            ingredients=properties.get("ingredients"),
            pantry=properties.get("pantry"),
            leftovers=properties.get("leftovers"),
        )


def load_meals() -> list[Meal]:
    meals: list[Meal] = []
    with open("meals.json", "r") as f:
        parsed: dict = json.loads(f.read())

    for name, properties in parsed.items():
        meals.append(Meal.from_json(name, properties))

    return meals


def pick_random_meals(n: int) -> list[Meal]:
    all_meals = load_meals()
    return random.sample(all_meals, n)


def required_pantry_for(meals: list[Meal]) -> set[str]:
    required_pantry: set[str] = set()
    for meal in meals:
        required_pantry.update(meal.pantry)
    return required_pantry
