from flask import Blueprint, redirect,session, url_for, current_app

bp = Blueprint('initpage', __name__, url_prefix='/') # /login 페이지 설정

'''
최상위 경로 접속시

로그인 되어 있을 때 > 대시보드 페이지 이동
로그인 안되어 있을 때 > 로그인 페이지 이동
'''

@bp.route('/')
def is_signedIn():
    user = session.get('user')
    with current_app.app_context():
        if user:
            if session["user"]["role"] == 'student': # 로그인 유저 > 선생,학생 구분
                return redirect(url_for('main.student_main_page'))
            else: return redirect(url_for('main.teacher_main_page'))
        else:
            return redirect(url_for('main.index')) #로그인페이지 이동