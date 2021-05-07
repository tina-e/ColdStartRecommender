import mysql.connector
from mysql.connector import errorcode
import random


def get_similar_users(cursor, k, category):
    recipes = get_recipes_by_category(cursor, category)
    users = []
    for recipe_id in recipes:
        users.append(get_users_who_rated_recipe(cursor, recipe_id[0]))
    print(len(list(dict.fromkeys([item for sublist in users for item in sublist]))))
    return list(dict.fromkeys([item for sublist in users for item in sublist]))[0:k] #TODO pick out k ? random.shuffle(list) [0:k] klappt iwie nicht weil shuffle none liefert

    #return ['gernd0110', 'tigerherz333', 'Skippy2007', 'SoulDiva', 'PolskaKucharka']

def get_users_who_rated_recipe(cursor, recipe_id):
    cursor.execute("SELECT link_name FROM kochbar_recipes_ratings WHERE id = '" + str(recipe_id) + "'" + "AND rating = '5'")
    return([el[0] for el in cursor])

#returns all recipe_ids of a specific category with more than 100 ratings and at least 4.5 starts
def get_recipes_by_category(cursor, category):
    query = "SELECT recipe_id FROM feature_table WHERE " + category + " = '1' AND avg_rating >= 4.5 AND number_of_ratings >= 100"
    cursor.execute(query)
    return [el for el in cursor]


def get_pseudo_ratings(cursor, similar_pref_users, only_multiple_occurence):
    target_values = ' OR '.join(f"link_name='{elem}'" for elem in similar_pref_users)
    query = f"SELECT id, rating FROM kochbar_recipes_ratings WHERE {target_values}"
    #query = f"SELECT count(id), id, rating FROM kochbar_recipes_ratings WHERE {target_values} GROUP BY id, rating HAVING count(id) > 1"
    cursor.execute(query)

    collected_ratings = {}
    for elem in cursor:
        collected_ratings.setdefault(elem[0], []).append(int(elem[1]))

    if only_multiple_occurence:
        pseudo_ratings = {}
        for key, values in collected_ratings.items():
            if len(values) > 1:
                pseudo_ratings[key] = sum(values) / len(values)
        return pseudo_ratings
    return [(key, sum(values) / len(values)) for key, values in collected_ratings.items()]


try:
      cnx = mysql.connector.connect(user='readonly', password='RoPlCa_readonly', host='132.199.143.90', port='8306', database='kochbar')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

else:
    cursor = cnx.cursor()

    k = 10
    category = "veggie_overlap"

    similar_pref_users = get_similar_users(cursor, k, category)
    print(similar_pref_users)

    pseudo_ratings = get_pseudo_ratings(cursor, similar_pref_users, True)
    for key, value in pseudo_ratings.items():
        print(key, value)
    print(len(pseudo_ratings))
    cnx.close()


    # cursor = cnx.cursor()
    # query = ("SELECT * FROM kochbar_recipes ORDER BY title LIMIT 10")
    # cursor.execute(query)
    # for element in cursor:
    #    print(element)
    # cnx.close()
