import random
import string
from . import db
from .models import Category, User, Product, Hashtag, Subcategory, Product_Image


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
    name=['Parth Deshpande', 'Tirth Patel', 'Naman Dharmani', 'Adit Rambhia', 'Adit Rambhia']
    email=['deshpandeparth', 'pateltirth', 'dharmaninaman', 'rambhiaadit', 'rambhiaadit']
    for i in range(10):

        user = User(
            name= name[i],
            email= email[i] + '@iitgn.ac.in',
            password='password',
            phone_no=random_number(10),
            gender='Male',
            residence_location='Emiet',
            residence_number=random_number(3)
        )
        user.set_password(user.password)
        db.session.add(user)

    # Create a Category
    categories = [
        Category(category_name='Electronics'),
        Category(category_name='Furniture'),
        Category(category_name='Clothing'),
        Category(category_name='Books'),
        Category(category_name='Toys'),
        Category(category_name='Sports'),
        Category(category_name='Beauty'),
        Category(category_name='Home Decor'),
        Category(category_name='Accessories'),
        Category(category_name='Jewelry')
    ]

    for category in categories:
        db.session.add(category)

    db.session.commit()

    subcategories = [
        Subcategory(subcategory_name='Smartphones', category_id=1),
        Subcategory(subcategory_name='Laptops', category_id=2),
        Subcategory(subcategory_name='Tablets', category_id=3),
        Subcategory(subcategory_name='Headphones', category_id=4),
        Subcategory(subcategory_name='Cameras', category_id=5),
        Subcategory(subcategory_name='Televisions', category_id=6),
        Subcategory(subcategory_name='Smart Watches', category_id=7),
        Subcategory(subcategory_name='Gaming Consoles', category_id=8),
        Subcategory(subcategory_name='Accessories', category_id=9),
        Subcategory(subcategory_name='Home Appliances', category_id=10)
    ]

    for subcategory in subcategories:
        db.session.add(subcategory)

    db.session.commit()

    for i in range(10):
        product_image = Product_Image(
            image_url='/placeholder.svg',
            prod_id=i+1,
            image_caption='This is a placeholder image'
        )
        db.session.add(product_image)

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
            tag_label='#'+random_string(7),
            product_id=random.randint(1, 10)
        )
        db.session.add(hashtag)

    # Commit the changes
    db.session.commit()


if __name__ == '__main__':
    seed_db()
