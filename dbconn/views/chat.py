from flask import Blueprint, render_template, request, jsonify, redirect, session
from flask_socketio import emit
from datetime import datetime
from .. import conn, socketio  # 여기서는 모듈 간의 의존성을 최소화합니다.

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('/')
def show_chatbot_page():
    return render_template('./Student_page/Chatbot_Or_Communication_Page/Chatbot_or_communication_page.html')
    # return render_template("./Student_page/1.html")

@socketio.on('connect', namespace='/')
def handle_connect():
    uid = session.get('user', {}).get('uid')
    if uid:
        # 클라이언트로부터 추가 데이터를 받아와야 한다고 가정
        board = request.args.get('board', 'default_board')  # 예시로 'board' 파라미터 사용
        db = conn.convert_to_list(conn.tb_select("Chatbot", "학생_ID", uid, board))
        emit('success', db, room=request.sid)
    else:
        emit('error', {'message': 'User not logged in'}, room=request.sid)

@socketio.on('chat', namespace='/chat')
def post_message(data):
    uid = session.get('user', {}).get('uid')
    if uid:
        message = data['msg']
        nowdate = datetime.now()
        new_chat = [(1, uid, nowdate, message, "")]
        conn.tb_ninsert("Chat", new_chat)
        emit('message_sent', {'status': 'success'}, room=request.sid)
    else:
        emit('error', {'message': 'User not logged in'}, room=request.sid)


# http://127.0.0.1:5000/chat/
# 위 코드로 접속시 send할 경우 보내는 짐
#기존 html 선행 조건: 본인 uid를 받는다는 전재로 작동됨, 추가 설치(flask_socketio)