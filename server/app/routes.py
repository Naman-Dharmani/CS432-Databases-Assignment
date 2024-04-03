from flask import render_template, jsonify, request, redirect, url_for, make_response
from flasgger import swag_from
from datetime import datetime, timedelta, timezone

from . import app
from .models import User, Product, Listing, Category, Subcategory, Hashtag, Product_Image, App_Feedback
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
# TODO: While using PUT method for product, update the date_modified field as well
# TODO: Update the corresponding tables that are connected to the product table
#   --> Category, Subcategory, Hashtag DONE
# TODO: DELETE method - need to enable cascading for delete in models.py


# Route to get all products with pagination
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


# Route to add a new product
@app.route('/product', methods=['POST'])
# @login_required
def create_product():
    try:
        data = request.json

        # Sanity check for the data
        keys = ['prod_title', 'description', 'prod_condition',
                'listed_price', 'quantity', 'category_name', 'subcategory_name']
        if not all(key in data for key in keys):
            return make_response(jsonify({'error': 'Data is missing some keys'}), 400)

        # Adding the form data to the db
        product = Product(prod_title=data['prod_title'],
                          description=data['description'],
                          prod_condition=data['prod_condition'],
                          listed_price=data['listed_price'],
                          quantity=data['quantity']
                          )
        db.session.add(product)
        db.session.commit()

        # Need the prod_id inorder to add the category
        # SQLAlchmey automatically updates the product instance after commit
        product_id = product.prod_id
        category = Category(category_name=data['category_name'],
                            prod_id=product_id
                            )
        db.session.add(category)
        db.session.commit()

        # Need the category_id inorder to add the subcategory
        category_id = category.category_id
        sub_category = Subcategory(subcategory_name=data['subcategory_name'],
                                   category_id=category_id
                                   )
        db.session.add(sub_category)
        db.session.commit()

        if 'hashtag' in data:
            # Multiple hashtags can be added
            for tag in data['hashtag'].split(','):
                tag = tag.strip()
                hashtag = Hashtag(tag_label=tag,
                                  product_id=product_id
                                  )
                db.session.add(hashtag)
                db.session.commit()

        # TODO: uncomment this once login is required
        # user_id = current_user.get_id()
        # listing = Listing(user_id=user_id,
        #                   prod_id=product_id
        #                   )
        # db.session.add(listing)
        # db.session.commit()

        product_image = Product_Image(image_url=data['image_url'],
                                      prod_id=product_id,
                                      # Describes what the image is about
                                      image_caption=data['image_caption']
                                      )
        db.session.add(product_image)
        db.session.commit()

        return make_response(jsonify({"message": "Product added successfully"}), 201)

    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


# Route to get/update/delete a product by id
@app.route('/product/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def product(id):
    if request.method == 'GET':
        try:
            required_prod = Product.query.filter_by(
                prod_id=id).first().to_dict()

            # If the product is not found, return a 404 error
            if required_prod == None:
                return make_response({"message": 'Product not found'}, 404)

            # If product is found, get the other details
            category = Category.query.filter_by(prod_id=id).first().to_dict()
            subcategory = Subcategory.query.filter_by(category_id=category['category_id']).first().to_dict()
            hashtags = [hashtag.to_dict()['tag_label'] for hashtag in Hashtag.query.filter_by(product_id=id).all()]
            product_image = Product_Image.query.filter_by(prod_id=id).first().to_dict()

            hashtags = dict(tag_label=hashtags)
                
            required_data= {**required_prod, **category, **subcategory, **hashtags, **product_image}
            # print(required_data)
            return make_response(jsonify(required_data), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

    elif request.method == 'PUT':
        try:
            product = Product.query.get(id)
            if product is None:
                return make_response(jsonify({'message': 'Product not found'}), 404)
            data = request.get_json()

            # Separating data for each table
            product_data = {key: value for key, value in data.items(
                            ) if key in Product.__table__.columns}
            category_data = {key: value for key, value in data.items(
                            ) if key in Category.__table__.columns}
            subcategory_data = {key: value for key, value in data.items(
                            ) if key in Subcategory.__table__.columns}
            hashtag_data = {key: value for key, value in data.items(
                            ) if key in Hashtag.__table__.columns}
            product_image_data = {key: value for key, value in data.items(
                            ) if key in Product_Image.__table__.columns}

            # Updating the product attributes
            for key, value in product_data.items():
                setattr(product, key, value)

            # ist = timezone(timedelta(hours=5, minutes=30))  # IST (UTC+5:30)
            utc = timezone(timedelta(hours=0, minutes=0))
            product.date_modified = datetime.now(
                utc).strftime('%Y-%m-%d %H:%M:%S')

            # Updating the category attributes
            category = Category.query.filter_by(prod_id=id).first()
            if category:
                for key, value in category_data.items():
                    setattr(category, key, value)

            # Updating the subcategory attributes
            subcategory = Subcategory.query.filter_by(
                category_id=category.category_id).first()
            if subcategory:
                for key, value in subcategory_data.items():
                    setattr(subcategory, key, value)

            # Updating the hashtags
            Hashtag.query.filter_by(product_id=id).delete()
            for key, value in hashtag_data.items():
                for tag in value.split(','):
                    tag = tag.strip()
                    hashtag = Hashtag(tag_label=tag,
                                      product_id=id
                                      )
                    db.session.add(hashtag)

            # Updating the product image
            product_image = Product_Image.query.filter_by(prod_id=id).first()
            if product_image:
                for key, value in product_image_data.items():
                    setattr(product_image, key, value)

            # The ids are already known, therefore commiting at the end
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



# <---------------------------------------------App Feedback----------------------------------------------------->
@app.route('/app/feedback', methods=['POST'])
def app_feedback():
    try:
        # user_id = current_user.get_id()
        user_id = 2
        data = request.get_json()
        feedback = App_Feedback(user_id=user_id, 
                                feedback_rating=data['rating'],
                                feedback_text=data['feedback_text']
                                )
        db.session.add(feedback)
        db.session.commit()
        return make_response(jsonify({'message': 'Feedback submitted'}), 201)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)