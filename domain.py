from dataclasses import dataclass
import json
import random
from typing import Generator, Optional
from enum import StrEnum
from collections import defaultdict


class MealType(StrEnum):
    Breakfast = "breakfast"
    Lunch = "lunch"
    Dinner = "dinner"


@dataclass
class Meal(object):
    name: str
    ingredients: list[str]
    pantry: list[str]
    leftovers: int
    meal_type: set[MealType]
    is_leftover: bool = False

    @staticmethod
    def from_json(name: str, properties: dict):
        return Meal(
            name=name,
            ingredients=properties.get("ingredients"),
            pantry=properties.get("pantry"),
            leftovers=properties.get("leftovers"),
            meal_type=set(MealType(m) for m in properties.get("meal")),
        )

    def as_leftover(self) -> "Meal":
        return Meal(
            name=self.name,
            ingredients=self.ingredients,
            pantry=self.pantry,
            leftovers=self.leftovers - 1,
            meal_type=self.meal_type,
            is_leftover=True,
        )


class MealDatabase:
    meals: list[Meal]

    def __init__(self):
        self.meals = []
        with open("meals.json", "r") as f:
            parsed: dict = json.loads(f.read())

        for name, properties in parsed.items():
            self.meals.append(Meal.from_json(name, properties))

    def meals_for_type(self, meal_type: MealType) -> Generator[Meal, None, None]:
        filtered = [m for m in self.meals if meal_type in m.meal_type]
        random.shuffle(filtered)

        k = 0
        while True:
            yield filtered[k]
            k = (k + 1) % len(filtered)


@dataclass
class DailySchedule:
    breakfast: Optional[Meal] = None
    lunch: Optional[Meal] = None
    dinner: Optional[Meal] = None

    @property
    def meals(self) -> Generator[Meal, None, None]:
        if self.breakfast is not None:
            yield self.breakfast

        if self.lunch is not None:
            yield self.lunch

        if self.dinner is not None:
            yield self.dinner

    def __repr__(self) -> str:
        s = "---\n"
        for meal in self.meals:
            s += f"- {meal.name}\n"
        return s


class MealSchedule:
    days: list[DailySchedule]

    def __init__(self):
        self.days = []

    def fill_schedule(self, days: int, db: MealDatabase):
        self.days = [DailySchedule() for _ in range(days)]

        # first do breakfasts, that only have left overs into other breakfasts
        all_breakfasts = db.meals_for_type(MealType.Breakfast)
        current_day = 0
        while current_day < days:
            breakfast = next(all_breakfasts)
            self.days[current_day].breakfast = breakfast
            leftovers_remaining = breakfast.leftovers
            while leftovers_remaining > 0 and current_day < (days - 1):
                current_day += 1
                self.days[current_day].breakfast = breakfast.as_leftover()
                leftovers_remaining -= 1

            current_day += 1

        # Fill the first lunch with something. Once we start adding dinners we'll start using leftovers
        all_lunches = db.meals_for_type(MealType.Lunch)
        self.days[0].lunch = next(all_lunches)

        # Now do dinners and lunches
        all_dinners = db.meals_for_type(MealType.Dinner)
        current_day = 0
        while current_day < days:
            last_dinner = next(all_dinners)
            leftovers_remaining = last_dinner.leftovers
            self.days[current_day].dinner = last_dinner.as_leftover()

            current_day += 1

            if current_day < days:
                # If there's leftovers, we eat that
                if leftovers_remaining > 0:
                    self.days[current_day].lunch = last_dinner.as_leftover()
                # Otherwise, pick a new lunch to cook
                else:
                    self.days[current_day].lunch = next(all_lunches)

    @property
    def pantry_items(self) -> set[str]:
        items = set()
        for day in self.days:
            for meal in day.meals:
                items.update(meal.pantry)
        return items

    def __repr__(self) -> str:
        return "\n".join(str(day) for day in self.days)


@dataclass
class GroceryListItem(object):
    name: str
    count: str
    meals: set[str]


class GroceryList:
    items: defaultdict[int]
    ingredient_to_meal_lookup: defaultdict[set[str]]

    def __init__(self):
        self.items = defaultdict(int)
        self.ingredient_to_meal_lookup = defaultdict(set)

    def add_meal(self, meal: Meal):
        # Don't add the same meal twice to the grocery list if it was a left over
        if meal.is_leftover:
            return

        for ingredient in meal.ingredients:
            self.items[ingredient] += 1
            self.ingredient_to_meal_lookup[ingredient].add(meal.name)

    def add_day(self, day: DailySchedule):
        for meal in day.meals:
            self.add_meal(meal)

    def add_schedule(self, schedule: MealSchedule):
        for day in schedule.days:
            self.add_day(day)

    def __iter__(self) -> Generator[GroceryListItem, None, None]:
        sorted_items = sorted(self.items.keys())
        for item_name in sorted_items:
            yield GroceryListItem(
                name=item_name,
                count=self.items[item_name],
                meals=self.ingredient_to_meal_lookup[item_name],
            )


def required_pantry_for(meals: list[Meal]) -> set[str]:
    required_pantry: set[str] = set()
    for meal in meals:
        required_pantry.update(meal.pantry)
    return required_pantry


db = MealDatabase()
schedule = MealSchedule()
schedule.fill_schedule(10, db)
for day in schedule.days:
    print(f"{day.breakfast.name}, {day.lunch.name}, {day.dinner.name}")

print(schedule.pantry_items)
