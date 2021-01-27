import mysql.connector

mydb = mysql.connector.connect(host="localhost", user='dheeraj', password='1234', auth_plugin='mysql_native_password', database="test")

mycursor = mydb.cursor()

class insert:
	def ins(name, college):
		mycursor.execute("insert into student(name, college) values(%s, %s)",(name, college))
		mydb.commit()
