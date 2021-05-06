import mysql.connector
from mysql.connector import errorcode

#TODO
def get_similar_users(cursor, k, category):
    #cursor.execute(query)
    return ["GERE", "tizian"]


def get_pseudo_ratings(cursor, similar_pref_users):
    target_values = ' OR '.join(f"link_name='{elem}'" for elem in similar_pref_users)
    query = f"SELECT id, rating FROM kochbar_recipes_ratings WHERE {target_values}"
    cursor.execute(query)

    pseudo_ratings = {}
    for elem in cursor:
        pseudo_ratings.setdefault(elem[0], []).append(int(elem[1]))
    pseudo_ratings = [(key, sum(values) / len(values)) for key, values in pseudo_ratings.items()]

    return pseudo_ratings


try:
      cnx = mysql.connector.connect(user='readonly', password='RoPlCa_readonly', host='132.199.143.90', port='8306',database='kochbar')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

else:
    cursor = cnx.cursor()

    k = 5
    category = "veggie_overlap"
    similar_pref_users = get_similar_users(cursor, k, category)
    pseudo_ratings = get_pseudo_ratings(cursor, similar_pref_users)

    cnx.close()



    #cursor = cnx.cursor()
    #query = ("SELECT * FROM kochbar_recipes ORDER BY title LIMIT 10")
    #cursor.execute(query)
    #for element in cursor:
    #    print(element)
    #cnx.close()