from user import User
from standard_recommender import UserCF_Recommender

def modify_pseudo_ratings(recipe_list, diff_price):
    user_file = open("./data/difficulty_price.csv", encoding="utf-8")
    for x in range(405863):  # 405863
        line = user_file.readline()[0:-1].split(",")
        if line[0] in recipe_list.keys():
            if diff_price[0] != line[1]:  # modify if difficulty doesnt match - values leicht mittel schwer
                recipe_list[line[0]] = recipe_list[line[0]] - 1
            if diff_price[1] != line[2]:  # modify if price category doesnt match - values 1 3 5
                recipe_list[line[0]] = recipe_list[line[0]] - 1
    return recipe_list

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

def get_pseudo_ratings(user):
    overlap_categories = user.get_category_indices()
    diff_price = [user.level, user.budget]

    similar_users = get_similar_users(overlap_categories)
    print("number of similar users: " + str(len(similar_users)))
    pseudo_ratings = get_recipes_from_users(similar_users)
    print(pseudo_ratings)
    pseudo_ratings = modify_pseudo_ratings(pseudo_ratings, diff_price)
    print("ratings after modification: ")
    print(pseudo_ratings)
    return pseudo_ratings



user = User("test123", "leicht", 1)

recipe_types = ["desserts_overlap", "side_dish_overlap",
                        "meat_and_poultry_overlap", "soups_stews_and_chili_overlap", "cakes_overlap",
                        "breakfast_and_brunch_overlap", "salad_overlap", "pasta_and_noodels_overlap",
                        "appetizers_and_snacks_overlap", "roasts_overlap", "casseroles_overlap",
                        "low_calorie_overlap", "healthy_overlap", "veggie_overlap", "stir_fry_overlap",
                        "asian_style_overlap", "pizza_overlap", "deep_fried_overlap", "italy_and_italian_style_overlap",
                        "candy_overlap", "seafood_overlap", "cookies_overlap", "everyday_cooking_overlap",
                        "dips_and_spreads_overlap", "drinks_overlap", "spirits_overlap"]

problematics = ["dips_and_spreads_overlap", "pizza_overlap", "low_calorie_overlap", "roasts_overlap", "pasta_and_noodels_overlap", "appetizers_and_snacks_overlap"]

for overlap in recipe_types:
    system = UserCF_Recommender()
    user.category_list = [overlap]
    user.pseudo_ratings = get_pseudo_ratings(user)
    system.add_user(user)
    recommendations = system.recommend_items(user.name, 10)
    print(f"recommendations for {overlap}")
    print(recommendations)

print(problematics)
print("fin")
