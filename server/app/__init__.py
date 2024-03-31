from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists
import yaml
from flasgger import Swagger


login_manager = LoginManager()
db = SQLAlchemy()
cors = CORS()

app = Flask(__name__)
conf = yaml.safe_load(open('config.yaml'))
mysql_host = conf['mysql_host']
mysql_user = conf['mysql_user']
mysql_password = conf['mysql_password']
mysql_db = conf['mysql_db']
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
app.config['SECRET_KEY'] = 'veryobviouslysecret' # TODO: Change this to something more secure

swagger = Swagger(app)
db.init_app(app)
cors.init_app(app)
login_manager.init_app(app)

from . import routes
from . import models
from . import auth

with app.app_context():
    # drop the database (development only)
    db.drop_all()

    # create the database (development only)
    db.create_all()

    # seed the database (development only)
    from . import seed

    seed.seed_db()
