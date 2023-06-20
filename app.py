from MySQLdb._mysql import connection
import re
from flask import Flask, render_template, request, redirect, session, url_for
import MySQLdb
from flask_mysqldb import MySQL
import mysql.connector
from mysql.connector import cursor
import MySQLdb.cursors


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


@app.route('/homepage')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('homepage.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/customer')
def customer():
    return render_template('login.html')


@app.route('/admin')
def admin():
    return render_template('loginadmin.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create_order')
def create_order():
    return render_template('createOrder.html')


@app.route('/view_order')
def view_order():
    return render_template('viewOrder.html')


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.route('/product')
def product():
    return render_template('productpages.html')


@app.route('/faq')
def faq():
    return render_template('FAQ.html')


@app.route('/index_product')
def index_product():
    return render_template('indexProduct.html')


@app.route('/create_product')
def create_product():
    return render_template('createProduct.html')


@app.route('/update_product')
def update_product():
    return render_template('updateProduct.html')


@app.route('/create_sales')
def create_sales():
    return render_template('createRecordSales.html')


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
        cursor.execute('SELECT * FROM logininfo WHERE username = %s AND custPassword = %s', (username, custpassword,))
        # Fetch one record and return result
        logininfo = cursor.fetchone()
        # If account exists in accounts table in out database
        if logininfo:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['custID'] = logininfo['custID']
            session['username'] = logininfo['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/custPassword!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('custID', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/register - this will be the registration page,
# we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        if "five" in request.form and "one" in request.form and "two" in request.form and "three" in request.form and\
              "four" in request.form and "six" in request.form:
            username = request.form['five']
            custname = request.form['one']
            custphone = request.form['two']
            custaddress = request.form['three']
            custemail = request.form['four']
            custpassword = request.form['six']

            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO login.logininfo(username,custName,custPhone, custAddress, custEmail, "
                        "custPassword)VALUES(%s,%s,%s,%s,%s,%s)", (username, custname, custphone, custaddress,
                                                                   custemail, custpassword))
            db.connection.commit()
            msg = 'You have successfully registered!'
        # Show registration form with message (if any)
    return render_template("register.html")


# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM logininfo WHERE custID = %s', (session['custID'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# Define a route for the account update page
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
            cursor.execute('SELECT * FROM logininfo WHERE username = %s', (session['username'], ))
            account = cursor.fetchone()
            cursor.execute('UPDATE logininfo SET username =% s,custName =%s, custPhone =%s, custAddress =%s, \
                custEmail =%s, custPassword =%s', (username, custname, custphone, custaddress, custemail, custpassword, ))
            db.connection.commit()
            msg = 'You have successfully updated !'
        return render_template("updateAccount.html", msg=msg)


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
        cursor.execute('SELECT * FROM admin WHERE adminUsername = %s AND adminPassword = %s', (adminusername,
                                                                                               adminpassword,))
        # Fetch one record and return result
        admin = cursor.fetchone()
        # If account exists in accounts table in out database
        if admin:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['adminID'] = admin['adminID']
            session['adminUsername'] = admin['adminUsername']
            # Redirect to home page
            return redirect(url_for('dashboard'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect adminUsername/adminPassword!'
    # Show the login form with message (if any)
    return render_template('loginadmin.html', msg=msg)


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout_admin')
def logout_admin():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('adminID', None)
    session.pop('adminUsername', None)
    # Redirect to login page
    return redirect(url_for('admin'))


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


@app.route('/profile_admin')
def profile_admin():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE adminID = %s', (session['adminID'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('dashboard.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login_admin'))


if __name__ == '__main__':
    app.run(debug=True)
