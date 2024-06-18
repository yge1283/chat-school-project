from flask import Blueprint, render_template, request, jsonify, redirect ,session, url_for, current_app
from .supabase_client import supabase
bp = Blueprint('student_main', __name__, url_prefix='/student')
from .. import conn, socketio 
from flask_socketio import emit


"""
bp선언시 위와 같이 작성
예시)  bp = Blueprint('student_main', __name__, url_prefix='/student')
                      ^^^^^^^^^^^^^                        ^^^^^^^^^^
                      __init__.py에 쓸 bp함수명             url 접두사:
                                                         이 파일에 쓰이는 모든 api는
                                                         /student/~
                                                         하위 경로로 작동함.
"""



@bp.route('/') #최상위 경로
def chat_up_call():
    # 해당 학생의 시간표 정보 전송 코드
    return render_template('./Student_page/Chat_Up_Call_page/Chat_Up_Call.html')
    #해당 학생의 시간표 페이지 표시
"""
@bp.route('/')
'/'는 위 접두사에 이은 최상위 경를 나타냄
예) https://127.0.0.1:5000/student/ 로 접속시 
def show_student_mainPage() 함수 실행.  # 함수명 복붙하고 그대로 사용하지말고 수정해서 사용하기!!!!!!!!!!!

위 함수의 경우 render_template으로 html을 반환해주는 기능.(위 url접속시 html페이지가 표시됨)
"""

# 대시보드에서 과목을 눌렀을때 메인페이지로 이동
@bp.route('/get_key', methods=['POST'])
def student_get_1dashboard():
    data = request.get_json()
    dashboard_key = str(data['key'])
    session['dashboard_key'] = dashboard_key
    return jsonify({'success': True}), 201

@bp.route('/main')
def student_main_page():
    return render_template('./Student_page/Main_page/Main_page.html')

@socketio.on('request_main_data')
def handle_main_data_request(data):
    # user = session['user']
    # board = session['board']
    # uid = user['uid']
    # key = board['key']  # Assuming 'key' is the key to access board ID
    uid="082d8640-9287-4284-9a73-47543b255309"
    key=1
    assignment_data = conn.tb_select("Assignment", key)
    board_data = conn.tb_get("Board", "작성자", uid, dashboard_key=key)
    class_data_list = conn.tb_select("Classdata", db_key=key, today_only=True)
    class_data_count = len(class_data_list)  # 리스트의 길이로 카운트
    memo_data = conn.me_get("S_memo", uid)

    emit('assignment_data', assignment_data)
    emit('board_data', board_data)
    emit('class_data_count', class_data_count)
    emit('memo_data', memo_data)


"""
@bp.route('/')
'/'는 위 접두사에 이은 최상위 경를 나타냄
예) https://127.0.0.1:5000/student/ 로 접속시 
def show_student_mainPage() 함수 실행.  # 함수명 복붙하고 그대로 사용하지말고 수정해서 사용하기!!!!!!!!!!!

@bp.route('/question')
def question():
    return render_template('./Student_page/Student_question_board_detail/Student_question_board_detail.html')

"""

# 1. supabase 작동 되는지 확인하는 코드
@bp.route('/create_table')
def student_create_table_page():
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
def student_get_dashboard_key(uid):
    temp = supabase.table('수강생').select("대시보드_key").eq('학생_ID', uid).execute()
    keys= [item['대시보드_key'] for item in temp.data]
    return keys

# 2. 과목정보 본인것만 가져오기
@bp.route('/get_my_courses')
def student_get_course_data():
    try:
        # 과목정보를 다시 불러온 경우(대시보드 페이지인경우)
        session['dashboard_key'] = None
        uid = session['user']['uid']
        # 함수 값 불러오기
        keys = student_get_dashboard_key(uid)
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
@bp.route('/get_mainboard')
def student_get_mainboard():
    dashboard_key = session['dashboard_key']
    print(f"현재 과목 코드 : {dashboard_key}")
    # 메인 페이지에서 필요한 데이터 : 질문게시판의 내용, 과제 내용, 학생 메모장
    # 메인 페이지의 하위페이지 - 질문게시판, 과제게시판 등등
    # 하위에서 필요한 데이터 : 질문게시판 - 댓글[게시물_ID] , 과제게시판 - 과제제출[과제_ID]
    try:
        # 1. 질문 게시판 내용
        response1 = supabase.table('게시판').select('*, 학생(학생이름)').eq('대시보드_key', dashboard_key).execute()
        question_data = response1.data if response1.data else []
        print(f"게시판: {question_data}")
        # 2. 과제 내용
        response2 = supabase.table('과제').select('*').eq('대시보드_key', dashboard_key).execute()
        homework_data = response2.data if response2.data else []
        print(f"과제: {homework_data}")
        # 3. 학생 메모장 내용
        uid = session['user']['uid']
        response3 = supabase.table('학생_메모장').select('*,학생(학생이름)').eq('작성자_ID', uid).execute()
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


