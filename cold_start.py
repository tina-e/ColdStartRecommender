import csv
import numpy as np
import time


def get_similar_users(list_of_categories):
    return_users = []
    user_file = open("./data/users.csv", encoding="utf-8")
    for x in range(16187):  # 16187
        line = user_file.readline()[0:-1].split(",")
        if int(line[1]) in list_of_categories:
            return_users.append(line[0])
    return return_users

def get_recipes_from_users(similar_pref_users):
    recipes = {}
    user_file = open("./data/reviewsV2.csv", encoding="utf-8")
    for x in range(7796004):  # 7796004
        line = user_file.readline()[0:-1].split(",")
        if line[0] in similar_pref_users:
            recipes[line[1]] = 5
    return recipes

def modify_pseudo_ratings(recipe_list):
    print("?")
    return ""

def get_pseudo_ratings(overlap_categories):
    categories = [recipe_types.index(el) for el in overlap_categories]
    similar_users = get_similar_users(categories)
    print("number of similar users: " + str(len(similar_users)))
    pseudo_ratings = get_recipes_from_users(similar_users)
    print(pseudo_ratings)
    pseudo_ratings = modify_pseudo_ratings(pseudo_ratings)
    print("ratings after modification: " + pseudo_ratings)

start_time = time.time()
# banned: main_dish
recipe_types = ["desserts_overlap", "main_dish_overlap", "side_dish_overlap",
                "meat_and_poultry_overlap", "soups_stews_and_chili_overlap", "cakes_overlap",
                "breakfast_and_brunch_overlap", "salad_overlap", "pasta_and_noodels_overlap",
                "appetizers_and_snacks_overlap", "roasts_overlap", "casseroles_overlap",
                "low_calorie_overlap", "healthy_overlap", "veggie_overlap", "stir_fry_overlap",
                "asian_style_overlap", "pizza_overlap", "deep_fried_overlap", "italy_and_italian_style_overlap",
                "candy_overlap", "seafood_overlap", "cookies_overlap", "everyday_cooking_overlap",
                "dips_and_spreads_overlap", "drinks_overlap", "spirits_overlap"]


get_pseudo_ratings(["candy_overlap", "seafood_overlap"])

print()
print("--- %s seconds ---" % (time.time() - start_time))
