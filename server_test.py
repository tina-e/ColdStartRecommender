import mysql.connector
from mysql.connector import errorcode

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

    query = ("SELECT * FROM kochbar_recipes ORDER BY title LIMIT 10")

    cursor.execute(query)
    for element in cursor:
        print(element)
    cnx.close()