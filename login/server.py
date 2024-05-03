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
    result = supabase.table("userinfo").select("email").eq("email", email).execute()
    if result.data:
        return jsonify({"exists": True}), 200
    else:
        return jsonify({"exists": False}), 200

# 아이디 중복 확인
@app.route('/check-id', methods=['POST'])
def check_id():
    user_id = request.json['user_id']
    result = supabase.table("userinfo").select("user_id").eq("user_id", user_id).execute()
    if result.data:
        return jsonify({"exists": True}), 200
    else:
        return jsonify({"exists": False}), 200

# 회원가입
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    response = supabase.auth.sign_up(email=data['email'], password=data['password'])
    if 'user' in response:
        user_data = {
            'user_name': data['name'],
            'birthday': data['birthdate'],
            'user_id': data['user_id'],
            'gender': data['gender'],
            'phone': data['phone'],
            'address': data['address'],
            'email': data['email']
        }
        supabase.table('userinfo').insert(user_data).execute()
        return jsonify({'success': True}), 201
    else:
        return jsonify({'error': 'Registration failed'}), 400

if __name__ == "__main__":
    app.run(debug=True)