import random
import string
from . import db
from .models import Category, User, Product, Hashtag, Subcategory
from app import app

def random_string(length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def random_number(length=10):
    """Generate a random number of fixed length """
    numbers = string.digits
    return ''.join(random.choice(numbers) for i in range(length))

def seed_db():
    # Create 10 Users
    # TODO: password needs to be hashed
    for _ in range(10):
        user = User(
            name=random_string(),
            email=f'{random_string()}@example.com',
            password='password',
            phone_no=random_number(10),
            gender=random.choice(['Male', 'Female', 'Other']),
            residence_location=random_string(5),
            residence_number=random_number(3)
        )
        user.set_password(user.password)
        db.session.add(user)

    # Create a Category
    category = Category(
        category_name='Electronics'
    )
    db.session.add(category)

    subcategory = Subcategory(
        subcategory_name='Electronics',
        category_id=1
    )
    db.session.add(subcategory)

    # Create 10 Products
    for _ in range(10):
        product = Product(
            prod_title=random_string(10),
            description=random_string(100),
            prod_condition=random.choice(['New', 'Used']),
            listed_price=random.uniform(0, 1000),
            quantity=random.randint(1, 100),
            subcategory_id=1
        )
        db.session.add(product)

    # Create 10 Hashtags
    for _ in range(10):
        hashtag = Hashtag(
            tag_label=random_string(7),
            product_id=random.randint(1, 10)
        )
        db.session.add(hashtag)

    # Commit the changes
    db.session.commit()

if __name__ == '__main__':
    seed_db()