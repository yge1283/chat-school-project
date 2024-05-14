"""
colab 백엔드에서 서버 실행중에만 사용가능.

(웹) 서버로 요청 > (aws 서버) colab으로 요청 > (colab) 요청 처리 후 답변 반환 
 > (aws 서버) 받은 답변 웹으로 & 질의응답 DB에 저장  > (웹) 답변 표시


"""



import requests
import json

url1 = "https://8740-34-125-57-107.ngrok-free.app/send_message" #코랩으로 메세지 전달 후 queue에 저장
url2 = "https://8740-34-125-57-107.ngrok-free.app/get_result"  #코랩에서 queue에 저장된 메세지 처리 후 반환

response = requests.post(url1, data={'message': '오늘 점심메뉴 추천해줘'})
print(response)

# {'result': 답변} 딕셔너리 형태로 반환.
response2 = requests.get(url2)
print(json.dumps(response2.text, ensure_ascii=False))
print(response2.text.encode().decode('unicode-escape'))