# chat-school-back
챗업스쿨 백엔드 구성  

- 가능한 객체(클래스)단위로 작성하기  
- 생성AI는 Docker에서 각개로 실행될 것임(로컬 구동시)  
- 이외 기능 main.py에 작성  

## Open Ai GPT
- API키는 개인이 각자 사용  
- 미완  

## koGPT2 로컬 구동 LM
- https://github.com/MrBananaHuman/KorGPT2Tutorial.git 하드포크 된것임  
- 테스트용으로 추후 수정/삭제 될수 있음  
- model은 용량이 커서 위 링크에서 제공되는 파일 별도 다운하여 'models'에 넣기  

## 로그인 / 회원등록 기능
- 'login'폴더에 작성  
- 회원 데이터는 DB미사용시 임시로 csv로 저장 및 테스트  
- Firebase 연동시 api키 공유하기(잔디에)  

## MySql설치 및 연동
1. 파이선용 mysql라이브러리 설치  
'pip instal pymysql'
2. 'mysql.py'에서 테스트

## requirements
추후 생성