@bp.route('/question')
def question():
    return render_template('./Student_page/Student_question_board_detail/Student_question_board_detail.html')
@socketio.on('connect', namespace='/question')
def question_start():
    # 기본값 설정
    dashboard_key = 1
    # 세션에 'dashboard_key'가 있는지 확인
    if 'dashboard_key' in session:
        dashboard_key = session['dashboard_key']
        emit('success')
    else:
        emit('error', {'message': 'dashboard_key not found in session'})
    
    # dashboard_key 출력
    print(dashboard_key)
    
    # conn.bd_select 메서드 호출
    try:
        result = conn.bd_select(db_key=dashboard_key,page=0)
        print(result)
        emit('board', result)
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('board', namespace='/question')
def question_page(data):
    dashboard_key=1
    if 'dashboard_key' in session:
        dashboard_key = session['dashboard_key']
        
        emit('success')
    else:
        emit('error', {'message': 'dashboard_key not found in session'})
    print(data)
    result = conn.bd_select(db_key=dashboard_key, desc=True,page=data)
    emit('board', result)

@socketio.on('question', namespace='/question')
def qes_com_get(data):
    bd_id=int(data)
    emit('question',conn.tb_select("Board","게시물_ID",bd_id))

@socketio.on('comment', namespace='/question')
def qes_com_get(data):
    bd_id=int(data)
    emit('comment',conn.tb_select("Comment","게시물_ID",bd_id))
    
@socketio.on('comment_num', namespace='/question')
def qes_com_get(data):
    bd_id = int(data)
    try:
        comment_count = conn.tb_len("Comment", "게시물_ID", bd_id)
        print(comment_count)
        emit('comment_num', {'게시물_ID': bd_id, 'comment_count': comment_count})
    except Exception as e:
        emit('error', {'message': str(e)})

    

# 질문게시판 가져오기
@bp.route('/get_questions', methods=['GET'])
def student_get_questions():
    try:
        dashboard_key = session.get('dashboard_key')
        if not dashboard_key:
            return jsonify({'error': 'No dashboard key in session'}), 400

        response = supabase.table('게시판').select('*, 학생(학생이름)').eq('대시보드_key', dashboard_key).execute()
        question_data = response.data

        return jsonify({'success': True, 'data': question_data}), 200
    except Exception as e:
        print(f"Error retrieving questions data: {e}")
        return jsonify({'error': 'Failed to retrieve questions data'}), 500

# 과제 가져오기
@bp.route('/get_homeworks', methods=['GET'])
def student_get_homeworks():
    try:
        dashboard_key = session.get('dashboard_key')
        if not dashboard_key:
            return jsonify({'error': 'No dashboard key in session'}), 400

        response = supabase.table('과제').select('*').eq('대시보드_key', dashboard_key).execute()
        homework_data = response.data

        return jsonify({'success': True, 'data': homework_data}), 200
    except Exception as e:
        print(f"Error retrieving homeworks data: {e}")
        return jsonify({'error': 'Failed to retrieve homeworks data'}), 500

# 댓글 가져오기
@bp.route('/get_comments', methods=['POST'])
def student_get_comments():
    try:
        data = request.get_json()
        question_id = data['question_id']
        
        response = supabase.table('댓글').select('*').eq('게시물_ID', question_id).execute()
        comments_data = response.data

        return jsonify({'success': True, 'data': comments_data}), 200
    except Exception as e:
        print(f"Error retrieving comments data: {e}")
        return jsonify({'error': 'Failed to retrieve comments data'}), 500

# 제출물 가져오기
@bp.route('/get_submissions', methods=['POST'])
def student_get_submissions():
    try:
        data = request.get_json()
        homework_id = data['homework_id']
        
        response = supabase.table('과제제출').select('*').eq('과제_ID', homework_id).execute()
        submissions_data = response.data

        return jsonify({'success': True, 'data': submissions_data}), 200
    except Exception as e:
        print(f"Error retrieving submissions data: {e}")
        return jsonify({'error': 'Failed to retrieve submissions data'}), 500



