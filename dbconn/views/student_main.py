from flask import Blueprint, render_template, request, jsonify, redirect

bp = Blueprint('main', __name__, url_prefix='/student')


@bp.route('/')
def show_student_mainPage():
    return render_template('./Student_page/Main_page.html')






