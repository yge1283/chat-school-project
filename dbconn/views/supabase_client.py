from supabase import create_client, Client
from .. import config  # dbconn 폴더의 config 파일 불러오기

url = config.SUPABASE_URL
key = config.SUPABASE_KEY
supabase: Client = create_client(url, key)