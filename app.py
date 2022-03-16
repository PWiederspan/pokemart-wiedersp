from flask import Flask, render_template, redirect, flash
from flask_mysqldb import MySQL
from flask import request
import datetime

# Configuration
app = Flask(__name__)

# database connection - from template
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_wiedersp"
app.config["MYSQL_PASSWORD"] = "9567"
app.config["MYSQL_DB"] = "cs340_wiedersp"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


# Homepage
@app.route('/index.html')
@app.route('/')
def root():
    return render_template("/index.j2")

#--------------------------------------------------------------

# CUSTOMER ROUTES

#--------------------------------------------------------------
# Customers Page
@app.route('/customers.html', methods=["POST", "GET"])
def customers():
    """ 
    Read, and Create functionality for Customers page.
    """
    def get_customer_id():
        #print("Getting Customer ID's")
        query = "SELECT Customer_id FROM Customers ORDER BY Customer_id DESC LIMIT 1"
        cur = mysql.connection.cursor()
        cur.execute(query) 
        data = cur.fetchall()
        return data
    # Add a Customer to the database 
    if request.method == "POST":                    
        if request.form.get("insert_customer_submit"):
            Name = request.form["Name"]
            Phone_number = request.form["Phone_number"]
            Badges = request.form["Badges"]
            Gender = request.form["Gender"]

            # Insert new values into Customer Table
            query1 = "INSERT INTO Customers (Name, Phone_number, Badges, Gender) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query1, (Name, Phone_number, Badges, Gender))
            mysql.connection.commit()

            # Insert new values into Customer_Trades Table
            value = get_customer_id()
            Customer_id_trade = value[0]["Customer_id"]
            print("Customer ID: " + str(Customer_id_trade))

            # Insert new values into Customer_Trades Table
            query2 = "INSERT INTO Customer_Trades (Customer_id_trade, Trade_id_trade) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            Trade_id_trade = None
            cur.execute(query2, (Customer_id_trade, Trade_id_trade))
            mysql.connection.commit()

            # redirect back to customer page
            return redirect("/customers.html")

    # Get Customer data from Customer Table
    if request.method == "GET":
        # Query to populate table
        query_table = "SELECT * FROM Customers"
        cur = mysql.connection.cursor()
        cur.execute(query_table)
        customer_table = cur.fetchall()

        # Render the Customers page with the fetched data
        return render_template("customers.j2", customer_data = customer_table)

# Update existing Customer Data
@app.route('/customers_update.html', methods=["GET","POST"])
def update_customers():
    if request.method == "POST":                    
        if request.form.get("update_customer_submit"):
            Customer_id = request.form["Customer_id"]
            Name = request.form["Name"]
            Phone_number = request.form["Phone_number"]
            Badges = request.form["Badges"]
            Gender = request.form["Gender"]

            # Insert new values into Customer Table
            query2 = "UPDATE Customers SET Name=%s, Phone_number=%s, Badges=%s, Gender=%s WHERE Customer_id=%s"
            cur = mysql.connection.cursor()
            cur.execute(query2, (Name, Phone_number, Badges, Gender, Customer_id))
            mysql.connection.commit()

            # redirect back to customer page
            return redirect("/customers.html")

    if request.method == "GET":
        query = "SELECT Customer_id FROM Customers"
        cur = mysql.connection.cursor()
        cur.execute(query) 
        idList = cur.fetchall() 
        print(idList)
        return render_template("customers_update.j2", idList=idList)


