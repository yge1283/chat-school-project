from flask import Blueprint, render_template, request, jsonify, redirect
from flask_socketio import emit
from datetime import datetime
from .. import conn, socketio  # 여기서는 모듈 간의 의존성을 최소화합니다.

bp = Blueprint('chat', __name__, url_prefix='/chat')
uid = ""

@bp.route('/')
def show_chatbot_page():
    # return render_template('./Student_page/Chatbot_Or_Communication_Page/Chatbot_or_communication_page.html')
    return render_template("./Student_page/1.html")

@socketio.on('connect', namespace='/')
def handle_message(data):
    uid = data['uuid']
    board = data['board']
    db = conn.convert_to_list(conn.tb_select("Chatbot", "학생_ID", uid, board))
    emit('sucsess', db, room=request.sid)

@socketio.on('chat', namespace='/chat')
def post_message(data):
    message = data['msg']
    nowdate = datetime.now()
    conn.tb_ninsert("Chat", [(1, uid, nowdate, message, "")])