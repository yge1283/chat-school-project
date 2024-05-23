from flask import Blueprint, render_template, request, jsonify, redirect

bp = Blueprint('student_main', __name__, url_prefix='/student')


@bp.route('/')
def show_student_mainPage():
    return render_template('./Student_page/Chat_Up_Call_page/Chat_Up_Call.html')






