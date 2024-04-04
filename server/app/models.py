from sqlalchemy import Column, Integer, String, Enum, DECIMAL, TIMESTAMP, Boolean, ForeignKey, Text, DateTime, CheckConstraint, TIME
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from sqlalchemy import func


class User(UserMixin, db.Model):
    
    __tablename__ = 'User'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    email = Column(String(60), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    date_joined = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    phone_no = Column(String(10), nullable=False, unique=True)
    gender = Column(Enum('Male', 'Female', 'Other'), nullable=False)
    time_availability_start = Column(TIME)
    time_availability_end = Column(TIME)
    residence_location = Column(String(255), nullable=False)
    residence_number = Column(String(255), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    anonymity_level = Column(Enum('Visible', 'Anonymous'), nullable=False, default='Visible')
    theme_preference = Column(Enum('Dark', 'Light'), default='Light')
    language_preference = Column(Enum('English', 'Hindi'), default='English')
    notification_preference = Column(Enum('All', 'Chat', 'None'), default='All')
    user_images = relationship('User_Image', backref='user', lazy='dynamic', cascade="all,delete")
    products = relationship('Product', backref='user', lazy='dynamic', cascade="all,delete")
    notifications = relationship('Notification', backref='user', lazy='dynamic', cascade="all,delete")
    devices = relationship('Devices', backref='user', lazy='dynamic', cascade="all,delete")
    # app_feedback = relationship('App_Feedback', backref='user', lazy='dynamic', cascade="all,delete")
    # reviews = relationship('Review', backref='user', lazy='dynamic', cascade="all,delete")
    interests = relationship('Interest', backref='user', lazy='dynamic', cascade="all,delete")
    listings = relationship('Listing', backref='user', lazy='dynamic', cascade="all,delete")
    seller = relationship('Seller', backref='user', lazy='dynamic', cascade="all,delete")
    # transactions = relationship('Transaction', backref='user', lazy='dynamic', cascade="all,delete")
    # chat_system = relationship('ChatSystem', backref='user', lazy='dynamic', cascade="all,delete")


    def __repr__(self):
        return f"<User(user_id={self.user_id}, name='{self.name}', email='{self.email}')>"

    def get_id(self):
        return self.user_id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
    
class Product(db.Model):
    
    __tablename__ = 'Product'
    prod_id = Column(Integer, primary_key=True, autoincrement=True)
    prod_title = Column(String(30), nullable=False)
    description = Column(String(400), nullable=False)
    status = Column(Enum('Available', 'Sold'), nullable=False, default='Available')
    prod_condition = Column(Enum('New', 'Used'), nullable=False, default='Used')
    listed_price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    date_listed = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    date_modified = Column(TIMESTAMP)
    flagging = Column(Integer, default=0)
    hashtags = relationship('Hashtag', backref='product', lazy='dynamic', cascade="all,delete")
    categories = relationship('Category', backref='product', lazy='dynamic', cascade="all,delete")
    product_images = relationship('Product_Image', backref='product', lazy='dynamic', cascade="all,delete")
    seller = relationship('Seller', backref='product', lazy='dynamic', cascade="all,delete")
    # transactions = relationship('Transaction', backref='product', lazy='dynamic', cascade="all,delete")
    interests = relationship('Interest', backref='product', lazy='dynamic', cascade="all,delete")
    listings = relationship('Listing', backref='product', lazy='dynamic', cascade="all,delete")
    # chat_system = relationship('ChatSystem', backref='product', lazy='dynamic', cascade="all,delete")

    def __repr__(self):
        return f"<Product(prod_id={self.prod_id}, prod_title='{self.prod_title}', prod_condition='{self.prod_condition}')>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Chat(db.Model):
    __tablename__ = 'Chat'

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    chat_time = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    text = Column(String(255), nullable=False)
    read_status = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Chat(message_id={self.message_id}, chat_time='{self.chat_time}', text='{self.text}', read_status={self.read_status})>"
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Hashtag(db.Model):
    __tablename__ = 'Hashtag'

    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_label = Column(String(27), nullable=False)
    product_id = Column(Integer, ForeignKey('Product.prod_id'), nullable=False)
    product = relationship("Product")

    def __repr__(self):
        return f"<Hashtag(tag_id={self.tag_id}, tag_label='{self.tag_label}', product_id={self.product_id})>"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Notification(db.Model):
    __tablename__ = 'Notification'

    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(255), nullable=False, default='')
    time = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    read_status = Column(Boolean, nullable=False, default=False)
    user_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    user = relationship("User")

    def __repr__(self):
        return f"<Notification(notification_id={self.notification_id}, content='{self.content}', time='{self.time}', read_status={self.read_status}, user_id={self.user_id})>"

class Category(db.Model):
    __tablename__ = 'Category'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(50), nullable=False)
    prod_id = Column(Integer, ForeignKey('Product.prod_id'), nullable=False)
    product = relationship("Product")
    subcategories = relationship('Subcategory', backref='category', lazy='dynamic', cascade="all,delete")

    def __repr__(self):
        return f"<Category(category_id={self.category_id}, category_name='{self.category_name}', prod_id={self.prod_id})>"
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Subcategory(db.Model):
    __tablename__ = 'Subcategory'

    subcategory_id = Column(Integer, primary_key=True, autoincrement=True)
    subcategory_name = Column(String(50), nullable=False)
    category_id = Column(Integer, ForeignKey('Category.category_id'), nullable=False)
    category = relationship("Category")

    def __repr__(self):
        return f"<Subcategory(subcategory_id={self.subcategory_id}, subcategory_name='{self.subcategory_name}', category_id={self.category_id})>"
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class User_Image(db.Model):
    __tablename__ = 'User_Image'

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(3072), nullable=False)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    image_caption = Column(String(20))

    def __repr__(self):
        return f"<User_Image(image_id={self.image_id}, image_url='{self.image_url}', user_id={self.user_id}, image_caption='{self.image_caption}')>"

