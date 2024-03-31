import random
import string
from . import db
from .models import User, Product, Hashtag
from app import app

def random_string(length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def seed_db():
    # Create 100 Users
    for _ in range(100):
        user = User(
            name=random_string(),
            email=f'{random_string()}@example.com',
            password='password',
            phone_no=random_string(10),
            gender=random.choice(['Male', 'Female', 'Other']),
            residence_location=random_string(255),
            residence_number=random_string(255)
        )
        db.session.add(user)

    # Create 100 Products
    for _ in range(100):
        product = Product(
            prod_title=random_string(30),
            description=random_string(400),
            prod_condition=random.choice(['New', 'Used']),
            listed_price=random.uniform(0, 1000),
            quantity=random.randint(1, 100)
        )
        db.session.add(product)

    # Create 100 Hashtags
    for _ in range(100):
        hashtag = Hashtag(
            tag_label=random_string(27),
            product_id=random.randint(1, 100)
        )
        db.session.add(hashtag)

    # Commit the changes
    db.session.commit()

if __name__ == '__main__':
    seed_db()