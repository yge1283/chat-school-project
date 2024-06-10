from flask import Blueprint, render_template, request, jsonify, redirect

bp = Blueprint('teacher_main', __name__, url_prefix='/teacher')


@bp.route('/')
def show_teacher_DashboardPage():
    return render_template('./Teacher_page/Teacher_Main_page/Teacher_Main_page_Dashboard.html')

# 과제 게시판 페이지를 위한 라우트 추가
@bp.route('/homeworkpage')
def show_teacher_homeworkPage():
    return render_template('./Teacher_page/Teacher_Homework_page/Teacher_Homework_Main_Page.html')

# 과제 게시판 페이지를 위한 라우트 추가
@bp.route('/makeHomeworkWithAIpage')
def show_teacher_homeworkMakeWithAIPage():
    return render_template('./Teacher_page/Teacher_Homework_page/Teacher_Homework_Make_with_AI.html')

@bp.route('/questionpage')
def show_teacher_questionPage():
    return render_template('./Teacher_page/Teacher_Question_page/Teacher_Question_board_Main_page.html')

@bp.route('/questionAnswerpage')
def show_teacher_questionAnswerPage():
    return render_template('./Teacher_page/Teacher_Question_page/Teacher_Question_board_writing_section.html')

@bp.route('/homeworkEditpage')
def show_teacher_homeworkEditPage():
    return render_template('./Teacher_page/Teacher_Homework_page/Teacher_Homework_Edit_Page.html')

@bp.route('/memopage')
def show_teacher_memoPage():
    return render_template('./Teacher_page/Teacher_Memo_page/Teacher_Memo_check_Page.html')

@bp.route('/MemoEditpage')
def show_teacher_memoEditPage():
    return render_template('./Teacher_page/Teacher_Memo_page/Teacher_Memo_edit_page.html')

@bp.route('/teachermainpage')
def show_teacher_mainPage():
    return render_template('./Teacher_page/Teacher_Main_page/Teacher_Main_page.html')

# 6.10일 추가(양지은): 생성한 AI문제 표시 페이지 라우터 추가
@bp.route('/teacheraiproblemview')
def show_teacher_aiproblemview():
    return render_template('./Teacher_page/Teacher_AI_View_page.html')

# 6.10일 추가(양지은): AI문제를 만들기 위한 파일 업로드 페이지 라우터 추가
@bp.route('/teacherfileupload')
def show_teacher_fileupload():
    return render_template('./Teacher_page/Teacher_File_Upload_page.html')





