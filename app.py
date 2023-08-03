import secrets

from MySQLdb._mysql import connection
import re
from flask import Flask, render_template, request, redirect, session, url_for, flash, current_app
import MySQLdb
from flask_login import login_required, current_user
from flask_mysqldb import MySQL

import mysql.connector
from mysql.connector import cursor
import MySQLdb.cursors
from werkzeug.exceptions import abort


def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


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


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if'loggedin' in session:
        if "custPhone" in request.form and "custAddress" in request.form:

            custphone = request.form['custPhone']
            custaddress = request.form['custAddress']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            print(session)
            #cursor.execute('SELECT * FROM customer WHERE custID = 24', (session['custID']))
            #account = cursor.fetchone()
            #if account:
                #msg = 'Account already exists !'
            #if not re.match(r"01\d{7}$", custphone):
               # msg = 'Invalid phone number!'
            #elif not re.match(r'[A-Za-z0-9]+', custaddress):
             #   msg = 'address must contain only characters and numbers !'
            #else:
            query = "UPDATE customer SET custPhone = %s, custAddress = %s WHERE custID = %s"
            values = (request.form['custPhone'], request.form['custAddress'], session['custID'])
            cursor.execute(query, values)
            db.connection.commit()
            print(cursor.rowcount, "record(s) affected")
            msg = 'You have successfully updated !'
            return redirect(url_for('profile'))
    return redirect(url_for('update'))


