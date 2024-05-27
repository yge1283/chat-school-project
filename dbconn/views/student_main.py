from flask import Blueprint, render_template, request, jsonify, redirect
from models import Dashboard, Timetable


"""
꼭 api정의서에 나와 있는데로 해주시고 변경사항 일을시 api정의서도 수정하기!
필요한 DB불러올때 models에서 필요한것만 불러와주세요. 
예시) from models import Dashboard, Timetable
                        ^^^^^^^^^^ ^^^^^^^^^^
                        여기에 필요한 테이블 추가
                        뭐가 있는지는 models.py 참고

"""



bp = Blueprint('student_main', __name__, url_prefix='/student')

"""
bp선언시 위와 같이 작성
예시)  bp = Blueprint('student_main', __name__, url_prefix='/student')
                      ^^^^^^^^^^^^^                        ^^^^^^^^^^
                      __init__.py에 쓸 bp함수명             url 접두사:
                                                         이 파일에 쓰이는 모든 api는
                                                         /student/~
                                                         하위 경로로 작동함.
"""



@bp.route('/') #최상위 경로
def show_student_mainPage():
    # 해당 학생의 시간표 정보 전송 코드
    return render_template('./Student_page/Chat_Up_Call_page/Chat_Up_Call.html')
    #해당 학생의 시간표 페이지 표시
"""
@bp.route('/')
'/'는 위 접두사에 이은 최상위 경를 나타냄
예) https://127.0.0.1:5000/student/ 로 접속시 
def show_student_mainPage() 함수 실행.  # 함수명 복붙하고 그대로 사용하지말고 수정해서 사용하기!!!!!!!!!!!

위 함수의 경우 render_template으로 html을 반환해주는 기능.(위 url접속시 html페이지가 표시됨)

"""

@bp.route('/<subject_id>') #클라이언트에게 받을 변수'subject_id'를 url로 지정
def show_subject_page():
    #학생정보 불러와 해당 과목{subject_id}의 정보 전송
    return render_template('./Student_page/Main_page/Main_page.html')

"""
@bp.route('/{subject_id}')
            ^^^^^^^^^^^
클라이언트(웹)쪽에서 지정된 변수를 받아 해당 값에 대한 특정 기능을 수행 할 수 있다.
예시) 여기서는 약속된 과목ID 'subject_id'를 받아와서 현재 로그인되어 있는 학생 uid와 과목id를 이용해
학생이 듣고 있는 해당 과목의 db정보를 불러와 특정과목 페이지와 함께 반환한다.

클라이언트 쪽에서 https://127.0.0.1:5000/student/korean으로 접속하여 
    {"uuid":"OAQMNCd2D76DCbx34MK"}를 받아왔다면
    서버에서 url의 변수 'korean'과 'uuid'를 사용하여
    학생이 수강하고 있는 korean 과목에 대한 정보를 찾아 전송.

"""