class Product_Image(db.Model):
    __tablename__ = 'Product_Image'

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(3072), nullable=False)
    prod_id = Column(Integer, ForeignKey('Product.prod_id'))
    image_caption = Column(String(20))

    def __repr__(self):
        return f"<Product_Image(image_id={self.image_id}, image_url='{self.image_url}', prod_id={self.prod_id}, image_caption='{self.image_caption}')>"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Seller(db.Model):
    __tablename__ = 'Seller'

    user_id = Column(Integer, primary_key=True)
    avg_seller_rating = Column(DECIMAL(10, 2))
    preferred_payment_method = Column(Enum('Cash', 'UPI', 'Net Banking', name='payment_method'), nullable=False, default='UPI')

    def __repr__(self):
        return f"<Seller(user_id={self.user_id}, avg_seller_rating={self.avg_seller_rating}, preferred_payment_method='{self.preferred_payment_method}')>"

class Review(db.Model):
    __tablename__ = 'Review'

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Enum('1', '2', '3', '4', '5', name='rating'), nullable=False)
    review_text = Column(String(255))
    date_of_review = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Review(review_id={self.review_id}, rating='{self.rating}', review_text='{self.review_text}', date_of_review='{self.date_of_review}')>"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class Devices(db.Model):
    __tablename__ = 'Devices'

    device_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    date_time_login = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    device_ip = Column(String(40), nullable=False)
    device_user_agent = Column(Text, nullable=False)

    def __repr__(self):
        return f"<Devices(device_id={self.device_id}, user_id={self.user_id}, date_time_login='{self.date_time_login}', device_ip='{self.device_ip}', device_user_agent='{self.device_user_agent}')>"

class App_Feedback(db.Model):
    __tablename__ = 'App_Feedback'

    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    feedback_time = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    feedback_rating = Column(Enum('1', '2', '3', '4', '5', name='feedback_rating'), nullable=False)
    feedback_text = Column(Text)

    def __repr__(self):
        return f"<App_Feedback(feedback_id={self.feedback_id}, user_id={self.user_id}, feedback_time='{self.feedback_time}', feedback_rating='{self.feedback_rating}', feedback_text='{self.feedback_text}')>"

class Transaction(db.Model):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey('User.user_id'))
    seller_id = Column(Integer, ForeignKey('User.user_id'))
    review_id = Column(Integer)
    prod_id = Column(Integer, ForeignKey('Product.prod_id'))
    transaction_date = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    selling_price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    __table_args__ = (
        CheckConstraint('quantity >= 1', name='quantity_check'),
    )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Interest(db.Model):
    __tablename__ = 'interests'

    user_id = Column(Integer, ForeignKey('User.user_id'), primary_key=True)
    prod_id = Column(Integer, ForeignKey('Product.prod_id'), primary_key=True)

class Listing(db.Model):
    __tablename__ = 'listings'

    user_id = Column(Integer, ForeignKey('User.user_id'), primary_key=True)
    prod_id = Column(Integer, ForeignKey('Product.prod_id'), primary_key=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class ChatSystem(db.Model):
    __tablename__ = 'chat_system'

    message_id = Column(Integer, ForeignKey('Chat.message_id'), primary_key=True)
    sender_id = Column(Integer, ForeignKey('User.user_id'), primary_key=True)
    prod_id = Column(Integer, ForeignKey('Product.prod_id'), primary_key=True)
    

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}