recipes = [


for recipe in recipes
  #get maching ingredient in recipes and user_input
  for ingredient in user_ingredients:
    if ingredient in recipe["ingredients"]:
        matching_ingredients.append(ingredient)

  matching_recipes = []

  for recipe in recipes:
      matching_ingredients = []
      for ingredient in user_ingredients:
          if ingredient in recipe["ingredients"]:
              matching_ingredients.append(ingredient)
      if len(matching_ingredients) > 0:
          matching_recipes.append({
              "recipe_id": recipe["recipe_id"],
              "recipe_name": recipe["recipe_name"],
              "matching_ingredients": matching_ingredients
          })