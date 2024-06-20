from flask import Blueprint, render_template, request, jsonify, redirect,session,render_template_string, current_app, url_for
import asyncio
#from supabase import create_client, Client
#from .. import config  # dbconn 폴더의 config 파일 불러오기
import logging
from ..connect import Connector

logger = logging.getLogger(__name__)
from .supabase_client import supabase

#url = config.SUPABASE_URL
#key = config.SUPABASE_KEY
#supabase: Client = create_client(url, key)

bp = Blueprint('main', __name__, url_prefix='/login') # /login 페이지 설정



@bp.route('/')
def index():
    return render_template('./login/Login_page.html') # 첫 로그인 페이지 화면

# <a href="{{ url_for('main.signup') }}" 로 사용가능
@bp.route('/signup')
def signup():
    return render_template('./login/SignUp_page.html') # 회원가입 html 페이지 표시

@bp.route('/findIDandPW')
def findidandpw():
    return render_template('./login/Find_ID_and_PW.html') # id, pw찾기 페이지 표시


# 프로필 반환 코드
@bp.route('/profile', methods=['GET'])
def show_profile():
    user = session.get('user')
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not logged in"}), 401


# 어디다 넣을지 몰라서 쓰는 시간표 생성코드
colors = [
    "#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#A133FF",
    "#33FFF6", "#FF9633", "#8D33FF", "#33FFB5", "#FF3333"
]

# 데이터 가져와서 가공하는 코드
def process_timetable(data):
    processed_data = []
    color_index = 0

    for entry in data:
        subject = entry['과목명']
        schedule = entry['시간표'].split(',')

        # 순차적으로 색상을 할당
        color = colors[color_index % len(colors)]
        color_index += 1

        timetable = {
            "월": {},
            "화": {},
            "수": {},
            "목": {},
            "금": {}
        }

        for time in schedule:
            day = time[0]
            period = time[1]
            if day == '월':
                timetable['월'][f"{period}교시"] = subject
            elif day == '화':
                timetable['화'][f"{period}교시"] = subject
            elif day == '수':
                timetable['수'][f"{period}교시"] = subject
            elif day == '목':
                timetable['목'][f"{period}교시"] = subject
            elif day == '금':
                timetable['금'][f"{period}교시"] = subject
        
        processed_data.append({
            "과목명": subject,
            "색상": color,
            "시간표": timetable
        })
    
    return processed_data

# 색깔, 과목명, 시간표 반환 JSON
@bp.route('/dbapi/timetable', methods=['GET'])
def get_timetable():
    db_connector = Connector()  # Connector 클래스 인스턴스 생성
    data = db_connector.fetch_timetable_data()  # 인스턴스를 통해 메서드 호출
    processed_data = process_timetable(data)
    return jsonify(processed_data)

# 대시보드_key, 선생이름, 과목명 등등 반환
@bp.route('/dbapi/dashboard', methods=['GET'])
def get_dashboard():
    db_connector = Connector()  # Connector 클래스 인스턴스 생성
    data = db_connector.get_dashboard_infos()  # 인스턴스를 통해 메서드 호출
    return jsonify(data)



@bp.route('/signin')
def signin():
    #로그인 정보 받는 코드 {딕셔너리}(json)
    #형식 {"email":"", "password": "", "teacher":""}
    # "teacher"의 값은 True or False
    recieve_info = request.form

    #로그인 정보 확인하는 코드
    #로그인 정보가 DB에 없으면 'login_fail' 반환
    #로그인 정보가 있으면 'main page' html 표시 

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
            userinfo = supabase.table('userinfo').select('IsT, user_name').eq("user_id",uid).execute()
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
                "message": "이메일 또는 비밀번호 오류"
            }), 401
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({
            "isSuccess": False,
            "message": "이메일 또는 비밀번호 오류",
            "error": str(e)
        }), 500
        
        

# 작동완료 6.12
@bp.route('/login-google', methods=['GET'])
def signin_with_google():
    try:
        res = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": f"{request.host_url}login/callback"
            }
        })
        print(f'res값 : {res}')
        return jsonify({"redirect_url": res.url})
    except Exception as e:
        print(f"Error during Google sign-in: {e}")
        return jsonify({"error": str(e)}), 500
    
# 보류
@bp.route('/login-kakao', methods=['GET'])
def signin_with_kakao():
    try:
        res = supabase.auth.sign_in_with_oauth({
            "provider": "kakao",
            "options": {
                "redirect_to": f"{request.host_url}login/callback"
            }
        })
        print(f'res값 : {res}')
        return jsonify({"redirect_url": res.url})
    except Exception as e:
        print(f"Error during Kakao sign-in: {e}")
        return jsonify({"error": str(e)}), 500
    
