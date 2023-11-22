import mysql.connector

hostname ="pe1.h.filess.io"
username ="SpecialProject_oppositeme"
password ="932f64019c479c829cf62d7abf5f19ea8a40c3ab"
database ="SpecialProject_oppositeme"
port = "3307"

mydb = mysql.connector.connect(host=hostname,database=database,user=username,password=password,port=port)

mycursor = mydb.cursor()

sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
val = ("Fluke", "Highway 18")
mycursor.execute(sql, val)
mydb.commit()