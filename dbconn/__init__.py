from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .connect import Connector
from flask_migrate import Migrate
from .connect import Connector
from flask_socketio import SocketIO
db_uri = Connector.read_config(section='postgres')
conn = Connector(db_uri)
socketio = SocketIO()
def create_app():
    app = Flask(__name__)
    # read_config 함수를 호출하여 데이터베이스 URI를 가져옴
    db_uri = Connector.read_config(section='postgres')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy()
    migrate = Migrate()
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    from .views import student_main, chatbot
    # app.register_blueprint(login.bp)
    # views에 Blueprint 만든 후 꼭 연결해주기!!!!!!!!!!!!!!!!
     

    app.register_blueprint(student_main.bp)
    app.register_blueprint(chatbot.bp)
    return app

"""
블루프린트 연결 가이드
1. from .views import ~ 에서 본인이 만든 views폴더안 .py파일의 이름을 추가해 주세요.
2. 다음 줄에 app.register_blueprint(<본인이선언한 bp함수명>.bp)
     본인이 선언한 bp이름은 views폴더안에 본인이 작업하는(만든)파일 들어가서
      예시로 bp = Blueprint('chatbot', __name__, url_prefix='/edu_chatbot')
                            ^^^^^^^
                            이 이름을 적어주세요.
                            헷갈리지 않을려면 .py파일이름과 같게 하셔도 됨

"""