@bp.route("/callback", methods=["GET", "POST"])
def oauth_callback():
    if request.method == "POST":
        try:
            data = request.json
            token = data.get("access_token")
            p_token = data.get("provider_token")
            r_token = data.get("refresh_token")

            print(f'토큰: {token}') 
            res = supabase.auth.get_user(token)
            User = res.user
            print(f'세션 교환 결과: {User}')
            uid = User.id
            print(f'uid: {uid}')

            if uid:
                userinfo = supabase.table('userinfo').select('IsT').eq('user_id', uid).execute()
                value = userinfo.data[0]['IsT'] if userinfo.data else None
                print(f'teacher: {value}, {type(value)}')
                
                # 세션에 사용자 정보를 저장합니다.
                session['user'] = {
                    'uid': uid,
                    'email': User.email,
                    'avr_url' : User.user_metadata['avatar_url'],
                    'name' : User.user_metadata['full_name']
                }
                
                if value is None:
                    return jsonify({
                    "isSuccess": True,
                    "message": "Login successful",
                    "uid": uid,
                    "redirect_url": "/login/signup"
                })
                role = 'teacher' if value else 'student'
                redirect_url = "/login/teacher/dashboard_page" if value else "/login/student/dashboard_page"

                session['role'] = role

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
                    "redirect_url": "/login"
                })

        except Exception as e:
            print(f"Error during OAuth callback: {e}")
            return jsonify({'error': str(e)}), 500
    else:
        # GET 요청 시 JavaScript를 포함한 간단한 HTML 페이지를 반환
                return render_template_string('''
            <!doctype html>
            <html>
            <head>
                <script type="text/javascript">
                    document.addEventListener('DOMContentLoaded', function() {
                        const hash = window.location.hash.substring(1);
                        if (hash) {
                            const params = new URLSearchParams(hash);

                            const accessToken = params.get('access_token');
                            const providerToken = params.get('provider_token');
                            const refreshToken = params.get('refresh_token');

                            if (accessToken && providerToken && refreshToken) {
                                fetch('/login/callback', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json'
                                    },
                                    body: JSON.stringify({
                                        access_token: accessToken,
                                        provider_token: providerToken,
                                        refresh_token: refreshToken
                                    })
                                }).then(response => response.json())
                                .then(data => {
                                    console.log(data);
                                    if (data.redirect_url) {
                                        window.location.href = data.redirect_url;
                                    } else {
                                        alert('OAuth 콜백 처리 중 오류가 발생했습니다.');
                                    }
                                });
                            }
                        }
                    });
                </script>
            </head>
            <body>
                <p>Processing...</p>
            </body>
            </html>
        ''')



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


# 로그인 후 dashboard로 이동
@bp.route('/teacher/dashboard_page')
def teacher_main_page():
    print(f'현재 세션: {session}')
    return render_template('./Teacher_page/Teacher_Main_page/Teacher_Main_page_Dashboard.html')

# student- callup 페이지 =시간표/대시보드 페이지
@bp.route('/student/dashboard_page')
def student_main_page():
    testttt = supabase.auth.get_user()
    test2222= supabase.table('userinfo').select('*').execute()
    print(f'현재 세션: {session}')
    print(f'현재 정보가있나: {testttt}')
    with current_app.app_context():
        return redirect(url_for('student_main.chat_up_call'))
    #return render_template('./Student_page/Chat_Up_Call_page/Chat_Up_Call.html')

# 선생인지, 학생인지 알기 전에 userinfo 로 보내기 -아직페이지가 없어서 signup에 보내기
@bp.route('/userinfo_page')
def userinfo_page():
    return render_template('./login/SignUp_page.html')


# 회원가입 - 현재 중복확인 버튼 id값이 없음

# 이메일 중복 확인
@bp.route('/check-email', methods=['POST'])
def check_email():
    email = request.json['email']
    result = supabase.table("profile").select("email").eq("email", email).execute()

    if result.data:
        return jsonify({"exists": True}), 200
    else:
        return jsonify({"exists": False}), 200

# 회원가입 (이메일로 하는 경우) - JS에서 학생인지, 선생인지 받아오는경우
@bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    print(f"세션상태 {session}")
    if session['user']:
        uid = session['user']['uid']
        email =session['user']['email']
        IsT= data.get('isTeacher')
        session['role'] = 'teacher' if IsT else 'student'
        redirect_url = "/login/teacher/dashboard_page" if IsT else "/login/student/dashboard_page"
        # Insert user data into 'userinfo' table
        user_data = {
            'user_id': uid,
            'user_name': data['name'],
            'birthday': data['birthdate'],
            'gender': data['gender'],
            'phone': data['phone'],
            'address': data['address'],
            'email': email,
            'IsT': IsT
        }
        insert_response = supabase.table('userinfo').insert(user_data).execute()
        
        if insert_response.data:
            return jsonify({'success': True, "redirect_url": redirect_url}), 201
        else:
            return jsonify({'error': '추가 등록 실패'}), 400

    
    response = supabase.auth.sign_up({
        "email": data['email'],
        "password": data['password'],
        "options": {
            "data": {
                "name": data['name'],
                "avatar_url": 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png', # 기본 이미지 제공
                "phone": data['phone']
            }
        }
    })

    if response:
        result = supabase.from_('profile').select('id').eq('email', data['email']).execute()
        profile_id = result.data[0]['id'] if result.data else None
        print(f"프로필 uid : {profile_id}")
        if profile_id:
            user_data = {
                'user_id' :profile_id,
                'user_name': data['name'],
                'birthday': data['birthdate'],
                'gender': data['gender'],
                'phone': data['phone'],
                'address': data['address'],
                'email': data['email'],
                'IsT': data.get('isTeacher')
            }
            insert_response =supabase.table('userinfo').insert(user_data).execute()
            if insert_response.data:
                return jsonify({'success': True}), 201
        else:
            return jsonify({'error': 'Registration failed'}), 400