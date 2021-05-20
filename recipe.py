import numpy as np

#TODO (optional für Anzeige am Ende)
def get_recipe_name_by_href(href):
    return "huhn"

def get_categories_by_href(href):
    # print("Getting new recipe")
    recipes_file = open("./data/recipes.csv", encoding="utf-8")
    for x in range(309360):  # 309360
        row = recipes_file.readline()[0:-1]
        if (href == row.split(",")[0]):
            recipes_file.close()
            return np.array([int(el) for el in row.split(",")[36:63]])
    # return np.array([int(0) for el in range(27)])
    return []




