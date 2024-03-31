from flask import render_template, jsonify, request, session, redirect, url_for
from . import app
from .models import User, Listing
from . import db

# Dummy data structure to simulate a database
products = [
     {'prod_id': 1,
     'prod_title': 'macbook pro',
     'description': 'A laptop by Apple',
     'prod_condition': 'new',
     'listed_price': 100000,
     'quantity': 1,
     'date_listed': '2024-03-30',
     'date_modified': None,
     'flagging': 0
     },
     {'prod_id': 2,
     'prod_title': 'Nothing Phone 2a',
     'description': 'Nothing by Nothing',
     'prod_condition': 'new',
     'listed_price': 24000,
     'quantity': 1,
     'date_listed': '2024-03-30',
     'date_modified': None,
     'flagging': 0
     }
]

# TODO: Home page ideas?
@app.route('/')
def home():
    return "Hello there!"


# TODO: Add a login route that would store the user_id in the session
#that session would then be used to know which user has requested/added what product


@app.route('/product/create')
def create_product():
    return render_template('add_product.html')


@app.route('/product/create/addToDb', methods=['POST'])
def add_product_to_db():

    # TODO: Once, the login route is implemented, uncomment the code below
    # if 'user_id' in session:
    #     user_id = session['user_id']
        data = request.form.to_dict()

        # Adding the form data to the db
        products.append(data)
        print(products)

        return "Product added successfully", 201
    # else:
    #     return redirect(url_for('login'))


@app.route('/product/<int:id>')
def product(id, methods=['GET']):

    # TODO: Replace this with a database query
    required_prod = {}
    for prod in products:
        if prod['prod_id'] == id:
            required_prod = prod
            break

    # If the product is not found, return a 404 error
    if not required_prod:
        return 'Product not found', 404
    return jsonify(required_prod)


# USER ROUTES
# TODO

@app.route('/user/<int:u_id>', methods=['GET'])
def get_user(u_id):
    user = User.query.get(u_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user.to_dict())

@app.route('/user/<int:u_id>', methods=['PUT'])
def update_user(u_id):
    user = User.query.get(u_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify(user.__dict__)

@app.route('/user/<int:u_id>', methods=['DELETE'])
def delete_user(u_id):
    user = User.query.get(u_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

@app.route('/user/<int:u_id>/listings', methods=['GET'])
def get_user_listings(u_id):
    listings = Listing.query.filter_by(user_id=u_id).all()
    return jsonify([listing.__dict__ for listing in listings])