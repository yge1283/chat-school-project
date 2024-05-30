# 여기 있는 코드는 connect.py에 올라갈 예정(ORM)
# 잘 작동되는지 확인한후에

# 1. 테이블마다 어떤 정보를 반환할건지 짜야하는데

from flask import Flask, session, jsonify, request, render_template
from supabase import create_client, Client
import os

app = Flask(__name__)

# Supabase 설정
supabase_url = ""
supabase_key = ""
supabase: Client = create_client(supabase_url, supabase_key)

app = Flask(__name__)

# Supabase 설정
supabase_url = ""
supabase_key = ""
supabase: Client = create_client(supabase_url, supabase_key)



# 시간표 반환하는 코드# 10가지 색상 리스트 정의
colors = [
    "#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#A133FF",
    "#33FFF6", "#FF9633", "#8D33FF", "#33FFB5", "#FF3333"
]

def fetch_timetable_data():
    response = supabase.table('대시보드').select('과목명, 시간표').execute()
    data = response.data
    return data

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

@app.route('/timetable-teacher', methods=['GET'])
def get_timetable():
    data = fetch_timetable_data()
    processed_data = process_timetable(data)
    return jsonify(processed_data)



# 업로드 파일
# bucket 이름 받아야됨 클라이언트 쪽에서
@app.route('/dbapi/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 파일 확장자 체크
    if not (file.filename.endswith('.pdf') or file.filename.endswith('.txt')):
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        path_on_supastorage = f"uploads/{file.filename}"
        # 파일을 읽어서 Supabase에 업로드
        response = supabase.storage.from_("testbucket").upload(file=file.read(), path=path_on_supastorage, file_options={"content-type": file.content_type})
        print(response)
        return jsonify({'message': 'File uploaded successfully', 'path': path_on_supastorage}), 200
    except Exception as e:
        print(f"Error during file upload: {e}")
        return jsonify({'error': str(e)}), 500






with open(filepath, 'rb') as f:
    supabase.storage.from_("testbucket").upload(file=f,path=path_on_supastorage, file_options={"content-type": "audio/mpeg"})
