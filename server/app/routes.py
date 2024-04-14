from flask import redirect, request, make_response, jsonify, url_for, flash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flasgger import swag_from
from datetime import datetime, timedelta, timezone
import requests

from . import app
from .models import db
# from . import AdminView
from .models import (
    User,
    Product,
    Listing,
    Category,
    Subcategory,
    Hashtag,
    Product_Image,
    App_Feedback,
    Chat,
    ChatSystem,
    Review,
    Transaction,
    Listing,
)
from sqlalchemy import or_, and_, MetaData, select
from sqlalchemy.orm import joinedload
from flask_dance.contrib.google import google
from flask_login import login_required, logout_user
from sqlalchemy.sql import text

items_per_page = 5


@app.route('/admin_user')
@jwt_required()
def admin_user():
    stmt = text("SELECT * FROM admin_view_user")
    users = []
    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            print(row)
            row_dict = {}
            row_dict['id'] = row[0]
            row_dict['name'] = row[1]
            row_dict['email'] = row[2]
            users.append(row_dict)

    return make_response(jsonify(users), 200)


@app.route('/admin_prod')
def admin_prod():

    stmt = text("SELECT * FROM admin_view_prod")
    users = []
    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        for row in result:
            print(row)
            row_dict = {}
            row_dict['name'] = row[0]
            row_dict['email'] = row[1]
            row_dict['product'] = row[2]
            users.append(row_dict)

    return make_response(jsonify(users), 200)


@app.route("/")
def home():
    """
    This is the home endpoint.
    ---
    responses:
      200:
        description: A successful response with "Hello, World!"
    """
    # user details if logged in
    # try:
    try:
        is_google_authorized = google.authorized
    except Exception as e:
        is_google_authorized = False
    if is_google_authorized:
        user_info = google.get("/oauth2/v2/userinfo").json()
        user = User.query.filter_by(email=user_info["email"]).first()
        if user is None:
            return make_response(jsonify({"message": "User not found"}), 404)
        return make_response(jsonify(user_info), 200)
    # except Exception as e:
    return make_response(jsonify({"message": "Hello, World!"}), 200)
    # return


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


@app.route("/login")
def login():
    return redirect(url_for("google.login"))


@app.route("/logout")
@jwt_required()
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("home"))


@app.route("/auth/google", methods=['POST'])
def google_login():
    auth_code = request.get_json()['code']

    data = {
        'code': auth_code,
        'client_id': app.config["GOOGLE_OAUTH_CLIENT_ID"],
        'client_secret': app.config["GOOGLE_OAUTH_CLIENT_SECRET"],
        'redirect_uri': 'postmessage',
        'grant_type': 'authorization_code'
    }

    try:
        response = requests.post(
            'https://oauth2.googleapis.com/token', data=data).json()
        print(response)
        headers = {
            'Authorization': f'Bearer {response["access_token"]}'
        }
        user_info = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo', headers=headers).json()
        print(user_info)
    except Exception as e:
        return make_response(jsonify({"error": f"error in authenticating user, {e}"}), 500)

    """
        check here if user exists in database, if not, add him
    """
    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        return make_response(jsonify({"error": "User does not exist. Sign up"}), 404)

    user_info['user_id'] = user.user_id
    jwt_token = create_access_token(
        identity=user_info['email'])  # create jwt token
    user_info['jwt'] = jwt_token
    response = jsonify(user=user_info)
    # response.set_cookie('access_token_cookie',
    #                     value=jwt_token, secure=False, domain="app.localhost")

    return response, 200


def get_product(id):
    product = (
        Product.query.options(
            joinedload(Product.subcategory).joinedload(Subcategory.category),
            joinedload(Product.product_images),
            joinedload(Product.hashtags),
            joinedload(Product.listings).joinedload(Listing.user),
        )
        .filter_by(prod_id=id)
        .first()
    )

    if product is None:
        return make_response(jsonify({"message": "Product not found"}), 404)

    product_dict = product.to_dict()
    product_dict["subcategory"] = product.subcategory.to_dict()
    product_dict["category"] = product.subcategory.category.to_dict()
    product_dict["product_images"] = [
        image.to_dict() for image in product.product_images
    ]
    product_dict["hashtags"] = [
        hashtag.to_dict()["tag_label"] for hashtag in product.hashtags
    ]
    # seller: user_id, name
    listing = product.listings[0]
    name = User.query.filter_by(user_id=listing.user_id).first().name
    product_dict["seller"] = {"user_id": listing.user_id, "name": name}

    return product_dict


