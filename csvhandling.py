import numpy as np
import csv
import time


def get_type_of_recipe(recipe_name):
    # print("Getting new recipe")
    recipes_file = open("./data/recipes.csv", encoding="utf-8")
    for x in range(20000):  # 309360
        row = recipes_file.readline()[0:-1]
        if (recipe_name == row.split(",")[0]):
            recipes_file.close()
            return np.array([int(el) for el in row.split(",")[36:63]])
    #return np.array([int(0) for el in range(27)])
    return []

def get_type_of_recipe_local(recipe_name):
    for item in recipe_data:
        if item[0] == recipe_name:
            return np.array([int(el) for el in item[36:63]])
    return []


recipe_data = []
recipes_file = open("./data/recipes.csv", encoding="utf-8")
for x in range(309360):  # 309360
    recipe_data.append(recipes_file.readline()[0:-1].split(","))
recipes_file.close()
print(len(recipe_data))

start_time = time.time()

file = open("./data/reviews.csv", encoding="utf-8")
previous_recipe = ""
current_recipe_value = None
type = "None"
users = {}


num = 7796003
for i in range(num):
    line = file.readline()[0:-1]
    # print(line)
    #print(i / num)
    current_recipe = line.split(",")[0]
    # print(current_recipe_value)
    if previous_recipe != current_recipe:
        current_recipe_value = get_type_of_recipe_local(current_recipe)
    user = line.split(",")[1]
    # print(user)
    if(len(current_recipe_value) != 0): # only add recipes which are in scope (otherwise 00000... would be added)
        try:
            users[user] = users.get(user) + current_recipe_value
        except:
            users[user] = current_recipe_value
    previous_recipe = current_recipe
    # print([int(el) for el in line.split(",")[36:63]])

with open('./data/users.csv', 'a', encoding="utf-8") as file:
    for k, v in users.items():
        if(np.all(v == v[0])):
            favorite = -1
        else:
            favorite = np.argmax(v)
            #print("line: " + k + "" + np.array2string(v) + str(favorite))
            file.write(k + "," + str(favorite) + "\n")

    # print(sum(1 for line in f))
# kochbar_recipes_ratings -> reviews.csv #7796004
# feature_table -> recipes.csv #309360
# kochbar_recipes_category ->countries.csv #3705040

file.close()
print("--- %s seconds ---" % (time.time() - start_time))

# print([int(el) for el in line.split(",")[36:63]])
# print(recipe_name)


# print(get_type_of_recipe("/rezept/99999/Huehnersalat-a-la-Vietnam.html"))
