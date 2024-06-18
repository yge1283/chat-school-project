from flask import Blueprint, render_template, request, jsonify, redirect, session
from flask_socketio import emit
from datetime import datetime
from .. import conn, socketio  # 여기서는 모듈 간의 의존성을 최소화합니다.
from .. ai_server_config import AI_SERVER_URL # config.py에 저장된 ai 서버 주소 가져옴

bp = Blueprint('chatbot', __name__, url_prefix='/edu_chatbot')


@bp.route('/choice_file')
def show_chatbot_page():
    return render_template('./Student_page/Chatbot_choice_page/chatbot_choice_page.html')

@bp.route('/daily_chatbot')
def show_daily_chat_page():
    return render_template('./Student_page/Chatbot_Or_Communication_Page/Chatbot_communication_page_emotion.html')

@bp.route('/submit_doc_to_chatbot')
def submit_doc_to_chatbot():
    return render_template('Student_page/Chatbot_Or_Communication_Page/Chatbot_or_communication_page.html')

@socketio.on('first_connect', namespace='/chatbot')
def connect():
    print('Client chatbot connected')
    emit('get_url',AI_SERVER_URL)
    uid="082d8640-9287-4284-9a73-47543b255309"
    if 'user' in session:
        uid = session['user']['uid']
    else:
        print('User not found in session')
    data=conn.tb_select('Chat','학생_ID',uid)
    print(data)
    emit('chatting',data)
    emit('connect',uid)



@socketio.on('message',namespace='/chatbot')
def send_message(data):
    uid = ""
    if 'user' in session:
        uid = session['user']['uid']
    else:
        print('User not found in session')
    if uid:
        message = data['msg']
        nowdate = datetime.now()
        aimessage=data['ai']
        conn.tb_ninsert("Chat",  [(1, uid, nowdate, message, aimessage)])
        emit('message_sent', {'status': 'success'}, room=request.sid)
    else:
        emit('error', {'message': 'User not logged in'}, room=request.sid)
    

    
