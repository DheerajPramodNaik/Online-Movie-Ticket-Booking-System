from flask import Flask, request, render_template, redirect, url_for, Response, json
from werkzeug.utils import secure_filename
from flask_cors import cross_origin
import mysql.connector
import insert
import yaml

UPLOAD_FOLDER = '/static/img'

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)

db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)

mydb = mysql.connector.connect(host=db['mysql_host'], user=db['mysql_user'], password=db['mysql_password'], auth_plugin='mysql_native_password', database=db['mysql_db'])



#---- Load The Welcome Page ----

@app.route('/')
@cross_origin()
def index():
	return render_template("index.html")



#--- Opens the Admin Login Page on clicking "Enter as Admin" ---

@app.route('/admin_login')
@cross_origin()
def admin_login():
	return render_template("admin_login.html")



#--- Function to login (For Admins) ---

@app.route('/admin_login', methods = ["GET", "POST"])
def login():
	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]
		mycursor = mydb.cursor()
		mycursor.execute("select passwd from admin where email='{}' ".format(email))
		temp = mycursor.fetchone()
		if temp != None:
			temp1 = temp[0]
			if temp1 == password:
				return redirect(url_for('admin_options'))
			else:
				return render_template('admin_login.html',text="Wrong Password")
		else:
			return render_template('admin_login.html',text="User Not Found")

	return render_template('admin_login.html')



#--- Loads the Admin Options page ---

@app.route('/admin_options')
@cross_origin()
def admin_options():
	return render_template("admin_options.html")



#--- Opens the Webpage for Updating Movies in Database (For Admins) ---

@app.route('/update_movie_database')
@cross_origin()
def update_movie_database():
	mycursor = mydb.cursor()
	mycursor.execute("select * from movie")
	temp = mycursor.fetchall()
	return render_template("update_mov_database.html", data=temp)

@app.route('/update_movie_database', methods = ["GET", "POST"])
def add_mov():
	if request.method == "POST":
		mov_name_1 = request.form["mov-name-1"]
		file_1 = request.form["file-1"]
		actors_1 = request.form["actors-1"]
		director_1 = request.form["director-1"]
		price_1 = request.form["price-1"]
		time_1 = request.form["time-1"]

		mov_name_2 = request.form["mov-name-2"]
		file_2 = request.form["file-2"]
		actors_2 = request.form["actors-2"]
		director_2 = request.form["director-2"]
		price_2 = request.form["price-2"]
		time_2 = request.form["time-2"]

		mov_name_3 = request.form["mov-name-3"]
		file_3 = request.form["file-3"]
		actors_3 = request.form["actors-3"]
		director_3 = request.form["director-3"]
		price_3 = request.form["price-3"]
		time_3 = request.form["time-3"]

		if file_3 == '':
			return render_template("update_mov_database.html", text="empty")
		
	return render_template("update_mov_database.html", text=file_3)



@app.route('/user_info')
@cross_origin()
def user_info():
	mycursor = mydb.cursor()
	mycursor.execute("select cust_id,username,email,phone,dob,no_of_bookings from user")
	temp = mycursor.fetchall()
	return render_template("user_info.html", data=temp)

@app.route('/booking_info')
@cross_origin()
def booking_info():
	mycursor = mydb.cursor()
	mycursor.execute("select * from tickets")
	temp = mycursor.fetchall()
	return render_template("booking_info.html", data=temp)

@app.route('/user_login')
@cross_origin()
def user_login():
	return render_template("user_login.html")	



@app.route('/user_login', methods = ["GET", "POST"])
def user_login_function():
	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]
		mycursor = mydb.cursor()
		mycursor.execute("select passwd from user where email='{}' ".format(email))
		temp = mycursor.fetchone()
		if temp != None:
			temp1 = temp[0]
			if temp1 == password:
				mycursor.execute("select username from user where email='{}' ".format(email))
				name = mycursor.fetchone()
				name1 = name[0]
				return redirect(url_for('user_options'))
			else:
				return render_template('user_login.html',text="Wrong Password")
		else:
			return render_template('user_login.html',text="User Not Found")

	return render_template('user_login.html')




@app.route('/register')
@cross_origin()
def register():
	return render_template("user_registration.html")



@app.route('/register', methods = ["GET", "POST"])
def user_register_function():
	if request.method == "POST":
		name = request.form["name"]
		mobile = int(request.form["mobile"])
		email = request.form["email"]
		password = request.form["password"]
		date = request.form["date"]
		book = 0
		val = (name, email, mobile, date, password, book)
		sql = "insert into user (username, email, phone, dob, passwd, no_of_bookings) values (%s, %s, %s, %s, %s, %d)"
		try:
			mycursor = mydb.cursor()
			mycursor.execute(sql, val)
			mydb.commit()
			return redirect(url_for('user_options'))
		except mysql.connector.Error as e:
			warn = "Mobile Number Or Email Already Exists"
			return render_template('user_registration.html', text=warn)



	
@app.route('/user_options')
@cross_origin()
def user_options():
	return render_template("user_options.html")



