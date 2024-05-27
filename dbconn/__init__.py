# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from .connect import Connector
app = Flask(__name__)
socketio = SocketIO(app)

def create_app():

    app = Flask(__name__)
    
    # 데이터베이스 설정
    db_uri = Connector.read_config(section='postgres')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # 데이터베이스 및 마이그레이션 초기화
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    
    # 블루프린트 및 SocketIO 초기화
    from .views import student_main, chat
    app.register_blueprint(student_main.bp)
    app.register_blueprint(chat.bp)
    socketio.init_app(app)
    
    return app
