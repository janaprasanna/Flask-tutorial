import mysql.connector
#connecting to db server
db = mysql.connector.connect(host="localhost", user="root", passwd="rootjana")
#creating a cursor to write sql queries
cursor = db.cursor()


#cursor.execute("CREATE DATABASE users")

cursor.execute("SHOW DATABASES")
for db in cursor:
    print(db)



