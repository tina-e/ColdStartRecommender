import mysql.connector
from mysql.connector import errorcode
import random
import csv
import numpy as np
import time



try:
    cnx = mysql.connector.connect(user='readonly', password='RoPlCa_readonly', host='132.199.143.90', port='8306',
                                  database='kochbar')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

else:
    start_time = time.time()
    # qu = "SELECT id, link_name, rating FROM kochbar_recipes_ratings" #-> reviews.csv
    # qu = "SELECT recipe_href, Schwierigkeitsgrad, Preiskategorie FROM kochbar_recipes" #-> reviews.csv
    # qu = "SELECT * FROM feature_table" #-> recipes.csv
    # qu = "SELECT COUNT(distinct category_label) FROM kochbar_recipes_category"
    # cursor = cnx.cursor()
    # cursor.execute(qu)
    # c = 0
    # for el in cursor:
    #    print(el)
    #    c = c + 1
    # print(c)
    # print(48717 / 7796004)
    # 7724641  5 star -> 0.990846
    # 48717 4 star -> 0.006248
    # 9454 3 star
    # 3196 2 star
    # 9996 1 star

    # rows = cursor.fetchall()
    # fp = open('./data/challenge.csv', 'w', encoding="utf-8", newline='')
    # myFile = csv.writer(fp, delimiter = ",")
    # myFile.writerows(rows)
    # fp.close()

    cnx.close()


    # for element in recipe_types:
    #     if element == "main_dish_overlap" or element == "desserts_overlap":
    #         print("continue")
    #         continue
    #     categories = [recipe_types.index(element)]
    #     similar_users = get_similar_users_from_file(categories)
    #     print("number of similar users for " +element+": "+ str(len(similar_users)))
    #     pseudo_ratings = get_pseudo_ratings_from_file(similar_users)
    #     print(len(pseudo_ratings.keys()))
    # #desserts: 2369 users, 41809


    print("--- %s seconds ---" % (time.time() - start_time))
