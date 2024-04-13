from flask import redirect, request, make_response, jsonify, url_for, flash
from flasgger import swag_from
from datetime import datetime, timedelta, timezone

from . import app
from .models import db
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
from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload
from flask_dance.contrib.google import google
from flask_login import login_required, logout_user

pagination_per_page = 5


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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("home"))


@app.route("/login")
def login():
    return redirect(url_for("google.login"))


def get_product(id):
    product = (
        Product.query.options(
            joinedload(Product.subcategory).joinedload(Subcategory.category),
            joinedload(Product.product_images),
            joinedload(Product.hashtags),
        )
        .filter_by(prod_id=id)
        .first()
    )

    if product is None:
        return make_response({"message": "Product not found"}, 404)

    product_dict = product.to_dict()
    product_dict["subcategory"] = product.subcategory.to_dict()
    product_dict["category"] = product.subcategory.category.to_dict()
    product_dict["product_images"] = [
        image.to_dict() for image in product.product_images
    ]
    product_dict["hashtags"] = [
        hashtag.to_dict()["tag_label"] for hashtag in product.hashtags
    ]

    return product_dict


# Route to get all products with pagination
@app.route("/products", methods=["GET"])
def get_products():
    # Retriving the page number from the query string
    try:
        page_num = request.args.get("page", 1, type=int)
        # per_page is the max number of products to be shown
        # If there are more products, the has_next attribute will be True
        # IF there are fewer products, the has_next attribute will be False
        page = Product.query.order_by(Product.date_listed.desc()).paginate(
            page=page_num, per_page=pagination_per_page
        )
        products_json = [get_product(product.prod_id) for product in page.items]
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
# @login_required
def create_product():
    try:
        data = request.json

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

        # if len(hashtags) > 0:
        #    for tag in hashtags:
        #        tag = tag.strip()
        #        hashtag = Hashtag(tag_label=tag,
        #                          product_id=product_id
        #                          )
        #        db.session.add(hashtag)
        #    db.session.commit()

        if "hashtags" in data:
            # Multiple hashtags can be added
            for tag in data["hashtags"].split(","):
                tag = tag.strip()
                hashtag = Hashtag(tag_label=tag, product_id=product_id)
                db.session.add(hashtag)
            db.session.commit()

        # TODO: uncomment this once login is required
        # user_id = current_user.get_id()
        # listing = Listing(user_id=user_id,
        #                   prod_id=product_id
        #                   )
        # db.session.add(listing)
        # db.session.commit()

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
        return make_response(jsonify({"error": str(e)}), 500)


# Route to get/update/delete a product by id


