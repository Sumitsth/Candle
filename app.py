from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    product = db.Column(db.String(100), nullable=False)
    fragrance = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(100), nullable=True)
    dispatched = db.Column(db.Boolean, default=False)

# Create the database and tables if they do not exist
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    orders = Order.query.all()
    return render_template('index.html', orders=orders)

@app.route('/add_order', methods=['POST'])
def add_order():
    name = request.form['name']
    product = request.form['product']
    fragrance = request.form['fragrance']
    quantity = int(request.form['quantity'])
    date = request.form['date']

    # Create a new order
    new_order = Order(name=name, product=product, fragrance=fragrance, quantity=quantity, date=date)
    db.session.add(new_order)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/dispatch_order/<int:id>', methods=['GET'])
def dispatch_order(id):
    order = Order.query.get(id)
    if order:
        order.dispatched = True
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
