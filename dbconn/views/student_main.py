from flask import Blueprint, render_template, request, jsonify, redirect

bp = Blueprint('main', __name__, url_prefix='/student_main')


@app.route('/<page_name>')
def page(page_name):
    return render_template(f'{page_name}.html')