# Customer Details
@app.route('/details.html/<int:id>', methods=["POST", "GET"])
def details(id):
    """ 
    Read, and Create functionality for more details on Customer Trades and Orders
    """
    # Add a Customer to the database 
    if request.method == "POST":                  
        if request.form.get("details_customer_submit"):
            Name = request.form["Name"]
            Phone_number = request.form["Phone_number"]
            Badges = request.form["Badges"]
            Gender = request.form["Gender"]

            # Insert new values into Customer Table
            query1 = "INSERT INTO Customers (Name, Phone_number, Badges, Gender) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query1, (Name, Phone_number, Badges, Gender))
            mysql.connection.commit()

            # redirect back to customer page
            return redirect("/customers.html")

    # Get Customer data from Customer Table
    if request.method == "GET":
        # Query to populate table
        query_table = """SELECT Customers.Name, Trades.Receiver, Trades.Trade_id,Orders.Order_id FROM Customers
                        INNER JOIN Customer_Trades on Customer_Trades.Customer_id_trade=Customers.Customer_id
                        INNER JOIN Trades on Customer_Trades.Customer_id_trade= Trades.Sender
                        INNER JOIN Orders on Orders.Customer_id=Trades.Sender
                        WHERE Customers.Customer_id = %s"""
        cur = mysql.connection.cursor()
        print("Getting query Table")
        cur.execute(query_table,(id,))
        details_table = cur.fetchall()
        print(details_table)

        # Render the Customers page with the fetched data
        return render_template("/details.j2", details_data = details_table)

