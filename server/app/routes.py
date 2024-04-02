from flask import render_template, jsonify, request, redirect, url_for
from flasgger import swag_from

from . import app
from .models import User, Product, Listing
from . import db
from . import login_manager, login_user, logout_user, login_required, current_user

# TODO: Home page ideas?
@app.route('/')
def home():
    return "Hello there!"

# <---------------------------------------------Product Routes----------------------------------------------------->
# TODO: add login_required wherever needed

@app.route('/product/create')
# @login_required
def create_product():
    user_id = current_user.get_id()
    return render_template('add_product.html')


@app.route('/product/create/addToDb', methods=['POST'])
# @login_required
def add_product_to_db():
    user_id = current_user.get_id()
    data = request.form.to_dict()

    # Adding the form data to the db
    product = Product(prod_title=data['prod_title'],
                    description=data['description'],
                    prod_condition=data['prod_condition'],
                    listed_price=data['listed_price'],
                    quantity=data['quantity']
                    )
    product.save()
    return "Product added successfully", 201


@app.route('/product', methods=['GET'])
def get_products():
    # Retriving the page number from the query string
    page = request.args.get('page', 1, type=int)
    per_page = 4
    
    # per_page is the max number of products to be shown
    # If there are more products, the has_next attribute will be True
    # IF there are fewer products, the has_next attribute will be False
    products = Product.query.paginate(page=page, per_page=per_page)
    products_json = [product.to_dict() for product in products.items]

    return jsonify({
        'products': products_json,
        'has_next': products.has_next  # To Indicate if there are more pages
    })


@app.route('/product/<int:id>')
def product(id, methods=['GET', 'PUT', 'DELETE']):
    if request.method == 'GET':
        required_prod = Product.query.filter_by(prod_id=id).first().to_dict()

        # If the product is not found, return a 404 error
        if required_prod == None:
            return 'Product not found', 404
        return jsonify(required_prod)
    elif request.method == 'DELETE':
        product = Product.query.get(id)
        if product is None:
            return jsonify({'message': 'Product not found'}), 404
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted'})
    elif request.method == 'PUT':
        product = Product.query.get(id)
        if product is None:
            return jsonify({'message': 'Product not found'}), 404
        data = request.get_json()
        for key, value in data.items():
            setattr(product, key, value)
        db.session.commit()
        return jsonify(product.__dict__)
    

# <---------------------------------------------User Routes----------------------------------------------------->
# TODO

@app.route('/user/<int:u_id>', methods=['GET'])
@swag_from('docs/get_user.yml')
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