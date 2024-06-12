from flask import Blueprint, render_template, request, jsonify, redirect ,session
from .supabase_client import supabase
bp = Blueprint('student_main', __name__, url_prefix='/student')
from .. import conn, socketio 
from flask_socketio import emit
{"제목":1,"내용":"내용"}

#필요한 데이터 게시물 추가, 
#
