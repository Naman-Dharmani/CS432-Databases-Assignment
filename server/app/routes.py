from flask import render_template, jsonify, request, redirect, url_for, make_response
from flasgger import swag_from

from . import app
from .models import User, Product, Listing
from . import db
from . import login_manager, login_user, logout_user, login_required, current_user


pagination_per_page = 4

# TODO: Home page ideas?


@app.route('/')
def home():
    """
    This is the home endpoint.
    ---
    responses:
      200:
        description: A successful response with "Hello, World!"
    """
    return "Hello there!"

# <---------------------------------------------Product Routes----------------------------------------------------->
# TODO: Add try catch error handling in all routes --> DONE
# TODO: add login_required wherever needed
# TODO: use make_response to return response with status code --> DONE
# TODO: check difference between .get() and .filter_by() in SQLAlchemy --> DONE
# get() - works only on PK and returns a record
# filter_by() - works on any column and returns a list of records.
# Also, multiple conditions can be specified


@app.route('/products', methods=['GET'])
def get_products():
    # Retriving the page number from the query string
    try:
        page = request.args.get('page', 1, type=int)

        # per_page is the max number of products to be shown
        # If there are more products, the has_next attribute will be True
        # IF there are fewer products, the has_next attribute will be False
        products = Product.query.paginate(
            page=page, per_page=pagination_per_page)
        products_json = [product.to_dict() for product in products.items]

        return make_response(
            jsonify({
                    'products': products_json,
                    'hasnext': products.has_next  # To Indicate if there are more pages
                    }), 200)

    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/product', methods=['POST'])
# @login_required
def create_product():
    try:
        user_id = current_user.get_id()
        data = request.json
        print(request.method)
        print(data)

        # Adding the form data to the db
        product = Product(prod_title=data['prod_title'],
                          description=data['description'],
                          prod_condition=data['prod_condition'],
                          listed_price=data['listed_price'],
                          quantity=data['quantity']
                          )
        product.save()
        return make_response(jsonify({"message": "Product added successfully"}), 201)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/product/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def product(id):
    if request.method == 'GET':
        try:
            required_prod = Product.query.filter_by(
                prod_id=id).first().to_dict()
            # If the product is not found, return a 404 error
            if required_prod == None:
                return make_response({"message": 'Product not found'}, 404)
            return make_response(jsonify(required_prod), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

    elif request.method == 'PUT':
        try:
            product = Product.query.get(id)
            print(product)
            if product is None:
                return make_response(jsonify({'message': 'Product not found'}), 404)
            data = request.get_json()
            for key, value in data.items():
                setattr(product, key, value)
            db.session.commit()
            return make_response(jsonify({'message': 'Product Updated'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

    elif request.method == 'DELETE':
        try:
            product = Product.query.get(id)
            if product is None:
                return make_response(jsonify({'message': 'Product not found'}), 404)
            db.session.delete(product)
            db.session.commit()
            return make_response(jsonify({'message': 'Product deleted'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)


# <---------------------------------------------User Routes----------------------------------------------------->
# TODO

@app.route('/user/<int:u_id>', methods=['GET'])
@swag_from('docs/get_user.yml')
def get_user(u_id):
    try:
        user = User.query.get(u_id)
        if user is None:
            return make_response(jsonify({'message': 'User not found'}), 404)
        return make_response(jsonify(user.to_dict()), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/user/<int:u_id>', methods=['PUT'])
def update_user(u_id):
    try:
        user = User.query.get(u_id)
        if user is None:
            return make_response(jsonify({'message': 'User not found'}), 404)
        data = request.get_json()
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return make_response(jsonify(user.to_dict()), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/user/<int:u_id>', methods=['DELETE'])
def delete_user(u_id):
    try:
        user = User.query.get(u_id)
        if user is None:
            return make_response(jsonify({'message': 'User not found'}), 404)
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({'message': 'User deleted'}))
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/user/<int:u_id>/listings', methods=['GET'])
def get_user_listings(u_id):
    try:
        listings = Listing.query.filter_by(user_id=u_id).all()
        return make_response(jsonify([listing.__dict__ for listing in listings]), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)