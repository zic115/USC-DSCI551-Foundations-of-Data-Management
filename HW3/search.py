import sys
import mysql.connector

name = sys.argv[1]

cnx = mysql.connector.connect(user = 'dsci551', password = 'Dsci-551', host = 'localhost', database = 'sakila')
cursor = cnx.cursor()

query = "SELECT c.first_name, c.last_name, cl.city FROM customer c LEFT OUTER JOIN customer_list cl ON c.customer_id = cl.ID WHERE first_name = '" + name + "'"
cursor.execute(query)

for result in cursor:
	print(result)

cursor.close()
cnx.close()