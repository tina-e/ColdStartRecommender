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
            raw = np.array([int(el) for el in row.split(",")[36:63]])
            indices = []
            for x in range(0, len(raw)):
                if(raw[x] == 1):
                    indices.append(x)
            indices = np.array(indices)
            #print([el for el in range(0, len(raw)) if 1 in raw[el]])
            return indices
    # return np.array([int(0) for el in range(27)])
    return []




