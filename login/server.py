# 플라스크 언어 (서버용)

from flask import Flask, request, jsonify, redirect
from supabase import create_client, Client
import config  # config 파일 불러오기

app = Flask(__name__)


# Supabase 키값 config.py 에서 가져오기 >> config파일은 업로드 하지 xx
# config.py 파일이 Git 저장소에 포함되지 않도록 설정해야함.
url = config.SUPABASE_URL
key = config.SUPABASE_KEY
supabase: Client = create_client(url, key)

# 이메일 중복 확인
@app.route('/check-email', methods=['POST'])
def check_email():
    email = request.json['email']
    result = supabase.table("profile").select("email").eq("email", email).execute()
    if result.data:
        return jsonify({"exists": True}), 200
    else:
        return jsonify({"exists": False}), 200

# 회원가입 (이메일로 하는 경우) - JS에서 학생인지, 선생인지 받아오는경우
@app.route('/register_student', methods=['POST'])
def register():
    data = request.json
    options = {
        "data": {
            "name": data['name'],
            "avatar_url": data.get('avatar_url', 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'), # 기본 이미지 제공
            "phone": data['phone']
        }
    }
    response = supabase.auth.sign_up(email=data['email'], password=data['password'], options=options)
    if 'user' in response:
        user_data = {
            
            'user_name': data['name'],
            'birthday': data['birthdate'],
            'gender': data['gender'],
            'phone': data['phone'],
            'address': data['address'],
            'email': data['email'],
            'isT' : data.get('is_teacher', False) 
        }
        supabase.table('userinfo').insert(user_data).execute()
        return jsonify({'success': True}), 201
    else:
        return jsonify({'error': 'Registration failed'}), 400
    

# 이메일로 로그인
@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    result = supabase.auth.sign_in(email=email, password=password)
    if result.get('error') is None:
        return jsonify({'session': result['session']}), 200
    else:
        return jsonify({'error': result['error']}), 401

# 구글로 로그인
@app.route('/login-google')
def login_google():
    return redirect(
        supabase.auth.sign_in_with_provider('google', redirect_to=url_for('callback', _external=True))
    )
# 구글(서드파티)로 로그인이 처음인 경우
@app.route('/callback')
def callback():
    # 세션에 저장된 사용자 ID 가져오기
    user_id = session.get('user_id')
    
    if not user_id:
        # Supabase 세션에서 사용자 ID를 가져오는 방법 예시 (구체적 구현 필요)
        user_id = supabase.auth.user().id if supabase.auth.user() else None
        session['user_id'] = user_id

    if user_id:
        # userinfo 테이블에서 사용자 정보 확인
        user_info = supabase.table('userinfo').select("*").eq('user_id', user_id).execute()
        
        if user_info.data and len(user_info.data) > 0:
            # 사용자 정보가 있으면 메인 페이지로 리다이렉트
            return redirect(url_for('main_page'))
        else:
            # 사용자 정보가 없으면 추가 정보 입력 페이지로 리다이렉트
            return redirect(url_for('additional_info'))
    else:
        return 'Authentication failed', 401

# 
@app.route('/additional-info')
def additional_info():
    return 'Please provide additional information'


# 카카오로 로그인
@app.route('/login-kakao')
def login_kakao():
    return redirect(
        supabase.auth.sign_in_with_provider('kakao', 
            redirect_to='메인페이지')
    )

# 로그아웃 
@app.route('/logout', methods=['POST'])
def logout():
    session = request.headers.get('Authorization')
    result = supabase.auth.sign_out(session)
    if result.get('error') is None:
        return jsonify({'message': 'Logged out successfully'}), 200
    else:
        return jsonify({'error': result['error']}), 401

# 로그인 상태인지 아닌지 확인하는 코드
@app.route('/checklogin')
def checklogin():
    user = session.get('user')  # 사용자 세션에서 사용자 정보 가져오기
    if user:
        return jsonify({'status': 'logged_in', 'user': user}), 200
    else:
        return jsonify({'status': 'logged_out'}), 200

# 프로필 이미지 가져오기
@app.route('/profile')
def profile():
    user_token = session.get('user_token')
    if not user_token:
        return jsonify({'error': 'User not logged in'}), 401

    response = supabase.table("profile").select("avatar_url, username").single().execute()
    if response.error:
        return jsonify({'error': 'Failed to fetch profile data'}), 500
    if not response.data:
        return jsonify({'error': 'Profile not found'}), 404
    
    profile_data = response.data
    return jsonify({
        'avatar_url': profile_data['avatar_url'],
        'username': profile_data['username']
    }), 200



# 비밀번호 재설정
# 이메일 OTP 전송코드
@app.route('/reset-password-request', methods=['POST'])
def reset_password_request():
    email = request.json['email']
    result = supabase.auth.api.reset_password_for_email(email)
    if 'error' not in result:
        return jsonify({'message': 'Password reset email sent'}), 200
    return jsonify({'error': result['error']}), 400

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    email = request.json['email']
    token = request.json['token']
    result = supabase.auth.api.verify_otp({
        'email': email, 'token': token, 'type': 'recovery'
    })
    if 'error' not in result:
        session['user'] = result['user']
        return jsonify({'message': 'OTP verified'}), 200
    return jsonify({'error': result['error']}), 400

# 비밀번호 재설정
@app.route('/update-password', methods=['POST'])
def update_password():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    password = request.json['password']
    result = supabase.auth.api.update_user_by_id(session['user']['id'], {'password': password})
    if 'error' not in result:
        return jsonify({'message': 'Password updated successfully'}), 200
    return jsonify({'error': result['error']}), 400


if __name__ == "__main__":
    app.run(debug=True)