# Route to get all products with pagination
@app.route("/products", methods=["GET"])
@jwt_required()
def get_products():
    try:
        # Retriving the page number from the query string
        # page_num = request.args.get("page", 1, type=int) ## default behaviour, not needed
        # per_page is the max number of products to be shown
        # If there are more products, the has_next attribute will be True
        # IF there are fewer products, the has_next attribute will be False
        page = Product.query.order_by(Product.date_listed.desc()).paginate(
            per_page=items_per_page, error_out=False)
        products_json = [get_product(product.prod_id)
                         for product in page.items]
        if not products_json:
            return make_response(jsonify({'error': "not found"}), 404)
        # products_json = [product.to_dict() for product in page.items]

        return make_response(
            jsonify(
                {
                    "products": products_json,
                    "has_next": page.has_next,  # To Indicate if there are more pages
                    "has_prev": page.has_prev,  # To Indicate if there are previous pages
                    "total": page.total,
                    "page_num": page.page,
                    "per_page": page.per_page,
                }
            ),
            200,
        )

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


# Route to add a new product
@app.route("/product", methods=["POST"])
@jwt_required()
def create_product():
    try:
        current_user_email = get_jwt_identity()
        current_user = User.query.filter_by(email=current_user_email).first()

        if not current_user:
            return make_response(jsonify({"error": "User does not exist"}), 404)

        data = request.json
        db.session.begin_nested()

        # Sanity check for the data
        keys = [
            "prod_title",
            "description",
            "listed_price",
            "quantity",
            "subcategory_id",
            "status",
        ]
        if not all(key in data for key in keys):
            return make_response(jsonify({"error": "Data is missing some keys"}), 400)

        # import re
        # description = data['description'].copy()
        # hashtags = re.findall(r'\#\w+', description)
        # description_text = re.sub(r'\#\w+', '', description).strip()

        # Adding the form data to the db
        product = Product(
            prod_title=data["prod_title"],
            description=data["description"],
            # description=description_text,
            listed_price=data["listed_price"],
            quantity=data["quantity"],
            status=data["status"],
            # the drop down option should be converted to a number before sending
            subcategory_id=data["subcategory_id"],
        )
        db.session.add(product)
        db.session.commit()

        product_id = product.prod_id

        if "hashtags" in data:
            # Multiple hashtags can be added
            for tag in data["hashtags"].split(","):
                tag = tag.strip()
                hashtag = Hashtag(tag_label=tag, product_id=product_id)
                db.session.add(hashtag)
            db.session.commit()

        listing = Listing(user_id=current_user.user_id,
                          prod_id=product_id
                          )
        db.session.add(listing)
        db.session.commit()

        if "image_url" in data:
            if "image_caption" in data:
                product_image = Product_Image(
                    image_url=data["image_url"],
                    prod_id=product_id,
                    # Describes what the image is about
                    image_caption=data["image_caption"],
                )
            else:
                product_image = Product_Image(
                    image_url=data["image_url"], prod_id=product_id
                )
            db.session.add(product_image)
            db.session.commit()

        return make_response(jsonify({"message": "Product added successfully"}), 201)

    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 500)


