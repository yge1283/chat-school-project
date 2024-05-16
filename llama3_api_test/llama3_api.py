"""
colab 백엔드에서 서버 실행중에만 사용가능.

(웹) 서버로 요청 > (aws 서버) colab으로 요청 > (colab) 요청 처리 후 답변 반환 
 > (aws 서버) 받은 답변 웹으로 & 질의응답 DB에 저장  > (웹) 답변 표시


"""

import requests
#import json

url1 = "https://8740-34-125-57-107.ngrok-free.app/send_message" #코랩으로 메세지 전달 후 queue에 저장
url2 = "https://8740-34-125-57-107.ngrok-free.app/get_result"  #코랩에서 queue에 저장된 메세지 처리 후 반환

# 위 URL의 host-name은 colab이 매번 다시 실행될때마다 바뀜!!

response = requests.post(url1, data={'message': '오늘 점심메뉴 추천해줘'}) #보낼 때 data에 딕셔너리 형태로 전송
print(response)

# {'result': '답변'} 딕셔너리 형태로 받음. 추후 받는 정보 추가 예정(토큰사용량 등)
response2 = requests.get(url2)
print(response2.text)
print(response2.text.encode().decode('unicode-escape')) #서버에서 바로 확인할때 디코더 설정


"""
출력 
<Response [200]>
"{\"result\":\"\\uc548\\ub155\\ud558\\uc138\\uc694! \\uc624\\ub298 \\uc800\\ud76c \\uc2dd\\ub2f9\\uc5d0\\uc11c \\ub9db\\uc788\\ub294 \\uba54\\ub274 \\uc911 \\ud558\\ub098\\ub294 \\uce74\\ub808 \\ub77c\\uc774\\uc2a4\\uc785\\ub2c8\\ub2e4. \\ub9e4\\ucf64\\ud55c \\uce74\\ub808 \\uc18c\\uc2a4\\uc640 \\ud568\\uaed8 \\ub2e4\\uc591\\ud55c \\ucc44\\uc18c, \\uace0\\uae30, \\uacc4\\ub780 \\ub4f1\\uc744 \\uacc1\\ub4e4\\uc5ec \\uc990\\uae38 \\uc218 \\uc788\\uc5b4\\uc694.\\n\\ucd94\\ucc9c: 1\\ubc88, \\\"\\uce74\\ub808\\ub77c\\uc774\\uc2a4\\\"\"}\n"
{"result":"안녕하세요! 오늘 저희 식당에서 맛있는 메뉴 중 하나는 카레 라이스입니다. 매콤한 카레 소스와 함께 다양한 채소, 고기, 계란 등을 곁들여 즐길 수 있어요.
추천: 1번, "카레라이스""}
"""