@app.route('/customer_search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        customer = request.form['customer']
        # search by name or id
        cur.execute("SELECT * FROM Customers WHERE Name LIKE %s OR Customer_id LIKE %s", (customer, customer))
        mysql.connection.commit()
        data = cur.fetchall()
        # all in the search box will return all the tuples
        if len(data) == 0 and customer == 'all': 
            cur.execute("SELECT * from Customers")
            mysql.connection.commit()
            data = cur.fetchall()
        return render_template('customer_search.j2', data=data)
    return render_template('customer_search.j2')

# Delete customer based on ID
@app.route('/delete-customer/<int:id>')
def delete_customer(id):
    cur = mysql.connection.cursor()
    query = "DELETE FROM Customers WHERE Customer_id =%s"
    cur.execute(query, (id,))
    mysql.connection.commit()
    flash("User deleted successfully")
    return redirect("/customers.html")

#--------------------------------------------------------------

# ITEMS ROUTES

#--------------------------------------------------------------

# Items table
@app.route('/items.html', methods=["POST", "GET"])
def items():
    """ 
    Read, and Create functionality for Customers page.
    """
    # Add an Item to the database 
    if request.method == "POST":                    
        if request.form.get("insert_item_submit"):
            Price = request.form["Price"]
            Description = request.form["Description"]
            Badge_required = request.form["Badge_required"]

            # Insert new values into Items Table
            query = "INSERT INTO Items (Price, Description, Badge_required) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (Price, Description, Badge_required))
            mysql.connection.commit()

            # redirect back to items page
            return redirect("/items.html")

    # Get Item data from Items Table
    if request.method == "GET":
        # Query to populate table
        query_table = "SELECT * FROM Items"
        cur = mysql.connection.cursor()
        cur.execute(query_table)
        item_table = cur.fetchall()

        # Render the items page with the fetched data
        return render_template("items.j2", item_data=item_table)

# Update existing Item data
@app.route('/items_update.html', methods=["GET","POST"])
def update_items():
    if request.method == "POST":                    
        if request.form.get("update_item_submit"):
            Item_id = request.form["Item_id"]
            Price = request.form["Price"]
            Description = request.form["Description"]
            Badge_required = request.form["Badge_required"]

            # Insert new values into Customer Table
            query2 = "UPDATE Items SET Price=%s, Description=%s, Badge_required=%s WHERE Item_id=%s"
            cur = mysql.connection.cursor()
            cur.execute(query2, (Price, Description, Badge_required, Item_id))
            mysql.connection.commit()

            # redirect back to customer page
            return redirect("/items.html")

    if request.method == "GET":
        query = "SELECT Item_id FROM Items"
        cur = mysql.connection.cursor()
        cur.execute(query) 
        idList = cur.fetchall() 
        print(idList)
        return render_template("items_update.j2", idList=idList)


# Delete item based on ID
@app.route('/delete-item/<int:id>')
def delete_item(id):
    cur = mysql.connection.cursor()
    query = "DELETE FROM Items WHERE Item_id =%s"
    cur.execute(query, (id,))
    mysql.connection.commit()
    flash("Item deleted successfully")
    return redirect("/items.html")

#--------------------------------------------------------------

# ORDERS ROUTES

#--------------------------------------------------------------    

# Orders Page
@app.route('/orders.html', methods=["POST", "GET"])
def orders():
    """ 
    Read, and Create functionality for Orders page.
    """
    # Add a order to the database 
    if request.method == "POST":                    
        if request.form.get("insert_order_submit"):
            Customer_id = request.form["Customer_id"]
            Item_id = request.form["Item_id"]
            Quantity = request.form["Quantity"]
            Date = datetime.datetime.utcnow()
            Total = request.form["Total"]

            # Insert new values into Customer Table
            query = "INSERT INTO Orders (Customer_id, Item_id, Quantity, Date, Total) VALUES (%s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (Customer_id, Item_id, Quantity, Date, Total))
            mysql.connection.commit()

            # redirect back to orders page
            return redirect("/orders.html")

    # Get Order data from Orders Table
    if request.method == "GET":
        # Query to populate table
        query_table = "SELECT * FROM Orders"
        cur = mysql.connection.cursor()
        cur.execute(query_table)
        order_table = cur.fetchall()

        # Render the Order page with the fetched data
        return render_template("orders.j2", order_data=order_table)

#--------------------------------------------------------------

# TRADES ROUTES

#--------------------------------------------------------------

# Trades Page
@app.route('/trades.html', methods=["POST", "GET"])
def trades():
    """ 
    Read, and Create functionality for Trades page.
    """
    def get_trade_id():
        #print("Getting Customer ID's")
        query = "SELECT Trade_id FROM Trades ORDER BY Trade_id DESC LIMIT 1"
        cur = mysql.connection.cursor()
        cur.execute(query) 
        data = cur.fetchall()
        return data
    # Add a order to the database 
    if request.method == "POST":                    
        if request.form.get("insert_trade_submit"):
            Sender = request.form["Sender"]
            Receiver = request.form["Receiver"]

            # Insert new values into Customer Table
            query = "INSERT INTO Trades (Sender, Receiver) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (Sender, Receiver))
            mysql.connection.commit()

            value = get_trade_id()
            Trade_id_trade = value[0]["Trade_id"]
            # Insert new values into Customer Table
            query = "UPDATE Customer_Trades SET Trade_id_trade=%s Where Customer_id_trade=%s"
            cur = mysql.connection.cursor()
            cur.execute(query, (Trade_id_trade, Sender))
            mysql.connection.commit()
            
            # redirect back to trades page
            return redirect("/trades.html")

    # Get Order data from Trades Table
    if request.method == "GET":
        # Query to populate table
        query_table = "SELECT * FROM Trades"
        cur = mysql.connection.cursor()
        cur.execute(query_table)
        trade_table = cur.fetchall()

        # Render the Order page with the fetched data
        return render_template("trades.j2", trade_data=trade_table)
    

# Customers Trades Page
@app.route('/customer_trades.html', methods=["POST", "GET"])
def customer_trades():
    """ 
    Read, and Create functionality for Customer_trades page.
    """
    # Add a customer trade to the database 
    if request.method == "POST":                    
        if request.form.get("insert_customer_trade_submit"):
            Customer_id_trade = request.form["Customer_id_trade"]
            Trade_id_trade = request.form["Trade_id_trade"]

            # Insert new values into Customer Table
            query = "INSERT INTO Customer_Trades (Customer_id_trade, Trade_id_trade) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (Customer_id_trade, Trade_id_trade))
            mysql.connection.commit()

            # redirect back to trades page
            return redirect("/customer_trades.html")

    # Get Order data from Trades Table
    if request.method == "GET":
        # Query to populate table
        query_table = "SELECT * FROM Customer_Trades"
        cur = mysql.connection.cursor()
        cur.execute(query_table)
        customer_trade_table = cur.fetchall()

        # Render the Order page with the fetched data
        return render_template("customer_trades.j2", customer_trade_data=customer_trade_table)

app.secret_key = 'This is a secret'

# Listener
if __name__ == "__main__":
    app.run(host="flip2.engr.oregonstate.edu", debug=True)
    app.run(port=62423, debug=True)