# Route to get/update/delete a product by id
@app.route("/product/<int:id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def product(id):
    if request.method == "GET":
        try:
            required_data = get_product(id)
            return make_response(jsonify(required_data), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    elif request.method == "PUT":
        try:

            db.session.begin_nested()
            product = Product.query.get(id)
            if product is None:
                return make_response(jsonify({"message": "Product not found"}), 404)
            data = request.get_json()

            # Separating data for each table
            product_data = {
                key: value
                for key, value in data.items()
                if key in Product.__table__.columns
            }
            hashtag_data = {
                key: value
                for key, value in data.items()
                if key in Hashtag.__table__.columns
            }
            product_image_data = {
                key: value
                for key, value in data.items()
                if key in Product_Image.__table__.columns
            }

            # Updating the product attributes
            for key, value in product_data.items():
                setattr(product, key, value)

            # ist = timezone(timedelta(hours=5, minutes=30))  # IST (UTC+5:30)
            utc = timezone(timedelta(hours=0, minutes=0))
            product.date_modified = datetime.now(
                utc).strftime("%Y-%m-%d %H:%M:%S")

            # Updating the hashtags
            Hashtag.query.filter_by(product_id=id).delete()
            for key, value in hashtag_data.items():
                for tag in value.split(","):
                    tag = tag.strip()
                    hashtag = Hashtag(tag_label=tag, product_id=id)
                    db.session.add(hashtag)

            # Updating the product image
            product_image = Product_Image.query.filter_by(prod_id=id).first()
            if product_image:
                for key, value in product_image_data.items():
                    setattr(product_image, key, value)

            # The ids are already known, therefore commiting at the end
            db.session.commit()
            return make_response(jsonify({"message": "Product Updated"}), 200)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 500)

    elif request.method == "DELETE":
        try:
            db.session.begin_nested()
            product = Product.query.get(id)
            if product is None:
                return make_response(jsonify({"message": "Product not found"}), 404)
            db.session.delete(product)
            db.session.commit()
            return make_response(jsonify({"message": "Product deleted"}), 200)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 500)


