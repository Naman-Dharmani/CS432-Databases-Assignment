import random
import string
from . import db
from .models import Category, User, Product, Hashtag, Subcategory, Product_Image, Listing


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
    name = ['Parth Deshpande', 'Tirth Patel', 'Naman Dharmani', 'Adit Rambhia', 'Sahil Das',
            'Rachit Verma', 'Yash Bothra', 'Manas Kawal', 'Siddharth Shah', 'Srujan Kumar Shetty']
    email = ['deshpandeparth', 'pateltirth', 'dharmaninaman', 'rambhiaadit', 'dassahil',
             'vermarachit', 'bothrayash', 'kawalmanas', 'shahsiddharth', 'shettysrujan']
    for i in range(len(name)):

        user = User(
            name=name[i],
            email=email[i] + '@iitgn.ac.in',
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

    url = ['https://www.aptronixindia.com/pub/media/catalog/product/m/b/mbp14-spacegray-select-202110-removebg-preview_2__1.png',
           'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS3GgYI1boRNJYqmw6sEvaZURa7ylX1UobMhA&s',
           'https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/ipad-air-finish-select-gallery-202211-purple-wificell_AV1_FMT_WHH?wid=1280&hei=720&fmt=p-jpg&qlt=95&.v=1670633077291',
           'https://www.boat-lifestyle.com/cdn/shop/products/rockerz-518-blue.png?v=1613731627',
           'https://5.imimg.com/data5/SELLER/Default/2022/9/OK/RL/XN/42175339/nikon-d7500-dslr-camera-500x500.jpg',
           'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhV8r1EAhL0nemzWh4bOIK-uDujSiYbEp2GfPZcxTVYA&s',
           'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFTmmfpJKrm2d5BeMu6qGsvXa_05BE5ZCDaD6TxEwYkQ&s',
           'https://5.imimg.com/data5/SELLER/Default/2023/8/334128858/YQ/JG/IN/5847953/mixer-grinder-for-home-750-watt.jpg',
           'https://5.imimg.com/data5/SELLER/Default/2023/8/334128858/YQ/JG/IN/5847953/mixer-grinder-for-home-750-watt.jpg',
           'https://images-cdn.ubuy.co.in/633b131b9bfd300af1121135-smartdevil-space-heater-70.jpg']
    for i in range(10):
        product_image = Product_Image(
            image_url=url[i],
            prod_id=i+1,
            image_caption='This is a placeholder image'
        )
        db.session.add(product_image)

    # Create 10 Products
    productname = ['Macbook M1', 'Iphone 15', 'Ipad Air', 'Boat Headphones', 'Nikon DSLR',
                   'Sony SmartTV', 'Apple Watch Series 9', 'Mixer-Grinder', 'PS5', 'Heater']
    for i in range(len(productname)):
        product = Product(
            prod_title=productname[i],
            description=f'This is a {productname[i]}',
            prod_condition=random.choice(['New', 'Used']),
            listed_price=random.randint(0, 1000),
            quantity=random.randint(1, 4),
            subcategory_id=i+1
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

    # Create a Listings
    for i in range(1, 11):
        user = User.query.get(i)
        product = Product.query.get(i)
        listings = Listing(
            user_id=user.user_id,
            prod_id=product.prod_id
        )
        db.session.add(listings)
        db.session.commit()

if __name__ == '__main__':
    seed_db()
