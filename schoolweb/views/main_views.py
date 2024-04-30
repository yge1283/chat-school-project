from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')  #url 첫페이지
def hello_pybo():
    return 'Hello, school!'