@app.route('/book_tickets')
@cross_origin()
def book_tickets():
	mycursor = mydb.cursor()
	mycursor.execute("select movie_name from movie")
	temp = mycursor.fetchall()

	mycursor.execute("select ticket_price from movie")
	p1 = mycursor.fetchall()
	price = []
	for i in p1:
		for j in i:
			price.append(j)

	mycursor.execute("select snack_name,price from snacks")
	temp1 = mycursor.fetchall()

	mycursor.execute("select movie_id from movie")
	mov_id = mycursor.fetchall()

	mycursor.execute("select seat_id from seats where movie_id=101 and occupied=0 ")
	m1 = mycursor.fetchall()
	mov_1 = []
	for i in m1:
		for j in i:
			mov_1.append(j)

	mycursor.execute("select seat_id from seats where movie_id=102 and occupied=0 ")
	m2 = mycursor.fetchall()
	mov_2 = []
	for i in m2:
		for j in i:
			mov_2.append(j)

	mycursor.execute("select seat_id from seats where movie_id=103 and occupied=0 ")
	m3 = mycursor.fetchall()
	mov_3 = []
	for i in m3:
		for j in i:
			mov_3.append(j)

	mycursor.execute("select price from snacks")
	s1 = mycursor.fetchall()
	snack = []
	for i in s1:
		for j in i:
			snack.append(j)

	return render_template("book_tickets.html", movies=temp, snack=temp1, price=json.dumps(price), ids=mov_id, mov_1=mov_1, mov_2=mov_2, mov_3=mov_3, snck=json.dumps(s1))



@app.route('/book_tickets', methods = ["GET", "POST"])
@cross_origin()
def book_tickets_now():
	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]
		mycursor = mydb.cursor()
		mycursor.execute("select passwd from user where email='{}' ".format(email))
		temp = mycursor.fetchone()
		if temp != None:
			temp1 = temp[0]
			if temp1 == password:
				mycursor.execute("select cust_id from user where email='{}' ".format(email))
				temp_id = mycursor.fetchone()
				cust_id = temp_id[0]

				mycursor.execute("select username from user where email='{}' ".format(email))
				temp_name = mycursor.fetchone()
				username = temp_name[0]

				mycursor.execute("select phone from user where email='{}' ".format(email))
				temp_phone = mycursor.fetchone()
				phone = temp_phone[0]

				select = request.form.get("movie-name")

				mycursor.execute("select movie_id from movie where movie_name='{}' ".format(select))
				temp_mov = mycursor.fetchone()
				movie_id = temp_mov[0]

				seats = request.form.getlist("mov-1") + request.form.getlist("mov-2") + request.form.getlist("mov-3")
				radio = request.form["chk"]
				seat_string = ' / '
				seat_string = seat_string.join(seats)
				total_price = int(request.form["totalPrice"])
				no_of_tickets = len(seats)

				mycursor.execute("select no_of_bookings from user where email='{}' ".format(email))
				temp_bookings = mycursor.fetchone()
				no_of_bookings = temp_bookings[0]

				if radio == "Yes":
					popcorn = int(request.form["popcorn"])
					burger = int(request.form["burger"])
					fries = int(request.form["fries"])
					coke = int(request.form["coke"])
				else:
					popcorn = 0
					burger = 0
					fries = 0
					coke = 0

				mycursor.execute("select ticket_id from tickets where movie_name='{}' and email='{}'  ".format(select, email))
				verify = mycursor.fetchone()

				if verify != None:
					return render_template('book_tickets.html',text="You have already booked tickets of this movie")
				else:
					try:
						for i in range(no_of_tickets):
							mycursor.execute("update seats set occupied=1 where seat_id='%s'"%seats[i])
							mydb.commit()

						val = (cust_id, username, phone, email, movie_id, select, no_of_tickets, seat_string, popcorn, burger, fries, coke, total_price)
						sql = "insert into tickets (cust_id, username, phone, email, movie_id, movie_name, no_of_tickets, seats, popcorn, burger, fries, coke, total_price) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
						
						mycursor.execute(sql, val)
						mydb.commit()

						no_of_bookings = no_of_bookings + 1
						mycursor.execute("update user set no_of_bookings=%d where email='%s'"%(no_of_bookings, email))
						mydb.commit()

						return render_template('book_tickets.html', text="Tickets Booked Successfully")
					except mysql.connector.Error as e:
						warn = "You need to select the seats"
						return render_template('book_tickets.html', text=e)
				
			else:
				return render_template('book_tickets.html',text="Wrong Password")
		else:
			return render_template('book_tickets.html',text="Email Not Found! Please Register")


	return render_template("book_tickets.html")


@app.route('/delete_user')
@cross_origin()
def delete_user():
	return render_template("confirm_delete.html")



@app.route('/delete_user', methods = ["GET", "POST"])
@cross_origin()
def confirm_delete():
	if request.method == "POST":
		email = request.form["email"]
		confirm = request.form["confirm"]
		password = request.form["password"]
		mycursor = mydb.cursor()
		mycursor.execute("select passwd from user where email='{}' ".format(email))
		temp = mycursor.fetchone()

		if temp != None:
			temp1 = temp[0]
			if temp1 == password:
				if confirm == "CONFIRM":
					mycursor = mydb.cursor()
					mycursor.execute("delete from user where email='{}' ".format(email))
					mydb.commit()
					return render_template('confirm_delete.html', text="Account Deleted Successfully")
				else:
					return render_template('confirm_delete.html', text="Please Type \"CONFIRM\"  in Caps")
			else:
				return render_template('confirm_delete.html', text="Wrong Password")
		else:
			return render_template('confirm_delete.html', text="User Not Found")



if __name__ == '__main__':
	app.run(debug=True)

#eturn f"<html><body><p>You will be redirected in 3 seconds</p><script>var timer = setTimeout(function() {{window.location='{ <redirect url> }'}}, 3000);</script></body></html>" 