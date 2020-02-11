from flask import Flask


from flask_sqlalchemy import SQLAlchemy
import os

app=Flask(__name__)
db=SQLAlchemy(app)

app.config.from_pyfile("config.py")


# from flaskblog.routes import *




from flaskblog.user  import userBlueprint
from flaskblog.articles import articleBlueprint
app.register_blueprint(userBlueprint,url_prefix="/users")

from flaskblog.models import *
app.register_blueprint(articleBlueprint)

# app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///test.db"
# app.config["SECRET_KEY"]="secret"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

# dwq