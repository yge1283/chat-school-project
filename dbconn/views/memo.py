from flask import Blueprint, render_template, request, jsonify, redirect ,session
from .supabase_client import supabase
bp = Blueprint('student_memo', __name__, url_prefix='/student/memo')
from .. import conn, socketio 
from flask_socketio import emit



