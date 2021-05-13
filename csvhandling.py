import numpy as np
def get_type_of_recipe(recipe_name):
    recipes_file = open("./data/recipes.csv", encoding="utf-8")
    for row in recipes_file:
        if(recipe_name == row.split(",")[0]):
            recipes_file.close()
            return np.array([int(el) for el in row.split(",")[36:63]])

file = open("./data/recipes.csv",encoding="utf-8")
previous_recipe = ""
current_recipe_value = None
type = "None"
users = {}
for i in range(5000):
    line = file.readline()[0:-1]
    current_recipe = line.split(",")[0]
    if(previous_recipe != current_recipe):
        current_recipe_value = get_type_of_recipe(current_recipe)
    user = line.split(",")[1]
    try:
        users[user] = users.get(user) + current_recipe_value
    except:
        users[user] = current_recipe_value
    previous_recipe = current_recipe
    #print([int(el) for el in line.split(",")[36:63]])
print(users)
    #print(sum(1 for line in f))
#kochbar_recipes_ratings -> reviews.csv #7796004
#feature_table -> recipes.csv #309360
#kochbar_recipes_category ->countries.csv #3705040

file.close()


    #print([int(el) for el in line.split(",")[36:63]])
    #print(recipe_name)


#print(get_type_of_recipe("/rezept/99999/Huehnersalat-a-la-Vietnam.html"))