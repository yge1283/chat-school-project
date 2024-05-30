from flask import Blueprint, render_template, request, jsonify, redirect

bp = Blueprint('chatbot', __name__, url_prefix='/edu_student')


@bp.route('/')
def show_chatbot_page():
    return render_template('./Student_page/Chatbot_Or_Communication_Page/Chatbot_or_communication_page.html')

