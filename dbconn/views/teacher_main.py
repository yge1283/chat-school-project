from flask import Blueprint, render_template, request, jsonify, redirect,session
from .supabase_client import supabase
import os

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






# 허용된 확장자 목록
def is_extension_allowed(filepath):
  allowed_extensions = {'.txt', '.pdf'}
  _, ext = os.path.splitext(filepath)
  return ext in allowed_extensions

# 선생님.py에만 있는 업로드 파일 기능
@bp.route('/send_upload', methods=['POST'])
def teacher_upload_files():
    files = request.files.getlist('files')
    dashboard_key = session.get('dashboard_key') # 과목 코드 (get)
    bucket_name = "fine"   # 버킷 이름 = 일단 'fine'으로 저장

    responses = []
    for file in files:
        filename = file.filename
        if not is_extension_allowed(filename):
            print(f"Upload failed: {filename} has an unsupported file extension.")
            return jsonify({'error': f'Unsupported file extension: {filename}'}), 400

        path_on_supastorage = f"subject/{dashboard_key}/{filename}" # Supabase 내 저장 경로 지정

        response = supabase.storage.from_(bucket_name).upload(path_on_supastorage, file.read())
        responses.append({'filename': filename, 'status_code': response.status_code})

    success = all(res['status_code'] == 200 for res in responses)
    return jsonify({'success': success, 'responses': responses}), 200 if success else 500



# student.py 랑 똑같이 과목정보랑 메인정보 가져오는 코드
# 1. supabase 작동 되는지 확인하는 코드
@bp.route('/create_table')
def teacher_create_table_page():
    try:
        supanova = supabase.auth.get_user()
        print(f"수파베이스는 괜찮은가요?: {supanova}")
        print(f"학생쪽 세션은 괜찮은가요?: {session['user']}")
        result = supabase.table('confirm').insert({"나라": "일본", "수도": "도쿄"}).execute()
        data = result.data
        if data:
            print("데이터가 있습니다.")
            print(f"data: {data}")
            return jsonify({'success': True, 'data': data}), 201
        else:
            return jsonify({'error': 'Failed to create table'}), 400
    except Exception as e:
        print(f"Error inserting into table: {e}")
        return jsonify({'error': 'Failed to create table'}), 500
    

# get_keys값
def teacher_get_dashboard_key(uid):
    temp = supabase.table('대시보드').select("대시보드_key").eq('담당선생_ID', uid).execute()
    keys= [item['대시보드_key'] for item in temp.data]
    return keys

# 2. 과목정보 본인것만 가져오기
@bp.route('/get_my_courses')
def teacher_get_course_data():
    try:
        # 과목정보를 다시 불러온 경우(대시보드 페이지인경우)
        session['dashboard_key'] = None
        uid = session['user']['uid']
        # 함수 값 불러오기
        keys = teacher_get_dashboard_key(uid)
        response = supabase.table('대시보드').select('*, 선생(선생이름)').execute()
        courses = [item for item in response.data if item['대시보드_key'] in keys]
        if courses:
            print("데이터가 있습니다.")
            print(f"data: {courses}")
            return jsonify({'success': True, 'data': courses}), 201
        else:
            return jsonify({'error': 'Failed to create table'}), 400
    except Exception as e:
        print(f"Error inserting into table: {e}")
        return jsonify({'error': 'Failed to create table'}), 500

#대시보드 선택한 JS값(대시보드 key 1개)에 MAIN에 정보 가져오기
@bp.route('/get_mainboard', methods=['POST'])
def teacher_get_mainboard():
    # 메인 페이지에서 필요한 데이터 : 질문게시판의 내용, 과제 내용, 학생 메모장
    # 메인 페이지의 하위페이지 - 질문게시판, 과제게시판 등등
    # 하위에서 필요한 데이터 : 질문게시판 - 댓글[게시물_ID] , 과제게시판 - 과제제출[과제_ID]
    try:
        data = request.get_json()
        dashboard_key = str(data['key'])
        # 세션에 대시보드 key 값을 저장했을 경우 (항상 1개의 키값만 저장되어있음.)
        session['dashboard_key'] = dashboard_key

        # 1. 질문 게시판 내용
        response1 = supabase.table('게시판').select('*, 학생(학생이름)').eq('대시보드_key', dashboard_key).execute()
        question_data = response1.data if response1.data else []
        print(f"게시판: {question_data}")
        # 2. 과제 내용
        response2 = supabase.table('과제').select('*').eq('대시보드_key', dashboard_key).execute()
        homework_data = response2.data if response2.data else []
        print(f"과제: {homework_data}")
        # 3. 선생 메모장 내용
        uid = session['user']['uid']
        response3 = supabase.table('선생_메모장').select('*,선생(선생이름)').eq('작성자_ID', uid).execute()
        memo_data = response3.data if response3.data else []
        print(f"학생 메모장 내용: {memo_data}")
        # 4. 오늘 업로드 된 파일이 있는지 확인 (선생님이 업로드함)
        path_to_list = f"subject/{dashboard_key}"
        print(f"대시보드 키값: {path_to_list}")
        response4 = supabase.storage.from_("fine").list(path=path_to_list)
        # 파일 이름 추출
        file_name = [select['name'] for select in response4 if 'name' in select]
        print(f"파일이름: {file_name}")
        return jsonify({
            'success': True,
            'question_data': question_data,
            'homework_data': homework_data,
            'memo_data': memo_data,
            'file_name': file_name
        }), 201
    except Exception as e:
        print(f"Error retrieving mainboard data: {e}")
        return jsonify({'error': 'Failed to retrieve mainboard data'}), 500