# 수강생 데이터에다가 '과목코드'입력해서 넣기 
@bp.route('/insert_key', methods=['POST'])
def student_insert_dashboard_key():
    # JS에서 학생이 추가할 대시보드 키값 받아오기
    get_data = request.get_json()
    dashboard_key = get_data['key']
    # 수강중인 과목인지 확인하기
    uid = session['user']['uid']
    keys = student_get_dashboard_key(uid)
    if dashboard_key in keys:
        return jsonify({'error': '이미 수강중인 과목입니다.'})
    try:
        # 정상적으로 코랩에서는 작동
        result = supabase.table('수강생').insert({"대시보드_key": dashboard_key, "학생_ID": uid}).execute()
        data = result.data
        if data:
            print(f"data: {data}")
            return jsonify({'success': True, 'data': data}), 201
        else:
            return jsonify({'error': 'Failed to create table'}), 400
    except Exception as e:
        print(f"Error inserting into table: {e}")
        return jsonify({'error': 'Failed to create table'}), 500
    

# x 버튼 누르면 자동으로 키값 받고, 수강생 데이터 행 삭제
@bp.route('/delete_key', methods=['POST'])
def student_delete_dashboard_key():
    # JS에서 학생이 추가할 대시보드 키값 받아오기
    get_data = request.get_json()
    key = get_data['key']
    dashboard_key = int(key) # int로 고쳐야함
    # 수강 중인 key 가 맞는 경우
    print(f"대시보드키값 받아왔나요? {dashboard_key} , {type(dashboard_key)}")
    uid = session['user']['uid']
    keys = student_get_dashboard_key(uid)
    if dashboard_key in keys:
        try:
            print(f"실행중인가요?")
            # 수강생 테이블에서 해당 행 삭제
            result = supabase.table('수강생').delete().match({"대시보드_key": dashboard_key, "학생_ID": uid}).execute()
            data = result.data
            print(f"제대로 삭제 되었나요?")
            if data:
                print(f"Deleted data: {data}")
                return jsonify({'success': True, 'data': data}), 200
            else:
                return jsonify({'error': 'Failed to delete entry'}), 400
        except Exception as e:
            print(f"Error deleting from table: {e}")
            return jsonify({'error': 'Failed to delete entry'}), 500
    else:
        return jsonify({'error': '수강중인 과목이 아닙니다.'}), 400

@bp.route('/comment')
def comment():
    return render_template('./Student_page/Student_question_board_detail/전문1.html')

# @bp.route('/<subject_id>') #클라이언트에게 받을 변수'subject_id'를 url로 지정
# def show_subject_page():
#     #학생정보 불러와 해당 과목{subject_id}의 정보 전송
#     return render_template('./Student_page/Main_page/Main_page.html')

@bp.route('/submit') #교육용 챗봇 누를 때
def submit():
    with current_app.app_context():
        return redirect(url_for('chatbot.show_chatbot_page')) # chatbot.py 블루프린트 모델로 이동
    
@bp.route('/daily_chat') #심리상담 챗봇 누를 때
def go_daily_chat_page():
    with current_app.app_context():
        return redirect(url_for('chatbot.show_daily_chat_page')) # chatbot.py 블루프린트 모델로 이동
"""
클라이언트 쪽에서 https://127.0.0.1:5000/student/korean으로 접속하여 
    {"uuid":"OAQMNCd2D76DCbx34MK"}를 받아왔다면
    서버에서 url의 변수 'korean'과 'uuid'를 사용하여
    학생이 수강하고 있는 korean 과목에 대한 정보를 찾아 전송.
"""






# 질문게시판 6.11일 추가 (양지은)
@bp.route('/studentquestion')
def show_student_questionmain():
    return render_template('./Student_page/Student_question_board_detail/Student_question_board_detail.html')

# 질문게시판 글쓰기 페이지 이동
@bp.route('/studentquestionwriting')
def show_student_question_writing():
    return render_template('Student_page/Student_question_board_detail/Student_question_board_detail.html')


# 과제 6.11일 추가 (양지은)
@bp.route('/studenthomework')
def show_student_homeworkmain():
    return render_template('Student_page/Student_homework_page/Student_Homework_Main_page.html')

# 과제글쓰기 6.11일 추가 (양지은)
@bp.route('/studenthomeworkwriting')
def show_student_homework_writing():
    return render_template('Student_page/Student_homework_page/Student_Homework_Edit_Page.html')

#파일 다운로드 6.11일 추가 (양지은)
@bp.route('/studentfiledownload')
def show_student_filedownload():
    return render_template('Student_page/File_Download_page/File_download_page.html')
