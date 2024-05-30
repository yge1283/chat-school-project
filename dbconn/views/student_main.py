from flask import Blueprint, render_template, request, jsonify, redirect
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
def chat_up_call():
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
@bp.route('/main')
def main():
    return render_template('./Student_page/Main_page/Main_page.html')

"""
@bp.route('/')
'/'는 위 접두사에 이은 최상위 경를 나타냄
예) https://127.0.0.1:5000/student/ 로 접속시 
def show_student_mainPage() 함수 실행.  # 함수명 복붙하고 그대로 사용하지말고 수정해서 사용하기!!!!!!!!!!!

@bp.route('/question')
def question():
    return render_template('./Student_page/Student_question_board_detail/Student_question_board_detail.html')

"""

@bp.route('/comment')
def comment():
    return render_template('./Student_page/Student_question_board_detail/전문1.html')

# @bp.route('/<subject_id>') #클라이언트에게 받을 변수'subject_id'를 url로 지정
# def show_subject_page():
#     #학생정보 불러와 해당 과목{subject_id}의 정보 전송
#     return render_template('./Student_page/Main_page/Main_page.html')

@bp.route('/submit')
def submit():
    return render_template('./Student_page/Chatbot_choice_page/chatbot_choice_page.html')
"""
클라이언트 쪽에서 https://127.0.0.1:5000/student/korean으로 접속하여 
    {"uuid":"OAQMNCd2D76DCbx34MK"}를 받아왔다면
    서버에서 url의 변수 'korean'과 'uuid'를 사용하여
    학생이 수강하고 있는 korean 과목에 대한 정보를 찾아 전송.
"""
@bp.route('/submit_doc_to_chatbot')
def submit_doc_to_chatbot():
    return render_template('Student_page/Chatbot_Or_Communication_Page/Chatbot_or_communication_page.html')

@bp.route('/submit_doc_to_chatbot')
def submit_doc_to_chatbot():
    return render_template('Student_page/Chatbot_Or_Communication_Page/Chatbot_or_communication_page.html')
"""
클라이언트 쪽에서 https://127.0.0.1:5000/student/korean으로 접속하여 
    {"uuid":"OAQMNCd2D76DCbx34MK"}를 받아왔다면
    서버에서 url의 변수 'korean'과 'uuid'를 사용하여
    학생이 수강하고 있는 korean 과목에 대한 정보를 찾아 전송.

"""