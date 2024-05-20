from flask import Blueprint, render_template, request, jsonify, redirect
import asyncio
from supabase import create_client, Client
from .. import config  # dbconn 폴더의 config 파일 불러오기


url = config.SUPABASE_URL
key = config.SUPABASE_KEY
supabase: Client = create_client(url, key)

bp = Blueprint('main', __name__, url_prefix='/login') # /login 페이지 설정


# @bp.route('/signup')
# def hello_pybo():
#     return 'Hello, Pybo!'

def examine_signup_info(email, phone, teacher): #가입정보를 받아 db있는 값과 비교하여 중복검사 함수
    #db filtering 코드 (선생님인지 학생인지에 따라 검색 테이블 다르게)
    dbemail=''
    dbphone=''

    if email == dbemail:
        return "email_exist" # 중복되는 이메일이 있으면
    elif phone == dbphone:
        return "phone_exist"  #중복되는 전화번호가 있으면
    else:
        return 'clean'  #중복되는 값이 없으면

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


# 이메일로 로그인
@bp.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    result = supabase.auth.sign_in(email=email, password=password)
    if result.get('error') is None:
        return jsonify({'session': result['session']}), 200
    else:
        return jsonify({'error': result['error']}), 401



@bp.route('/send_signupform')
def send_signupform():
    #가입정보 받는 코드 {딕셔너리}(json)
    #형식 {"username":"", "birthYear":"", "birthMonth":"", "birthDay":"", "password":"", "phone":"", "address":"","teacher":""}
    # "teacher"의 값은 True or False
    recieve_info = request.form

    #받은 가입정보로 db에 중복된 이메일, 전화번호 있는지 검사 하는 함수
    result = examine_signup_info(recieve_info['email'], recieve_info['phone'], recieve_info['teacher'])
    
    #위 검사에서 중복이 있으면 반환값 그대로 응답
    if result != 'clean':
        return result  # 'email_exist' or 'phone_exist'
    
    else: 

        #위 검사에서 중복이 없으면 학생 table에 각 요소 저장하는 코드
        #서드파티 미연동시, uid 생성 하는 코드

        return 'success' # 가입 성공시 응답

