# meal-picker
A little tool for figuring out what we're going to eat this week.
Here's a typical usage:
```
$ ./meal-picker -n 3 # give me 3 meals
--------------------------------------------------------------------------------
Tofu Stir Fry
Tofu Curry
Blackened Chicken Salad
--------------------------------------------------------------------------------
Seed was 1752582683
Dry-run only. Set -r to actually save to Reminders

$ ./meal-picker -n 3 -s 1752582683 -r # I like those choices, add 'em to my Reminders lists
```

Basically, I'll spam `./meal-picker -n 3` a bunch until I get a menu I like,
then I'll "save it" to my Groceries list in the Reminders app by adding the
`-r` flag.

For this to work for you need to
- Be on a Mac
- Have a list in the Reminders app called "Groceries"
- Have a calendar in your Calendar app called "Meals"

The nice part about this is that if you're logged into iCloud, the list will
automatically sync to your phone and voilá you have a grocery list. The list of
meals/ingredients is in `meals.json`. Feel free to fork and add your own meals.