@app.route('/update')
def update():
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    print(session)
    cursor.execute("""SELECT * FROM customer WHERE custID = %s """, (session['custID'],))
    account = cursor.fetchone()
    print('account', account)
    return render_template("updateAccount.html", account=account)


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
    # Check if "adminUsername" and "adminPassword" POST requests exist (user submitted form)
    if request.method == 'POST' and 'adminUsername' in request.form and 'adminPassword' in request.form:
        # Create variables for easy access
        adminUsername = request.form['adminUsername']
        adminPassword = request.form['adminPassword']
        # Check if account exists using MySQL
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE adminUsername = %s AND adminPassword = %s', (adminUsername, adminPassword,))
        # Fetch one record and return result
        admin = cursor.fetchone()
        # If account exists in accounts table in out database
        if admin:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['adminID'] = admin['adminID']
            session['adminUsername'] = admin['adminUsername']
            # Redirect to home page
            return redirect(url_for('admin_home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect adminUsername/adminPassword!'
    # Show the login form with message (if any)
    return render_template('loginadmin.html', msg=msg)


@app.route('/admin_home')
def admin_home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('homepageAdmin.html', adminUsername=session['adminUsername'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login_admin'))


@app.route('/profile_admin')
def profile_admin():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE adminID = %s', (session['adminID'],))
        profile = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profileAdmin.html', profile=profile)
    # User is not loggedin redirect to login page
    return redirect(url_for('login_admin'))


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout_admin')
def logout_admin():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('adminID', None)
    session.pop('adminUsername', None)
    # Redirect to login page
    return redirect(url_for('login_admin'))


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


def getAvailableIngredient():
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("""
            SELECT * FROM ingredients
        """)

    available_ingredients = cursor.fetchall()
    return available_ingredients


def filterRecipe(available_ingredients, products):
    filtered_products = []
    for product in products:
        ingredients_required = product['ingredients_required']
        available_ingredient_names = [ingredient['ingredient_name'] for ingredient in available_ingredients]
        required_ingredient_names = [ingredient['ingredient_name'] for ingredient in ingredients_required]
        if all(ingredient_name in available_ingredient_names for ingredient_name in required_ingredient_names):
            for ingredient in ingredients_required:
                for available_ingredient in available_ingredients:
                    if (
                            ingredient['ingredient_name'] == available_ingredient['ingredient_name']
                            and ingredient['quantity'] <= available_ingredient['available_quantity']
                    ):
                        filtered_products.append(product)
                        break
                else:
                    break
    return filtered_products


def requiredingredients(product):
    ingredient = {
        'ingredient_id': product['ingredient_id'],
        'quantity': product['quantity'],
        'unit': product['unit'],
        'ingredient_name': product['ingredient_name']
    }
    return ingredient


@app.route('/recommend')
def recommend():
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

    try:
        # Execute the SQL query
        cursor.execute("""
            SELECT p.productID, p.productName, p.productSize, i.ingredient_id, r.quantity, i.unit, i.ingredient_name
            FROM product p
            JOIN recipes r ON p.productID = r.productID
            JOIN ingredients i ON r.ingredient_id = i.ingredient_id
        """)

        # Fetch all the rows
        fetch_products = cursor.fetchall()
        available_ingredients = getAvailableIngredient()
        #required_ingredients =requiredingredients(product)
        products = {}
        for product in fetch_products:
            product_id = product['productID']
            if product_id not in products:
                products[product_id] = {
                    'productID': product['productID'],
                    'productName': product['productName'],
                    'productSize': product['productSize'],
                    'ingredients_required': []
                }
            ingredient = requiredingredients(product)
            products[product_id]['ingredients_required'].append(ingredient)
        formatted_products = list(products.values())
        recommend_product = delete_duplicates(filterRecipe(available_ingredients, formatted_products))
        print('ready', recommend_product)
        return render_template('recommend.html', recommendations=recommend_product)

    except MySQLdb.Error as e:
        print(f"Error: {e}")

    finally:
        cursor.close()

    return "Error occurred. Please try again later."


def delete_duplicates(total_list):
    expected_list = []
    in_expected_list = False
    for i in total_list:
        # print(i)
        for j in expected_list:
            if j['productID'] == i['productID']:
                in_expected_list = True
        if not in_expected_list:
            expected_list.append(i)
        in_expected_list = False

    return expected_list


@app.route('/view_ingredients')
def view_ingredients():
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

    try:
        # Execute the SQL query
        cursor.execute("""
           SELECT * 
           FROM ingredients;
        """)

        # Fetch all the rows
        ingredients = cursor.fetchall()

        return render_template('viewIngredients.html', ingredients=ingredients)

    except MySQLdb.Error as e:
        print(f"Error: {e}")

    finally:
        cursor.close()

    return "Error occurred. Please try again later."


@app.route('/add')
def add():
    return render_template("insertIngredients.html")


@app.route('/insert_ingredients', methods=['GET', 'POST'])
def insert_ingredients():
    if request.method == "POST":
        if "ingredient_name" in request.form and "available_quantity" in request.form and "unit" in request.form:
            ingredient_name = request.form['ingredient_name']
            available_quantity = request.form['available_quantity']
            unit = request.form['unit']

            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO login.ingredients(ingredient_name,available_quantity,unit)"
                        "VALUES(%s,%s,%s)", (ingredient_name, available_quantity, unit))
            db.connection.commit()
            msg = 'You have successfully insert!'

    return render_template("insertIngredients.html")


@app.route('/update_ingredients/<int:ingredient_id>', methods=['GET', 'POST'])
def update_ingredients(ingredient_id):
    if'loggedin' in session:
        if "available_quantity" in request.form:

            available_quantity = request.form['available_quantity']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            print(ingredient_id)

            query = "UPDATE ingredients SET available_quantity = %s WHERE ingredient_id = %s"
            values = (request.form['available_quantity'], ingredient_id,)
            cursor.execute(query, values)
            db.connection.commit()
            print(cursor.rowcount, "record(s) affected")
            msg = 'You have successfully updated !'
        return redirect(url_for('view_ingredients'))
    return redirect(url_for('update_in', ingredient_id=ingredient_id))


@app.route('/update_in/<int:ingredient_id>')
def update_in(ingredient_id):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    print(ingredient_id)
    sql = "SELECT * FROM ingredients WHERE ingredient_id = %s"
    params = (ingredient_id, )
    cursor.execute(sql, params)
    ingredient = cursor.fetchone()
    print('ingredient', ingredient)
    return render_template("updateIngredients.html", ingredient=ingredient)


@app.route('/create_pro')
def create_pro():
    return render_template('createProduct.html')


@app.route('/create_product', methods=['GET', 'POST'])
def create_product():
    if request.method == "POST":
        if "productName" in request.form and "productDesc" in request.form and "productPrice" in request.form and \
                "productSize" in request.form:
            productName = request.form['productName']
            productDesc = request.form['productDesc']
            productPrice = request.form['productPrice']
            productSize = request.form['productSize']

            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO login.product(productName,productDesc,productPrice, productSize)""VALUES(%s,%s,%s,%s)", (productName, productDesc, productPrice, productSize,))
            db.connection.commit()
            msg = 'Successfully create product!'
        # Show registration form with message (if any)
    return render_template("createProduct.html")


@app.route('/view_order')
def view_order():
    return render_template('viewOrder.html')


@app.route('/index_product')
def index_product():
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

    try:
        # Execute the SQL query
        cursor.execute("""
              SELECT * 
              FROM product;
           """)

        # Fetch all the rows
        product = cursor.fetchall()

        return render_template('indexProduct.html', product=product)

    except MySQLdb.Error as e:
        print(f"Error: {e}")

    finally:
        cursor.close()

    return "Error occurred. Please try again later."


@app.route('/update_product/<int:productID>', methods=['GET', 'POST'])
def update_product(productID):
    if 'loggedin' in session:
        if "productName" in request.form and "productDesc" in request.form and "productPrice" in request.form and "productSize" in request.form:
            productName = request.form['productName']
            productDesc = request.form['productDesc']
            productPrice = request.form['productPrice']
            productSize = request.form['productSize']

            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            print(productID)

            query = "UPDATE product SET productName = %s, productDesc = %s, productPrice = %s, productSize = %s WHERE productID = %s"
            values = (productName, productDesc, productPrice, productSize, productID)

            cursor.execute(query, values)
            db.connection.commit()
            print(cursor.rowcount, "record(s) affected")

            msg = 'You have successfully updated!'
            return redirect(url_for('index_product'))

    return redirect(url_for('update_pro', productID=productID))


@app.route('/update_pro/<int:productID>', methods=['GET', 'POST'])
def update_pro(productID):
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    print(productID)
    sql = "SELECT * FROM product WHERE productID = %s"
    params = (productID,)
    cursor.execute(sql, params)
    product = cursor.fetchone()
    print('product', product)
    return render_template("updateProduct.html", product=product)


@app.route('/delete_product/<int:productID>', methods=['GET', 'POST'])
def delete_product(productID):
    if 'loggedin' in session:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

        # SQL query to delete the selected product by productID
        delete_query = "DELETE FROM product WHERE productID = %s"
        cursor.execute(delete_query, (productID,))

        # Commit the changes and close the connection
        db.connection.commit()
        cursor.close()

        msg = 'Product successfully deleted!'
        return redirect(url_for('index_product'))

        # If not logged in, redirect to the login page or display an error message
    return redirect(url_for('login'))


@app.route('/single_page/<int:productID>')
def single_page(productID):
    # Connect to MySQL
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

    # Execute SQL query to get the product details
    query = "SELECT * FROM product WHERE productID = %s"
    cursor.execute(query, (productID,))
    product = cursor.fetchone()

    # Close the connection
    db.connection.commit()
    cursor.close()

    if not product:
        # Return 404 if product not found
        return render_template('404.html'), 404

    return render_template('singlepages.html', product=product)


@app.route('/addcart', methods=['POST'])
def addcart():
    try:
        productID = request.form.get('productID')
        productStock = request.form.get('productStock')
        product = create_product.query.filter_by(productID=productID).first()

        if productID and productStock and request.method == "POST":
            DictItems = {productID: {'productName': product.productName, 'productDesc': product.productDesc, 'productPrice': product.productPrice, 'productSize': product.producSize, 'productStock': product.productStock}}

            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session:
        return redirect('single_page')
    subtotal = 0
    for key, product in session['Shoppingcart'].items():
        subtotal += (product['productPrice']) * int(product['productStock'])
    return render_template('carts.html')


@app.route('/create_order')
@login_required  # Requires the user to be logged in to access this route
def create_order():
    try:
        custID = current_user.id
        if 'Shoppingcart' in session:
            orderID = secrets.token_hex(5)
            # Save each cart item as a separate order record
            for productID, cart_item in session['Shoppingcart'].items():
                order = orders(custID=custID, orderID=orderID, orders=session)
                db.connection.add(order)

                db.connection.commit()
                session.pop('Shoppingcart')
                flash('Your order has been sent successfully', 'success')
                return redirect(url_for('homepage'))
            else:
                flash('Your cart is empty', 'info')
                return redirect(url_for('getCart'))

    except Exception as e:
            print(e)
            flash('Something went wrong', 'danger')
            return redirect(url_for('getCart'))


@app.route('/orders/<int:orderID>')
def orders(orderID):
    if current_user.is_authenticated:
        totalOrder = 0
        custID = current_user.custID
        customer = register.query.filter_by(custID=custID).first()
        orders = orders.query.filter_by(custID=custID).first()
        for _key, product in orders.order.items():
           totalOrder = (product['productPrice']) * (product['productStock'])
    else:
        return redirect(url_for('login'))
    return render_template('login.html', orderID=orderID, totalOrder=totalOrder)


@app.route('/create_sales')
def create_sales():
    return render_template('createRecordSales.html')


@app.route('/recommendation')
def recommendation():
    return render_template('recommendation.html')


@app.route('/delete')
def delete():
    return render_template('delete.html')


if __name__ == '__main__':
    app.run(debug=True)
