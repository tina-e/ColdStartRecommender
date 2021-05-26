import numpy as np


# TODO (optional für Anzeige am Ende)
def get_recipe_name_by_href(href):
    return "huhn"


def get_categories_by_href(href):
    recipes_file = open("./data/recipes.csv", encoding="utf-8")
    for x in range(309360):  # 309360
        row = recipes_file.readline()[0:-1]
        if (href == row.split(",")[0]):
            recipes_file.close()
            raw = np.array([int(el) for el in row.split(",")[36:63]])
            indices = []
            for x in range(0, len(raw)):
                if raw[x] == 1:
                    indices.append(x)
            indices = np.array(indices)
            return indices
    # return np.array([int(0) for el in range(27)])
    return []


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
    user_file = open("data/reviews.csv", encoding="utf-8")
    for x in range(7796004):  # 7796004
        line = user_file.readline()[0:-1].split(",")
        if line[0] in similar_pref_users:
            recipes[line[1]] = 5
    return recipes


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


def get_pseudo_ratings(user):
    overlap_categories = user.get_category_indices()
    diff_price = [user.level, user.budget]
    similar_users = get_similar_users(overlap_categories)
    print("number of similar users who have mainly rated one of these categories: " + str(len(similar_users)))
    pseudo_ratings = get_recipes_from_users(similar_users)
    pseudo_ratings = modify_pseudo_ratings(pseudo_ratings, diff_price)
    return pseudo_ratings


def modify_recommendations(recommendations, user_dislikes):
    # user_dislikes: [self.has_lactose_intolerance, self.has_gluten_intolerance, self.unwanted_ingredients]
    # recommendations: array an strings
    if user_dislikes[0] == False and user_dislikes[1] == False and len(
            user_dislikes[2]) == 0:  # skip if there are no restrictions
        print("Skipped filtering of recommendations because there are no limitations because of intolerance")
        print("Returning " + str(len(recommendations))+" recommendations")
        return recommendations
    recipes_file = open("./data/recipes.csv", encoding="utf-8")
    final_recommendations = []
    for x in range(309360):  # 309360
        row = recipes_file.readline()[0:-1].split(",")
        if row[0] in recommendations:  # if one recipe has been found
            if not (user_dislikes[0] == int(row[88]) or user_dislikes[1] == int(row[84])):
                final_recommendations.append(row[0])
    print("Returning " + str(len(final_recommendations)) + " recommendations")
    return final_recommendations
