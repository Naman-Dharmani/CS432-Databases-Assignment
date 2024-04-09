# import random
# import string
from . import db
from .models import (
    Category,
    Chat,
    ChatSystem,
    Review,
    Transaction,
    User,
    Product,
    Hashtag,
    Subcategory,
    User_Image,
    Product_Image,
    Listing,
)


def seed_db2():
    users = [
        User(
            name="Alice Smith",
            email="alice.smith@example.com",
            password="password123",
            phone_no="2345678901",
            gender="Female",
            residence_location="Los Angeles",
            residence_number="456 Elm St",
        ),
        User(
            name="Bob Johnson",
            email="bob.johnson@example.com",
            password="password456",
            phone_no="3456789012",
            gender="Male",
            residence_location="Chicago",
            residence_number="789 Oak St",
        ),
        User(
            name="Eve Wilson",
            email="eve.wilson@example.com",
            password="password789",
            phone_no="4567890123",
            gender="Other",
            residence_location="Miami",
            residence_number="012 Pine St",
        ),
        User(
            name="Charlie Brown",
            email="charlie.brown@example.com",
            password="passwordabc",
            phone_no="5678901234",
            gender="Male",
            residence_location="Houston",
            residence_number="123 Cedar St",
        ),
        User(
            name="Grace Davis",
            email="grace.davis@example.com",
            password="passworddef",
            phone_no="6789012345",
            gender="Female",
            residence_location="Phoenix",
            residence_number="234 Maple St",
        ),
        User(
            name="David Lee",
            email="david.lee@example.com",
            password="passwordghi",
            phone_no="7890123456",
            gender="Male",
            residence_location="Seattle",
            residence_number="345 Birch St",
        ),
    ]
    db.session.add_all(users)
    db.session.commit()

    categories = [
        Category(category_name="Electronics"),
        Category(category_name="Furniture"),
        Category(category_name="Clothing"),
        Category(category_name="Books"),
        Category(category_name="Toys"),
        Category(category_name="Sports"),
        Category(category_name="Beauty"),
        Category(category_name="Home Decor"),
        Category(category_name="Accessories"),
        Category(category_name="Jewelry"),
    ]
    db.session.add_all(categories)
    db.session.commit()

    subcategories = [
        Subcategory(subcategory_name="Smartphones", category_id=1),
        Subcategory(subcategory_name="Laptops", category_id=1),
        Subcategory(subcategory_name="Tablets", category_id=1),
        Subcategory(subcategory_name="Headphones", category_id=1),
        Subcategory(subcategory_name="Cameras", category_id=1),
        Subcategory(subcategory_name="Monitors", category_id=1),
        Subcategory(subcategory_name="Desks", category_id=2),
        Subcategory(subcategory_name="Chairs", category_id=2),
        Subcategory(subcategory_name="Sofas", category_id=2),
        Subcategory(subcategory_name="Beds", category_id=2),
        Subcategory(subcategory_name="Dresses", category_id=3),
        Subcategory(subcategory_name="Shirts", category_id=3),
        Subcategory(subcategory_name="Pants", category_id=3),
        Subcategory(subcategory_name="Shoes", category_id=3),
        Subcategory(subcategory_name="Hats", category_id=3),
        Subcategory(subcategory_name="Fiction", category_id=4),
        Subcategory(subcategory_name="Non-Fiction", category_id=4),
        Subcategory(subcategory_name="Children's Books", category_id=4),
        Subcategory(subcategory_name="Textbooks", category_id=4),
        Subcategory(subcategory_name="Sci-Fi", category_id=4),
        Subcategory(subcategory_name="Action Figures", category_id=5),
        Subcategory(subcategory_name="Board Games", category_id=5),
        Subcategory(subcategory_name="Puzzles", category_id=5),
        Subcategory(subcategory_name="LEGO", category_id=5),
        Subcategory(subcategory_name="Basketball", category_id=6),
        Subcategory(subcategory_name="Soccer", category_id=6),
        Subcategory(subcategory_name="Football", category_id=6),
        Subcategory(subcategory_name="Tennis", category_id=6),
        Subcategory(subcategory_name="Running", category_id=6),
        Subcategory(subcategory_name="Makeup", category_id=7),
        Subcategory(subcategory_name="Skincare", category_id=7),
        Subcategory(subcategory_name="Haircare", category_id=7),
        Subcategory(subcategory_name="Fragrance", category_id=7),
        Subcategory(subcategory_name="Tools", category_id=7),
        Subcategory(subcategory_name="Wall Art", category_id=8),
        Subcategory(subcategory_name="Rugs", category_id=8),
        Subcategory(subcategory_name="Lighting", category_id=8),
        Subcategory(subcategory_name="Decorative Pillows", category_id=8),
        Subcategory(subcategory_name="Vases", category_id=8),
        Subcategory(subcategory_name="Watches", category_id=9),
        Subcategory(subcategory_name="Necklaces", category_id=9),
        Subcategory(subcategory_name="Bracelets", category_id=9),
        Subcategory(subcategory_name="Earrings", category_id=9),
        Subcategory(subcategory_name="Rings", category_id=9),
    ]
    db.session.add_all(subcategories)
    db.session.commit()

    products = [
        Product(
            prod_title="Smartphone",
            description="Brand new smartphone",
            prod_condition="New",
            listed_price=500.00,
            quantity=10,
            subcategory_id=1,
        ),
        Product(
            prod_title="Desk Lamp",
            description="Adjustable desk lamp",
            prod_condition="Used",
            listed_price=20.00,
            quantity=5,
            subcategory_id=2,
        ),
        Product(
            prod_title="Headphones",
            description="High-quality headphones",
            prod_condition="New",
            listed_price=100.00,
            quantity=8,
            subcategory_id=4,
        ),
        Product(
            prod_title="Backpack",
            description="Durable backpack",
            prod_condition="Used",
            listed_price=30.00,
            quantity=3,
            subcategory_id=9,
        ),
        Product(
            prod_title="Camera",
            description="Professional camera",
            prod_condition="New",
            listed_price=800.00,
            quantity=2,
            subcategory_id=5,
        ),
        Product(
            prod_title="Monitor",
            description="27-inch computer monitor",
            prod_condition="Used",
            listed_price=150.00,
            quantity=6,
            subcategory_id=6,
        ),
    ]

    db.session.add_all(products)
    db.session.commit()

    # Create instances of Hashtag and add them to the session
    hashtags = [
        Hashtag(tag_label="electronics", product_id=1),
        Hashtag(tag_label="furniture", product_id=2),
        Hashtag(tag_label="audio", product_id=3),
        Hashtag(tag_label="accessories", product_id=4),
        Hashtag(tag_label="photography", product_id=5),
        Hashtag(tag_label="computers", product_id=6),
    ]

    db.session.add_all(hashtags)
    db.session.commit()

    reviews = [
        Review(
            rating="5",
            review_text="Great seller! Fast shipping.",
            date_of_review="2024-02-14 08:30:00",
        ),
        Review(
            rating="4",
            review_text="Good product, as described.",
            date_of_review="2024-02-14 09:00:00",
        ),
        Review(
            rating="3",
            review_text="Average quality, expected better.",
            date_of_review="2024-02-14 09:30:00",
        ),
        Review(
            rating="5",
            review_text="Excellent service, highly recommend.",
            date_of_review="2024-02-14 10:00:00",
        ),
        Review(
            rating="4",
            review_text="Fast transaction, good communication.",
            date_of_review="2024-02-14 10:30:00",
        ),
        Review(
            rating="2",
            review_text="Product was damaged, not happy.",
            date_of_review="2024-02-14 11:00:00",
        ),
        Review(
            rating="1",
            review_text="Terrible experience, would not buy again.",
            date_of_review="2024-02-14 11:30:00",
        ),
    ]

    db.session.add_all(reviews)
    db.session.commit()

    # Create instances of Transaction and add them to the session

    transactions = [
        Transaction(
            transaction_id=1,
            buyer_id=1,
            seller_id=2,
            review_id=1,
            prod_id=1,
            selling_price=500.00,
            quantity=1,
        ),
        Transaction(
            transaction_id=2,
            buyer_id=2,
            seller_id=3,
            review_id=2,
            prod_id=2,
            selling_price=20.00,
            quantity=1,
        ),
        Transaction(
            transaction_id=3,
            buyer_id=3,
            seller_id=4,
            review_id=3,
            prod_id=3,
            selling_price=100.00,
            quantity=1,
        ),
        Transaction(
            transaction_id=4,
            buyer_id=4,
            seller_id=5,
            review_id=4,
            prod_id=4,
            selling_price=30.00,
            quantity=1,
        ),
        Transaction(
            transaction_id=5,
            buyer_id=5,
            seller_id=6,
            review_id=5,
            prod_id=5,
            selling_price=800.00,
            quantity=1,
        ),
        Transaction(
            transaction_id=6,
            buyer_id=6,
            seller_id=1,
            review_id=6,
            prod_id=6,
            selling_price=150.00,
            quantity=1,
        ),
        Transaction(
            transaction_id=7,
            buyer_id=1,
            seller_id=2,
            review_id=7,
            prod_id=1,
            selling_price=500.00,
            quantity=1,
        ),
    ]

    db.session.add_all(transactions)
    db.session.commit()

    # Create instances of Review and add them to the session

    # Create instances of Chat and add them to the session
    chats = [
        Chat(
            chat_time="2024-02-14 08:30:00",
            text="Hello, how can I help you?",
            read_status=False,
        ),
        Chat(
            chat_time="2024-02-14 09:00:00",
            text="Hello, how can I help you?",
            read_status=False,
        ),
        Chat(
            chat_time="2024-02-14 09:30:00",
            text="Sure, let me know if you have any questions.",
            read_status=False,
        ),
        Chat(
            chat_time="2024-02-14 10:00:00",
            text="Thank you, I will.",
            read_status=False,
        ),
        Chat(
            chat_time="2024-02-14 10:30:00",
            text="Hello, is this still available?",
            read_status=False,
        ),
        Chat(
            chat_time="2024-02-14 11:00:00",
            text="Yes, it is still available.",
            read_status=False,
        ),
        Chat(
            chat_time="2024-02-14 11:30:00",
            text="Great, I would like to buy it.",
            read_status=False,
        ),
    ]

    db.session.add_all(chats)
    db.session.commit()

    chat_systems = [
        ChatSystem(message_id=1, sender_id=2, reciever_id=1, prod_id=1),
        ChatSystem(message_id=2, sender_id=2, reciever_id=3, prod_id=2),
        ChatSystem(message_id=3, sender_id=3, reciever_id=4, prod_id=3),
        ChatSystem(message_id=4, sender_id=4, reciever_id=5, prod_id=4),
        ChatSystem(message_id=5, sender_id=5, reciever_id=6, prod_id=5),
        ChatSystem(message_id=6, sender_id=6, reciever_id=1, prod_id=6),
        ChatSystem(message_id=7, sender_id=1, reciever_id=1, prod_id=2),
    ]

    db.session.add_all(chat_systems)
    db.session.commit()

    listings = [
        Listing(user_id=1, prod_id=1),
        Listing(user_id=2, prod_id=2),
        Listing(user_id=3, prod_id=3),
        Listing(user_id=4, prod_id=4),
        Listing(user_id=5, prod_id=5),
        Listing(user_id=6, prod_id=6),
        Listing(user_id=1, prod_id=2),
        Listing(user_id=2, prod_id=3),
        Listing(user_id=3, prod_id=4),
        Listing(user_id=4, prod_id=5),
        Listing(user_id=5, prod_id=6),
        Listing(user_id=6, prod_id=1),
    ]

    db.session.add_all(listings)
    db.session.commit()

    user_images = [
        User_Image(user_id=1, image_url="https://picsum.photos/200"),
        User_Image(user_id=2, image_url="https://picsum.photos/200"),
        User_Image(user_id=3, image_url="https://picsum.photos/200"),
        User_Image(user_id=4, image_url="https://picsum.photos/200"),
        User_Image(user_id=5, image_url="https://picsum.photos/200"),
        User_Image(user_id=6, image_url="https://picsum.photos/200"),
    ]
    db.session.add_all(user_images)
    db.session.commit()

    product_images = [
        Product_Image(
            prod_id=1,
            image_url="https://www.aptronixindia.com/pub/media/catalog/product/m/b/mbp14-spacegray-select-202110-removebg-preview_2__1.png",
        ),
        Product_Image(
            prod_id=2,
            image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS3GgYI1boRNJYqmw6sEvaZURa7ylX1UobMhA&s",
        ),
        Product_Image(
            prod_id=3,
            image_url="https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/ipad-air-finish-select-gallery-202211-purple-wificell_AV1_FMT_WHH?wid=1280&hei=720&fmt=p-jpg&qlt=95&.v=1670633077291",
        ),
        Product_Image(
            prod_id=4,
            image_url="https://www.boat-lifestyle.com/cdn/shop/products/rockerz-518-blue.png?v=1613731627",
        ),
        Product_Image(
            prod_id=5,
            image_url="https://5.imimg.com/data5/SELLER/Default/2022/9/OK/RL/XN/42175339/nikon-d7500-dslr-camera-500x500.jpg",
        ),
        Product_Image(
            prod_id=6,
            image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhV8r1EAhL0nemzWh4bOIK-uDujSiYbEp2GfPZcxTVYA&s",
        ),
    ]
    db.session.add_all(product_images)
    db.session.commit()
