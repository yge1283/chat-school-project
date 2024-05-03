from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from connect import MySQLConnector
from flask_migrate import Migrate

app = Flask(__name__)
db_uri = MySQLConnector.read_config()  # read_config 함수를 호출하여 데이터베이스 URI를 가져옴
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db)