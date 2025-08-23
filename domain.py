from dataclasses import dataclass
import json
import random
from typing import Generator, Optional
from enum import StrEnum


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

    @staticmethod
    def from_json(name: str, properties: dict):
        return Meal(
            name=name,
            ingredients=properties.get("ingredients"),
            pantry=properties.get("pantry"),
            leftovers=properties.get("leftovers"),
            meal_type=set(MealType(m) for m in properties.get("meal")),
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


class MealSchedule:
    schedule: list[DailySchedule]

    def __init__(self):
        self.schedule = []

    def schedule_full_for(meal_type: str):
        return False

    def fill_schedule(self, days: int, db: MealDatabase):
        self.schedule = [DailySchedule() for _ in range(days)]

        # first do breakfasts, that only have left overs into other breakfasts
        all_breakfasts = db.meals_for_type(MealType.Breakfast)
        current_day = 0
        while current_day < days:
            breakfast = next(all_breakfasts)
            self.schedule[current_day].breakfast = breakfast
            leftovers_remaining = breakfast.leftovers
            while leftovers_remaining > 0 and current_day < (days - 1):
                current_day += 1
                self.schedule[current_day].breakfast = breakfast
                leftovers_remaining -= 1

            current_day += 1

    @property
    def pantry_items(self) -> set[str]:
        items = set()
        for day in self.schedule:
            if day.breakfast is not None:
                items.update(day.breakfast.pantry)
            if day.lunch is not None:
                items.update(day.lunch.pantry)
            if day.dinner is not None:
                items.update(day.dinner.pantry)
        return items


def required_pantry_for(meals: list[Meal]) -> set[str]:
    required_pantry: set[str] = set()
    for meal in meals:
        required_pantry.update(meal.pantry)
    return required_pantry


#db = MealDatabase()
#schedule = MealSchedule()
#schedule.fill_schedule(4, db)
#for day in schedule.schedule:
#    print(day.breakfast.name)