from flask import Blueprint, render_template, request, jsonify, redirect
from flask_socketio import emit
from datetime import datetime
from .. import conn,socketio  # 여기서는 모듈 간의 의존성을 최소화합니다.
bp = Blueprint('chat', __name__, url_prefix='/main')
uid = "082d8640-9287-4284-9a73-47543b255309"


conn.tb_select("Assignment","작성자",uid,db_key)
conn.tb_select("Board","작성자",uid,db_key)
conn.tb_select("Classdata",db_key=db_key,today_only=True).count()
conn.tb_select("S_memo","작성자_ID",uid,db_key)


