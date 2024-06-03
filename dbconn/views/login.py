from flask import Blueprint, render_template, request, jsonify, redirect,session
import asyncio
from supabase import create_client, Client
from .. import config  # dbconn 폴더의 config 파일 불러오기

url = config.SUPABASE_URL
key = config.SUPABASE_KEY
supabase: Client = create_client(url, key)

bp = Blueprint('main', __name__, url_prefix='/login') # /login 페이지 설정



@bp.route('/')
def index():
    return render_template('./login/Login_page.html') # 첫 로그인 페이지 화면

@bp.route('/signup')
def signup():
    return render_template('login/SignUp_page.html') # 회원가입 html 페이지 표시

@bp.route('/findIDandPW')
def findidandpw():
    return render_template('login/Find_ID_and_PW.html') # id, pw찾기 페이지 표시

@bp.route('/signin')
def signin():
    #로그인 정보 받는 코드 {딕셔너리}(json)
    #형식 {"email":"", "password": "", "teacher":""}
    # "teacher"의 값은 True or False
    recieve_info = request.form

    #로그인 정보 확인하는 코드
    #로그인 정보가 DB에 없으면 'login_fail' 반환
    #로그인 정보가 있으면 'main page' html 표시 

# 로그인- 이메일, 구글 (예정)
# 이메일로 로그인
@bp.route('', methods=['POST'])
def login():
    try:
        # 데이터를 클라이언트에서 받아옴
        data = request.get_json()
        email = data['email']
        password = data['password']
        print(f"Logging in with email: {email}")

        # supabase로 로그인을 함
        result = supabase.auth.sign_in_with_password({"email": email, "password": password})

        # uid값을 저장안해도, userinfo에서 자기 UID에 맞는 행만 선택됨 굳이?
        uid = result.user.id
        avr = result.user.user_metadata['avatar_url']
        print(f'uid: {uid}')

        if uid:
            # 선생인지 조회
            userinfo = supabase.table('userinfo').select('IsT, user_name').execute()
            value = userinfo.data[0]['IsT'] if userinfo.data else None
            name = userinfo.data[0]['user_name'] if userinfo.data else None
            print(f'teacher: {value}, {type(value)}')

            role = 'teacher' if value else 'student'
            redirect_url = "/login/teacher/dashboard_page" if value else "/login/student/dashboard_page"

            # 세션에 사용자 정보를 저장합니다.
            session['user'] = {
                'uid': uid,
                'email': email,
                'role': role,
                'avr_url' : avr,
                'name' : name
            }
            session['role'] = role

            print(f'현재 세선상태: {session}')
            return jsonify({
                "isSuccess": True,
                "message": "Login successful",
                "uid": uid,
                "session": {"role": role},
                "redirect_url": redirect_url
            })
            
        else:
            return jsonify({
                "isSuccess": False,
            }), 401
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({
            "isSuccess": False,
            "message": "이메일 또는 비밀번호 오류",
            "error": str(e)
        }), 500
        
# 구글로 로그인(보류중) -작동확인 완료
@bp.route('/login-google', methods=['GET'])
def signin_with_google():
    try:
        res = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": f"{request.host_url}login/callback"  # 수정된 부분
            }
        })
        return jsonify({"redirect_url": res.url})
    except Exception as e:
        print(f"Error during Google sign-in: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route('/callback')
def oauth_callback():
    try:
        # OAuth 인증 후 사용자를 확인
        session = supabase.auth.get_session()
        print(f'구글 세션 {session}')
        uid = session.user.id
        print(f'uid: {uid}')

        if uid:
            userinfo = supabase.table('userinfo').select('IsT').eq('user_id', uid).execute()
            value = userinfo.data[0]['IsT'] if userinfo.data else None
            print(f'teacher: {value}, {type(value)}')

            role = 'teacher' if value else 'student'
            redirect_url = "/login/teacher/dashboard_page" if value else "/login/student/dashboard_page"

            if value is None:
                # IsT 값이 없으면
                my_url = "/login/teacher/my_page" if role == 'teacher' else "/login/student/my_page"
                return jsonify({
                    "isSuccess": False,
                    "message": "Login failed",
                    "redirect_url": my_url
                })

            return jsonify({
                "isSuccess": True,
                "message": "Login successful",
                "uid": uid,
                "session": {"role": role},
                "redirect_url": redirect_url
            })
        else:
            return jsonify({
                "isSuccess": False,
                "message": "Login failed",
                "redirect_url": my_url
            })

    except Exception as e:
        print(f"Error during OAuth callback: {e}")
        return jsonify({'error': str(e)}), 500





# 로그아웃
@bp.route('/logout', methods=['POST'])
def logout():
    user = session.get('user')
    if not user:
        return jsonify({'error': 'No active session'}), 400
    else:
        result = supabase.auth.sign_out()
        print(f'sign_out result: {result}')  # 디버깅을 위한 로그 추가

    if result is None:
        print(f"supabase.auth.sign_out()가 None을 반환했습니다.")
        session.pop('user', None)
        return jsonify({'message': 'Logged out successfully'}), 200
    else:
        return jsonify({'error': result['error']}), 401


# 대시보드 페이지 올라오면 >> 로그인 후 dashboard로 이동
@bp.route('/teacher/dashboard_page')
def teacher_main_page():
    return render_template('./Teacher_page/Teacher_Page_Main_Frame.html')

@bp.route('/student/dashboard_page')
def student_main_page():
    return render_template('./Student_page/Main_page/Main_page.html')


# 회원가입 2순위로 미룰예정


