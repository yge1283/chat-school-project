from flask import Flask, session, jsonify, request, render_template
from supabase import create_client, Client
import os

app = Flask(__name__)

# Supabase 설정
supabase_url = ""
supabase_key = ""
supabase: Client = create_client(supabase_url, supabase_key)


# 사용자가 'naver.com 처럼 특정 URL 에 접속할때 - 로그인 페이지를 반환'
@app.route('/')
def index():
    return render_template('/login/Login_page.html')
# html 반환은 됨



# 하나의 코드로 supabase/table에 있는 정보값 가져오기
# table_name : 게시판
@app.route('/api/get-table/<table_name>', methods=['GET'])
def api_get_table(table_name):
    try:
        response = supabase.table(table_name).select('*').execute()
        data = response.data
        return jsonify(data), 200
    except Exception as e:
        print(f"Error fetching table data: {e}")
        return jsonify({'error': str(e)}), 500



# 이메일로 로그인 - 현재 확인 완료 잘 됨

@app.route('/login-email', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        
        result = supabase.auth.sign_in_with_password({"email": email, "password": password})

        uid = result.get('user', {}).get('id')

        print(f"Supabase response: {result}")

        if uid:
            # 유저 정보 조회
            userinfo = supabase.table('userinfo').select('IsT').eq('uid', uid).single().execute()
            
            # 선생인지 학생인지 확인하는 코드
            if userinfo.get('data', {}).get('IsT') == True:
                # session role값 지정 후 다른 페이지로 리다이렉트 할때마다 역할을 확인하면됨
                session['role'] = 'teacher'
                return render_template('teacher/main_page.html')
            else:
                session['role'] = 'student'
                return render_template('student/main_page.html')
        else:
            return jsonify({"message": "Login failed"}), 401
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"message": "An error occurred during login"}), 500
    

# 로그인 상태인지 아닌지 확인하는 코드
@app.route('/checklogin')
def checklogin():
    user = session.get('user')  # 사용자 세션에서 사용자 정보 가져오기
    if user:
        return jsonify({'status': 'logged_in', 'user': user}), 200
    else:
        return jsonify({'status': 'logged_out'}), 200
    
    







if __name__ == "__main__":
    app.run(debug=True)