# <---------------------------------------------User Routes----------------------------------------------------->
@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.json
        user = User(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            phone_no=data["phone_no"],
            gender=data["gender"],
            residence_location=data["residence_location"],
            residence_number=data["residence_number"],
            anonymity_level=data["anonymity_level"],
            theme_preference=data["theme_preference"],
            language_preference=data["language_preference"],
            notification_preference=data["notification_preference"],
        )
        user.set_password(data["password"])
        user.save()
        return make_response(jsonify({"message": "User created successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/user", methods=["GET"])
@jwt_required()
@swag_from("docs/get_user.yml")
def get_user_details():
    try:
        # Access the identity of the current user with get_jwt_identity
        current_user_email = get_jwt_identity()

        user = User.query.filter_by(email=current_user_email).first()
        if user is None:
            return make_response(jsonify({"message": "User not found"}), 404)
        res = user.to_dict()
        del res["password"]
        return make_response(jsonify(res), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/user", methods=["PUT"])
@jwt_required()
def update_user():
    try:
        current_user_email = get_jwt_identity()

        db.session.begin_nested()
        user = User.query.filter_by(email=current_user_email).first()
        if user is None:
            return make_response(jsonify({"message": "User not found"}), 404)
        data = request.get_json()
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        res = user.to_dict()
        del res["password"]
        return make_response(jsonify(res), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/user", methods=["DELETE"])
@jwt_required()
def delete_user():
    try:
        current_user_email = get_jwt_identity()

        db.session.begin_nested()
        user = User.query.filter_by(email=current_user_email).first()
        if user is None:
            return make_response(jsonify({"message": "User not found"}), 404)
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"message": "User deleted"}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)


# @app.route("/user/listings", methods=["GET"])
# @jwt_required()
# def get_user_listings():
#     try:
#         current_user_email = get_jwt_identity()
#         current_user = User.query.filter_by(email=current_user_email).first()

#         listings = Listing.query.filter_by(
#             user_id=current_user.user_id).all()
#         return make_response(jsonify([listing.__dict__ for listing in listings]), 200)
#     except Exception as e:
#         return make_response(jsonify({"error": str(e)}), 500)


# <---------------------------------------------App Feedback----------------------------------------------------->
@app.route("/app/feedback", methods=["POST"])
@jwt_required()
def app_feedback():
    try:
        db.session.begin_nested()
        # user_id = current_user.get_id()
        user_id = 2
        data = request.get_json()
        feedback = App_Feedback(
            user_id=user_id,
            feedback_rating=data["rating"],
            feedback_text=data["feedback_text"],
        )
        db.session.add(feedback)
        db.session.commit()
        return make_response(jsonify({"message": "Feedback submitted"}), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)


# <---------------------------------------------Transaction Routes----------------------------------------------------->
@app.route('/user/transactions', methods=['GET'])
@jwt_required()
def all_transactions_():
    try:
        cucurrent_user_email = get_jwt_identity()
        current_user = User.query.filter_by(email=cucurrent_user_email).first()

        transactions = Transaction.query.filter_by(
            seller_id=current_user.user_id).all()
        return make_response(jsonify([transaction.to_dict() for transaction in transactions]), 200)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/user/transactions", methods=["GET"])
@jwt_required()
def all_transactions():
    try:
        cucurrent_user_email = get_jwt_identity()
        current_user = User.query.filter_by(email=cucurrent_user_email).first()

        transactions = Transaction.query.filter(
            or_(Transaction.buyer_id == current_user.user_id,
                Transaction.seller_id == current_user.user_id)
        ).all()
        # return make_response(
        #     jsonify([transaction.to_dict() for transaction in transactions]), 200
        # )

        # response = {transaction + product image}

        response = []
        for entry in transactions:
            data = entry.to_dict()
            prod_id = entry.prod_id
            data["product_image"] = (
                Product_Image.query.filter_by(prod_id=prod_id)
                .first()
                .to_dict()["image_url"]
            )
            data["product_title"] = Product.query.get(
                prod_id).to_dict()["prod_title"]
            data["buyer_name"] = User.query.get(
                entry.buyer_id).to_dict()["name"]
            data["seller_name"] = User.query.get(
                entry.seller_id).to_dict()["name"]
            data["rating"] = Review.query.get(
                entry.review_id).to_dict()["rating"]
            data["review"] = Review.query.get(
                entry.review_id).to_dict()["review_text"]
            response.append(data)

        return make_response(jsonify(response), 200)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/user/transactions/<t_id>", methods=["GET", "PUT"])
@jwt_required()
def get_transaction_details(t_id):
    # Add check for user accessibility
    try:
        if request.method == "GET":
            transaction = Transaction.query.filter_by(
                transaction_id=t_id).first()
            return make_response(transaction.to_dict(), 200)
        else:
            db.session.begin_nested()
            transaction = Transaction.query.get(t_id)
            if transaction is None:
                return make_response(jsonify({"message": "Transaction not found"}), 404)
            data = request.get_json()
            for key, value in data.items():
                setattr(transaction, key, value)
            db.session.commit()
            return make_response(jsonify(transaction.to_dict()), 200)

    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/user/new_transaction", methods=["POST"])
@jwt_required()
def new_transaction():
    try:
        if request.method == 'POST':
            cucurrent_user_email = get_jwt_identity()
            current_user = User.query.filter_by(
                email=cucurrent_user_email).first()

            db.session.begin_nested()
            transaction_details = request.get_json()
            buyer_id = transaction_details["buyer_id"]
            # seller_id = transaction_details["seller_id"]
            seller_id = current_user.user_id
            prod_id = transaction_details["prod_id"]
            # transaction_date = transaction_details['transaction_date']
            transaction_date = datetime.utcnow()
            selling_price = transaction_details["selling_price"]
            quantity = transaction_details["quantity"]

            new_entry = Transaction(
                buyer_id=buyer_id,
                seller_id=seller_id,
                prod_id=prod_id,
                transaction_date=transaction_date,
                selling_price=selling_price,
                quantity=quantity,
            )
            db.session.add(new_entry)
            db.session.commit()

        return make_response(
            jsonify({"message": "Transaction recorded successfully"}), 201
        )

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/review/<r_id>", methods=["GET", "POST", "PUT"])
@jwt_required()
def review(r_id):
    try:
        if request.method == "GET":
            review = Review.query.get(r_id)
            if review is None:
                return make_response(jsonify({"message": "Review not found"}), 404)
            return make_response(jsonify(review.to_dict()), 200)

        elif request.method == "POST":
            review_details = request.get_json()
            review_text = review_details["text"]
            review_rating = review_details["rating"]
            date_of_review = datetime.utcnow()

            new_entry = Review(
                rating=review_rating,
                date_of_review=date_of_review,
                review_text=review_text,
            )
            db.session.add(new_entry)
            db.session.commit()
            return make_response(
                jsonify({"message": "Review submitted successfully!"}), 201
            )

        else:
            review = Review.query.get(r_id)
            if review is None:
                return make_response(jsonify({"message": "Review not found"}), 404)
            data = request.get_json()
            for key, value in data.items():
                setattr(review, key, value)
            db.session.commit()
            return make_response(jsonify(review.to_dict()), 200)

    except Exception as e:

        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/user/review/<t_id>", methods=["POST", "PUT"])
@jwt_required()
def review_trans(t_id):
    try:
        if request.method == "POST":
            db.session.begin_nested()
            review_details = request.get_json()
            review_text = review_details["text"]
            review_rating = review_details["rating"]
            date_of_review = datetime.utcnow()

            new_entry = Review(
                rating=review_rating,
                date_of_review=date_of_review,
                review_text=review_text,
            )
            db.session.add(new_entry)
            db.session.commit()

            # Change the entry in the corresponding transaction
            transaction = Transaction.query.get(t_id)
            transaction.review_id = new_entry.review_id
            db.session.add(transaction)
            db.session.commit()

            return make_response(
                jsonify({"message": "Review submitted successfully!"}), 201
            )
        else:
            db.session.begin_nested()
            transaction = Transaction.query.get(t_id)
            review = Review.query.get(transaction.review_id)
            if review is None:
                return make_response(jsonify({"message": "Review not found"}), 404)
            data = request.get_json()
            for key, value in data.items():
                setattr(review, key, value)
            db.session.commit()
            return make_response(jsonify(review.to_dict()), 200)

    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)


# <---------------------------------------------Chat Routes----------------------------------------------------->
@app.route("/user/senders", methods=["GET"])
@jwt_required()
def all_senders():
    try:
        cucurrent_user_email = get_jwt_identity()
        current_user = User.query.filter_by(email=cucurrent_user_email).first()

        entries = (
            ChatSystem.query.join(
                Listing, Listing.prod_id == ChatSystem.prod_id)
            .filter(Listing.user_id == current_user.user_id)
            .all()
        )
        return make_response(jsonify([entry.to_dict() for entry in entries]), 200)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/user/senders/<p_id>", methods=["GET"])
@jwt_required()
def prod_senders(p_id):
    try:
        cucurrent_user_email = get_jwt_identity()
        current_user = User.query.filter_by(email=cucurrent_user_email).first()

        entries = (
            ChatSystem.query.join(
                Listing, Listing.prod_id == ChatSystem.prod_id)
            .filter(and_(Listing.user_id == current_user.user_id, Listing.prod_id == p_id))
            .all()
        )
        return make_response(jsonify([entry.to_dict() for entry in entries]), 200)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/user/senders/product/<p_id>/<s_id>", methods=["GET"])
@jwt_required()
def messages_see(p_id, s_id):
    try:
        entries = (
            Chat.query.join(
                ChatSystem, ChatSystem.message_id == Chat.message_id)
            .filter(and_(ChatSystem.sender_id == s_id, ChatSystem.prod_id == p_id))
            .all()
        )

        for entry in entries:
            message = Chat.query.get(entry.message_id)
            message.read_status = True

        db.session.commit()
        return make_response(jsonify([entry.to_dict() for entry in entries]), 200)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/user/send/<s_id>/<r_id>/<p_id>", methods=["POST"])
@jwt_required()
def messages_send(p_id, s_id, r_id):
    try:
        if request.method == "POST":
            db.session.begin_nested()
            chat_details = request.get_json()
            message = chat_details["text"]
            chat_time = datetime.now()

            new_entry1 = Chat(
                text=message, chat_time=chat_time, read_status=False)
            db.session.add(new_entry1)
            db.session.commit()

            new_entry2 = ChatSystem(
                message_id=new_entry1.message_id,
                sender_id=s_id,
                reciever_id=r_id,
                prod_id=p_id,
            )
            db.session.add(new_entry2)
            db.session.commit()

        return make_response(jsonify({"message": "Message sent successfully!"}), 201)

    except Exception as e:

        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 500)


# <---------------------------------------------Category Routes----------------------------------------------------->
@app.route("/categories", methods=["GET"])
def get_categories():
    try:
        entries = Category.query.all()
        return make_response(jsonify([entry.to_dict() for entry in entries]), 200)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/subcategory/<int:c_id>", methods=["GET"])
def get_subcategories(c_id):
    try:
        entries = Subcategory.query.filter_by(category_id=c_id)
        return make_response(jsonify([entry.to_dict() for entry in entries]), 200)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/subcategories", methods=["GET"])
def get_all_subcats():
    try:
        entries = Subcategory.query.all()
        return make_response(jsonify([entry.to_dict() for entry in entries]), 200)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