@app.route("/product/<int:id>", methods=["GET", "PUT", "DELETE"])
def product(id):
    if request.method == "GET":
        try:
            # required_prod = Product.query.filter_by(
            #         prod_id=id).first().to_dict()

            # # If the product is not found, return a 404 error
            # if required_prod == None:
            #     return make_response({"message": 'Product not found'}, 404)

            # # If product is found, get the other details
            # subcategory_id = required_prod.get('subcategory_id')
            # subcategory = Subcategory.query.filter_by(
            #     subcategory_id=subcategory_id).first().to_dict()

            # category_id = subcategory.get('category_id')
            # category = Category.query.filter_by(category_id=category_id).first().to_dict()

            # hashtags = [hashtag.to_dict()['tag_label']
            #             for hashtag in Hashtag.query.filter_by(product_id=id).all()]

            # # hashtags = Hashtag.query.filter_by(product_id=id).all().to_dict()
            # product_image = Product_Image.query.filter_by(
            #     prod_id=id).first().to_dict()

            # hashtags = dict(tag_label=hashtags)

            # required_data = {**required_prod, **category,
            #                  **subcategory, **hashtags, **product_image}
            # print(required_data)
            required_data = get_product(id)
            return make_response(jsonify(required_data), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    elif request.method == "PUT":
        try:
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
            # category_data = {key: value for key, value in data.items(
            # ) if key in Category.__table__.columns}
            # subcategory_data = {key: value for key, value in data.items(
            # ) if key in Subcategory.__table__.columns}
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
            product.date_modified = datetime.now(utc).strftime("%Y-%m-%d %H:%M:%S")

            # # Updating the category attributes
            # category = Category.query.filter_by(prod_id=id).first()
            # if category:
            #     for key, value in category_data.items():
            #         setattr(category, key, value)

            # # Updating the subcategory attributes
            # subcategory = Subcategory.query.filter_by(
            #     category_id=category.category_id).first()
            # if subcategory:
            #     for key, value in subcategory_data.items():
            #         setattr(subcategory, key, value)

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
            return make_response(jsonify({"error": str(e)}), 500)

    elif request.method == "DELETE":
        try:
            product = Product.query.get(id)
            if product is None:
                return make_response(jsonify({"message": "Product not found"}), 404)
            db.session.delete(product)
            db.session.commit()
            return make_response(jsonify({"message": "Product deleted"}), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


# <---------------------------------------------User Routes----------------------------------------------------->
# TODO


@app.route("/user/<int:u_id>", methods=["GET"])
@swag_from("docs/get_user.yml")
def get_user(u_id):
    try:
        user = User.query.get(u_id)
        if user is None:
            return make_response(jsonify({"message": "User not found"}), 404)
        res = user.to_dict()
        del res["password"]
        return make_response(jsonify(res), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/user/<int:u_id>", methods=["PUT"])
def update_user(u_id):
    try:
        user = User.query.get(u_id)
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
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/user/<int:u_id>", methods=["DELETE"])
def delete_user(u_id):
    try:
        user = User.query.get(u_id)
        if user is None:
            return make_response(jsonify({"message": "User not found"}), 404)
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"message": "User deleted"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/user/<int:u_id>/listings", methods=["GET"])
def get_user_listings(u_id):
    try:
        listings = Listing.query.filter_by(user_id=u_id).all()
        return make_response(jsonify([listing.__dict__ for listing in listings]), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


# <---------------------------------------------App Feedback----------------------------------------------------->
@app.route("/app/feedback", methods=["POST"])
def app_feedback():
    try:
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
        return make_response(jsonify({"error": str(e)}), 500)


# <---------------------------------------------Transaction Routes----------------------------------------------------->


@app.route("/user/<u_id>/transactions", methods=["GET"])
def all_transactions(u_id):
    try:
        transactions = Transaction.query.filter(
            or_(Transaction.buyer_id == u_id, Transaction.seller_id == u_id)
        ).all()
        return make_response(
            jsonify([transaction.to_dict() for transaction in transactions]), 200
        )

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/user/transactions/<t_id>", methods=["GET", "PUT"])
def get_transaction_details(t_id):
    # Add check for user accessibility
    try:
        if request.method == "GET":
            transaction = Transaction.query.filter_by(transaction_id=t_id).first()
            return make_response(transaction.to_dict(), 200)

        else:
            transaction = Transaction.query.get(t_id)
            if transaction is None:
                return make_response(jsonify({"message": "Transaction not found"}), 404)
            data = request.get_json()
            for key, value in data.items():
                setattr(transaction, key, value)
            db.session.commit()
            return make_response(jsonify(transaction.to_dict()), 200)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/user/new_transaction", methods=["POST"])
def new_transaction():
    try:
        if request.method == "POST":
            transaction_details = request.get_json()
            buyer_id = transaction_details["buyer_id"]
            seller_id = transaction_details["seller_id"]
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


@app.route("/user/review/<t_id>", methods=["POST", "PUT"])
def review_trans(t_id):
    try:
        if request.method == "POST":
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
        return make_response(jsonify({"error": str(e)}), 500)


# <---------------------------------------------Chat Routes----------------------------------------------------->


@app.route("/user/senders/<u_id>", methods=["GET"])
def all_senders(u_id):
    try:
        entries = (
            ChatSystem.query.join(Listing, Listing.prod_id == ChatSystem.prod_id)
            .filter(Listing.user_id == u_id)
            .all()
        )
        return make_response(jsonify([entry.to_dict() for entry in entries]), 200)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/user/senders/<u_id>/<p_id>", methods=["GET"])
def prod_senders(u_id, p_id):
    try:
        entries = (
            ChatSystem.query.join(Listing, Listing.prod_id == ChatSystem.prod_id)
            .filter(and_(Listing.user_id == u_id, Listing.prod_id == p_id))
            .all()
        )
        return make_response(jsonify([entry.to_dict() for entry in entries]), 200)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/user/senders/product/<p_id>/<s_id>", methods=["GET"])
def messages_see(p_id, s_id):
    try:
        entries = (
            Chat.query.join(ChatSystem, ChatSystem.message_id == Chat.message_id)
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
def messages_send(p_id, s_id, r_id):
    try:
        if request.method == "POST":
            chat_details = request.get_json()
            message = chat_details["text"]
            chat_time = datetime.now()

            new_entry1 = Chat(text=message, chat_time=chat_time, read_status=False)
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
