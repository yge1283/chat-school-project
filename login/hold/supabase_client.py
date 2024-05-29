import os
from flask import g
from werkzeug.local import LocalProxy
from supabase.client import Client, ClientOptions
from flask_storage import FlaskSessionStorage
from dotenv import load_dotenv

# .env 파일 로드
# pip install python-dotenv
load_dotenv()

# 보안상 config.py 보다는 .env 파일에 URL과 KEY값 저장하는 것이 좋다고함
url = os.environ.get("SUPABASE_URL", "")
key = os.environ.get("SUPABASE_KEY", "")

# 클라이언트 인스턴스 반환
def get_supabase() -> Client:
    if "supabase" not in g:
        g.supabase = Client(
            url,
            key,
            options=ClientOptions(
                storage=FlaskSessionStorage(),
                flow_type="pkce"
            ),
        )
    return g.supabase

# LocalProxy는 supabase 클라이언트가 처음 접근될 때만 생성되도록 하며
# 이후에는 동일한 인스턴스를 사용하도록 합니다.
supabase: Client = LocalProxy(get_supabase)
