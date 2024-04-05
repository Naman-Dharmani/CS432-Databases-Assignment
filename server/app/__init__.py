import os
import random
import string
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import yaml


app = Flask(__name__)

# Connection to the DB
conf = yaml.safe_load(open('server/config.yaml'))
mysql_host = conf['mysql_host']
mysql_user = conf['mysql_user']
mysql_password = conf['mysql_password']
mysql_db = conf['mysql_db']
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"

db = SQLAlchemy()
cors = CORS()

db.init_app(app)
cors.init_app(app)

# App Login Functionality
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", None)
if not JWT_SECRET_KEY:
    JWT_SECRET_KEY = ''.join(random.choice(
        string.ascii_lowercase) for i in range(32))
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
jwt = JWTManager(app)

with app.app_context():
    from . import auth
    from . import models
    from . import routes

    # drop the database (development only)
    db.drop_all()

    # create the database (development only)
    db.create_all()

    # seed the database (development only)
    from . import seed

    seed.seed_db()
