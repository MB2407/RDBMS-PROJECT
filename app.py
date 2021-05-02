import os
from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy

# Specifying the location of the SQLITE3 database ---------------------------------------------------------------------------------------
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "RDBMS_PROJECT_CSE.db"))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jbcsjbvak7njdfnjisn8nwfdnk'
app.config['SQLALCHEMY_DATABASE_URI'] = database_file

db = SQLAlchemy(app)

# DATABASE TABLES ------------------------------------------------------------------------------------------------------------------------
class Inventory(db.Model):
    __tablename__ = 'inventory'
    item_id = db.Column(db.Integer, nullable=False,primary_key=True)
    item_name = db.Column(db.String, nullable=False)
    item_price = db.Column(db.Float, nullable=False)
    item_capacity = db.Column(db.Integer)
    clients = db.relationship('Client', backref='inventory')
    items_sold = db.relationship('Sold', backref='inventory')

class Client(db.Model):
    __tablename__ = 'client'
    client_id = db.Column(db.Integer, nullable=False, primary_key=True)
    client_name = db.Column(db.String(40), nullable=False)
    client_age = db.Column(db.Integer)
    client_dob = db.Column(db.String(14), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory.item_id'), nullable=False)

class Sold(db.Model):
    __tablename__ = 'sold'
    sold_id = db.Column(db.Integer, nullable=False, primary_key=True)
    sold_date = db.Column(db.String(14), nullable=False)
    sold_capacity = db.Column(db.Integer, nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory.item_id'), nullable=False) 
    
# Routes ---------------------------------------------------------------------------------------------------------------------------------

# HOMEPAGE
@app.route('/')
def home():
    return render_template('home.html')

# DISPLAYING THE CLIENT DATABASE 
@app.route("/client", methods=['GET','POST'])
def displayClients():
    c = Client.query.all()
    return render_template("client.html", clients=c)

# DISPLAYING THE INVENTORY DATABASE
@app.route("/inventory", methods=['GET','POST'])
def displayInventory():
    items = Inventory.query.all()
    return render_template("inventory.html", items=items) 

# # INSERT INTO INVENTORY TABLE
# @app.route("/insertInventory", methods=['POST'])
# def insert():
#     item = Inventory(item_id = request.form['id'], item_name=request.form['name'], item_price = request.form['price'], item_capacity = request.form['capacity'])
#     db.session.add(item)
#     db.session.commit()
#     return redirect("/")
    
# # UPDATE INTO INVENTORY TABLE
# @app.route("/updateInventory", methods=['POST'])
# def update():
#     oldItemId, oldItemName, oldItemPrice, oldItemCapacity = request.form.get("oldItemId"), request.form.get("oldItemName"), request.form.get("oldItemPrice"), request.form.get("oldItemCapacity") 
#     newItemId, newItemName, newItemPrice, newItemCapacity = request.form.get("newItemId"), request.form.get("newItemName"), request.form.get("newItemPrice"), request.form.get("newItemCapacity")
#     i = Inventory.query.filter_by(item_id=oldItemId).first()
#     i.item_name, i.item_id, i.item_price, i.item_capacity = newItemName, newItemId, newItemPrice, newItemCapacity
#     db.session.commit()
#     return redirect("/")

# # DELETE FROM INVENTORY TABLE
# @app.route("/deleteInventory", methods=['POST'])
# def delete():
#     item_id = request.form.get('id')
#     i = Inventory.query.filter_by(item_id=item_id).first()
#     db.session.delete(i)
#     db.session.commit()
#     return redirect("/")

# INSERT INTO CLIENT DATABASE
@app.route('/insertClient', methods=['POST'])
def insertClient():
    client = Client(client_id = request.form['client_id'], client_name=request.form['client_name'], client_age=request.form['client_age'], client_dob=request.form['client_dob'], items_id=request.form['item_id'])
    db.session.add(client)
    db.session.commit()
    return redirect('/client')

# UPDATE INTO CLIENT DATABASE
@app.route('/updateClient', methods=['POST'])
def updateClient():
    oldclientId, oldClientName, oldClientAge, oldClientDob, oldClientItemId = request.form.get("oldClientId"), request.form.get("oldClientName"), request.form.get("oldClientAge"), request.form.get("oldClientDob"), request.form.get("oldClientItemId")
    newClientId, newClientName, newClientAge, newClientDob, newClientItemId = request.form.get("newClientId"), request.form.get("newClientName"), request.form.get("newClientAge"), request.form.get("newClientDob"), request.form.get("newClientItemId")
    c = Client.query.filter_by(client_name=oldclientName).first()
    c.client_id, c.client_name, c.client_age, c.client_dob, c.item_id = newClientId, newClientName, newClientAge, newClientDob, newClientItemId
    db.session.commit()
    return redirect('/client')

# DELETE FROM CLIENT DATABASE
@app.route('/deleteClient', methods=['POST'])
def deleteClient():
    name = request.form.get("client_name")
    c = Client.query.filter_by(client_name=name).first()
    db.session.delete(c)
    db.session.commit()
    return redirect("/client")

@app.route("/sold", methods=['GET'])
def sold():
    sold_items = Sold.query.all()
    return render_template("shop.html", sold = sold_items)

@app.route("/insertSold", methods=['POST', 'GET'])
def insertSold():
    sold = Sold(sold_id = request.form['sold_id'], sold_date = request.form['sold_date'], sold_capacity= request.form['sold_capacity'], item_id = request.form['item_id']) 
    db.session.add(sold)
    db.session.commit()
    capacity = sold.sold_capacity
    item_id = sold.item_id
    i = Inventory.query.filter_by(item_id = item_id).first()
    i.item_capacity -= capacity
    return redirect('/sold')

if __name__ == '__main__':
    app.run(debug=True, port=3000, host="0.0.0.0")

