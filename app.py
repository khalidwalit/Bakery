from MySQLdb._mysql import connection
import re
from flask import Flask, render_template, request, redirect, session, url_for, flash
import MySQLdb
from flask_mysqldb import MySQL

import mysql.connector
from mysql.connector import cursor
import MySQLdb.cursors
from werkzeug.exceptions import abort

app = Flask(__name__)
app.secret_key = "1234353234"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "fatin222"
app.config["MYSQL_DB"] = "login"

db = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/customer')
def customer():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        if "five" in request.form and "one" in request.form and "two" in request.form and "three" in request.form and \
                "four" in request.form and "six" in request.form:
            username = request.form['five']
            custname = request.form['one']
            custphone = request.form['two']
            custaddress = request.form['three']
            custemail = request.form['four']
            custpassword = request.form['six']

            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO login.customer(username,custName,custPhone, custAddress, custEmail, "
                        "custPassword)VALUES(%s,%s,%s,%s,%s,%s)", (username, custname, custphone, custaddress,
                                                                   custemail, custpassword))
            db.connection.commit()
            msg = 'You have successfully registered!'
        # Show registration form with message (if any)
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'custPassword' in request.form:
        # Create variables for easy access
        username = request.form['username']
        custpassword = request.form['custPassword']
        # Check if account exists using MySQL
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE username = %s AND custPassword = %s', (username, custpassword,))
        # Fetch one record and return result
        customer= cursor.fetchone()
        # If account exists in accounts table in out database
        if customer:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['custID'] = customer['custID']
            session['username'] = customer['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect Username/Password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)


@app.route('/homepage')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('homepage.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE custID = %s', (session['custID'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route("/update_account", methods=['GET', 'POST'])
def update_account():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'five' in request.form and 'one' in request.form and 'two' in request.form and \
                'three' in request.form and 'four' in request.form and 'six' in request.form:
            username = request.form['five']
            custname = request.form['one']
            custphone = request.form['two']
            custaddress = request.form['three']
            custemail = request.form['four']
            custpassword = request.form['six']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM customer WHERE username = %s', (session['username'], ))
            account = cursor.fetchone()
            cursor.execute('UPDATE customer SET username =% s,custName =%s, custPhone =%s, custAddress =%s, \
                custEmail =%s, custPassword =%s', (username, custname, custphone, custaddress, custemail, custpassword, ))
            db.connection.commit()
            msg = 'You have successfully updated !'
        return render_template("updateAccount.html", msg=msg)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('custID', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


@app.route('/admin')
def admin():
    return render_template('loginadmin.html')


@app.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    if request.method == "POST":
        if "seven" in request.form and "eight" in request.form and "nine" in request.form and "ten" in request.form \
                and "eleven" in request.form:
            adminname = request.form['seven']
            adminphone = request.form['eight']
            adminemail = request.form['nine']
            adminusername = request.form['ten']
            adminpassword = request.form['eleven']

            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO login.admin(adminName,adminPhone,adminEmail, adminUsername, adminPassword)"
                        "VALUES(%s,%s,%s,%s,%s)", (adminname, adminphone, adminemail, adminusername, adminpassword))
            db.connection.commit()
            msg = 'You have successfully registered!'
        # Show registration form with message (if any)
    return render_template("registeradmin.html")


@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'adminUsername' in request.form and 'adminPassword' in request.form:
        # Create variables for easy access
        adminusername = request.form['adminUsername']
        adminpassword = request.form['adminPassword']
        # Check if account exists using MySQL
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login.admin WHERE adminUsername = %s AND adminPassword = %s',
                       (adminusername, adminpassword,))
        # Fetch one record and return result
        admin = cursor.fetchone()
        # If account exists in accounts table in out database
        if admin:
            # Create session data, we can access this data in other routes
            session['logged_in'] = True
            session['adminID'] = admin['adminID']
            session['adminUsername'] = admin['adminUsername']
            # Redirect to home page
            return redirect(url_for('admin_page'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect adminUsername/adminPassword!'
    # Show the login form with message (if any)
    return render_template('dashboard.html', msg=msg)


@app.route('/admin_page')
def admin_page():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('adminpage.html', adminusername=session['adminUsername'])
    # User is not loggedin redirect to login page
    return redirect(url_for('admin'))


@app.route('/profile_admin')
def profile_admin():
    # Check if user is loggedin
    if 'logged_in' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE adminID = %s', (session['adminID'],))
        admin = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profileAdmin.html', admin=admin)
    # User is not loggedin redirect to login page
    return redirect(url_for('admin_page'))


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout_admin')
def logout_admin():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('adminID', None)
    session.pop('adminUsername', None)
    # Redirect to login page
    return redirect(url_for('admin_page'))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/cake')
def cake():
    return render_template('cakes.html')


@app.route('/faq')
def faq():
    return render_template('FAQ.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


def recommend():
    # Define the recipe data (example)
    recipes = [
        {
            "recipe_id": 1,
            "recipe_name": "Burn Cheesecake",
            "ingredients": [
                {"name": "Cream Cheese", "quantity": "250g"},
                {"name": "Icing Sugar", "quantity": "60g"},
                {"name": "Flour", "quantity": "5g"},
                {"name": "Eggs", "quantity": "2"},
                {"name": "Whipped Cream", "quantity": "150g"},
            ]
        },
        {
            "recipe_id": 2,
            "recipe_name": "Vanilla Sponge Cake",
            "ingredients": [
                {"name": "Egg Whites", "quantity": "4"},
                {"name": "Vanilla", "quantity": "1 tsp"},
                {"name": "Sugar", "quantity": "120g"},
                {"name": "Flour", "quantity": "120g"},
                {"name": "Oil ", "quantity": "30g"},
                {"name": "Milk ", "quantity": "40g"},
                {"name": "Vanilla ", "quantity": "1/2 tsp"},
            ]
        },
        {
            "recipe_id": 3,
            "recipe_name": "Pandan Gula Melaka",
            "ingredients": [
                {"name": "Cake Flour", "quantity": "200g"},
                {"name": "Butter", "quantity": "125g"},
                {"name": "Salt ", "quantity": "1/2 tsp"},
                {"name": "Essence", "quantity": "1/2 tsp"},
                {"name": "Caster Sugar", "quantity": "160g"},
                {"name": "Eggs", "quantity": "2"},
                {"name": "Coconut Milk", "quantity": "75g"},
                {"name": "Water", "quantity": "25g"},
                {"name": "Pandan Leaves Juice", "quantity": " 2 tsp"},
                {"name": "Gula Melaka", "quantity": "50g"},
                {"name": "Sugar", "quantity": "1 tsp"},
            ]

        },
        {
            "recipe_id": 4,
            "recipe_name": "Chocolate Moist Cake",
            "ingredients": [
                {"name": "Self-Rising Flour", "quantity": "25g"},
                {"name": "Eggs", "quantity": "2"},
                {"name": "Sugar", "quantity": "200g"},
                {"name": "Vanilla", "quantity": "15g"},
                {"name": "Milk ", "quantity": "125ml"},
                {"name": "Oil ", "quantity": "83ml"},
                {"name": "Hot Water ", "quantity": "83ml"},
                {"name": "Coffee ", "quantity": "1 tsp"},
                {"name": "Baking Soda ", "quantity": "1 tsp"},
            ]
        },
        {
            "recipe_id": 5,
            "recipe_name": "Rainbow Cake",
            "ingredients": [
                {"name": "Unsalted Butter", "quantity": "250g"},
                {"name": "Sugar", "quantity": "225g"},
                {"name": "Eggs", "quantity": "3"},
                {"name": "Vanilla", "quantity": " 1 tsp"},
                {"name": "Baking Powder ", "quantity": "2 tsp"},
                {"name": "Whole Milk ", "quantity": "50g"},
                {"name": "Rainbow Food Coloring ", "quantity": "6 tsp"},
            ]
        },
    ]
    return recipes


recipes = recommend()
print(recipes)


@app.route('/create_order')
def create_order():
    return render_template('createOrder.html')


@app.route('/view_order')
def view_order():
    return render_template('viewOrder.html')


@app.route('/index_product')
def index_product():
    return render_template('indexProduct.html')


@app.route('/update_product')
def update_product():
    return render_template('updateProduct.html')


@app.route('/create_product')
def create_product():
    return render_template('createProduct.html')


@app.route('/create_sales')
def create_sales():
    return render_template('createRecordSales.html')


if __name__ == '__main__':
    app.run(debug=True)
