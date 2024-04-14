import os
import yaml

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
# from flask_jwt_extended import JWTManager

from .auth import google_bp
from .models import db, login_manager

# from . import routes
# from . import seed
from . import seed2
from sqlalchemy import MetaData, Table
from sqlalchemy.sql import text

import sqlalchemy as sa
from sqlalchemy.ext import compiler
from sqlalchemy.schema import DDLElement
from sqlalchemy.sql import table

app = Flask(__name__)


CORS(app, resource={r"/*": {"origins": "*"}})


# Connection to the DB
conf = yaml.safe_load(open("server/config.yaml"))
mysql_host = conf["mysql_host"]
mysql_user = conf["mysql_user"]
mysql_password = conf["mysql_password"]
mysql_db = conf["mysql_db"]
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
)

app.config["SQLALCHEMY_POOL_SIZE"] = 100
app.config["Access-Control-Allow-Origin"] = "*"
app.config["Access-Control-Allow-Headers"] = "Content-Type"

# Google OAuth
load_dotenv()
GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
app.config["GOOGLE_OAUTH_CLIENT_ID"] = GOOGLE_OAUTH_CLIENT_ID
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = GOOGLE_OAUTH_CLIENT_SECRET
app.secret_key = "super secret key"


app.register_blueprint(google_bp, url_prefix="/login")
db.init_app(app)
# cors.init_app(app)
login_manager.init_app(app)


print(GOOGLE_OAUTH_CLIENT_ID)
print(GOOGLE_OAUTH_CLIENT_SECRET)


# App Login Functionality using JWT
# JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", None)
# if not JWT_SECRET_KEY:
#     JWT_SECRET_KEY = "".join(random.choice(string.ascii_lowercase) for i in range(32))
# app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
# jwt = JWTManager(app)


# Define a custom DDLElement for CREATE VIEW
class CreateView(DDLElement):
    def __init__(self, name, query):
        self.name = name
        self.query = query

# Compiler for CREATE VIEW
@compiler.compiles(CreateView)
def _create_view(element, compiler, **kw):
    return f"CREATE VIEW {element.name} AS {element.query}"


# Define a custom DDLElement for CREATE VIEW
class CreateView(DDLElement):
    def __init__(self, name, query):
        self.name = name
        self.query = query

# Compiler for CREATE VIEW
@compiler.compiles(CreateView)
def _create_view(element, compiler, **kw):
    return f"CREATE VIEW {element.name} AS {element.query}"

with app.app_context():
    from . import routes

    db.drop_all()  # drop the database (development only)
    db.create_all()  # create the database (development only)

    # seed the database (development only)
    # seed.seed_db()
    seed2.seed_db2()

    metadata = MetaData()
    metadata.bind = db.engine 

    view_query1 = """
    SELECT user_id, name, email
    FROM User;
    """

    view_query2 = """
    SELECT User.name, User.email, Product.prod_title
    FROM User JOIN listings JOIN Product;
    """

    # # Create the view in the database
    with db.engine.connect() as conn:

        conn.execute(text("DROP VIEW IF EXISTS admin_view_user"))
        conn.execute(CreateView('admin_view_user', view_query1))
        conn.execute(text(f"GRANT SELECT ON admin_view_user TO '{mysql_user}'@'{mysql_host}';"))

        conn.execute(text("DROP VIEW IF EXISTS admin_view_prod"))
        conn.execute(CreateView('admin_view_prod', view_query2))
        conn.execute(text(f"GRANT SELECT ON admin_view_prod TO '{mysql_user}'@'{mysql_host}';"))

    metadata.reflect(bind = db.engine, views = True)
