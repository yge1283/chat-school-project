# 1. firebase에서 기능 구현하기
## 1.1 login 기능 구현
참고 사이트: 
https://velog.io/@anji00/Firebase-로그인-구현하기-1 (web 전용)

https://velog.io/@gmlstjq123/Firebase-사용하기 (Android 전용)

Firebase설치 (html만 사용시 / react 사용시)
https://codingapple.com/unit/firebase-installation-with-npm/?id=9822

[깃 push - git status / git add . / git cummit -m "" / git push origin main]

## 1.11 프로젝트 생성 및 빌드 추가
Authentication에서 Sign-in-method 탭에서
로그인 방법 추가하기
앱추가하기 - 웹 앱(sdk 키 발급 받아서 firebase.js 코드에 추가)


# 2 supabase에서 기능 구현하기
## 2.1 login 기능 구현
참고 사이트: 
https://velog.io/@dyorong/supabase-로그인-기능-구현

구글, 카카오 로그인 구현완료(auth.users 데이터 : 
    role(역할) : 인증됨(authenticated)
    이메일
    avar 사진 : 프로필 사진
    비밀번호
    creat at : 만들어진 시간
    update at : 수정된, 업데이트 된 시간(비밀번호 재설정 등)

)
수정할 사항: 로그인이 완료되면 메인페이지로 이동
    가입하기 버튼: 가입페이지로 이동
    비밀번호 찾기 버튼 : 비밀번호 재설정 페이지로 이동

추가한 사항: 로그인이 되어있는경우 프로필 사진과, FULL name (사용자 이름)이 뜨도록변경
    + 사진이나, 이름을 클릭했을 경우 >> 본인 mypage로 이동하는 기능 추가예정
    <div class="profile"> 을 css로 위치와 사이즈를 바꿀수있음

## 2.2 supabase 회원가입 구현

추가 데이터를 다른 테이블에 저장
이메일 같은 데이터 <- auth.users에 추가되면
자동으로 다른 테이블에 저장되도록 trigger와 fucntion 구성 필요
: 현재 auth.users와 관련된 함수와 트리거가 작동하지 않음
 > 이 데이터를 기반으로 서버 DB에 보낼 예정

 ## 2.3 비밀번호 재설정 구현

비밀번호 찾기 버튼을 누르면 해당 이메일에 6자리 숫자 OTP생성
(supabase에서는 .token 이라고 칭함)
이메일에 있는 토큰의 유효기간은 60분(시간을 늘릴 수 있는데 추천하지는 않는다고함)
토큰을 입력했을때, 세션 값이 나오며(로그인이 된 상태? 인지는 모름)
비밀번호를 업데이트가 가능한 상태가 됨

추가해야할 사항
: 정상적으로 수정이 되었을 경우 - **메인페이지로 이동**
    이메일에 OTP가 정상적으로 전송되었을 경우 - **전송 버튼 비활성화 및 이메일 입력칸 수정 막기**
    토큰 인증을 완료했을 경우  - **인증 버튼 비활성화**




 ## 2.4 아이디 찾기 구현 (예정)
 auth.users : supabase에서 자동으로 등록되는 회원정보
 에서 이메일로 로그인을 실행하고 > public userinfo 에 저장된 ID 내용을
 반환해주는 것을 예정하고있는데
 현재 2.2 에서 SUPABASE 자체 회원정보가 들어있는 auth.users에 접근하는 것이 보안상 어려워서
 trigger를 무조건 구현해야하는 상황
 (전화번호 인증 기능을 추가하기에는 비용문제 때문에 이메일을 까먹는 경우는
있을 수 없다고 가정)

 ## 2.5 네이버 로그인 (가능한지 확인필요)
supabase에서는 네이버 provider가 제공되지 않아서
따로 API 를 가져와서 로그인이 되는지 확인하고
이 정보를 auth.users에 추가할 수 있는지 확인이 필요하다.



# 3 javaScript 코드를 flask 언어로 변환
## 3.1 회원가입 페이지 변경사항
기본적인 구조는 동일하나
JS내에서 supabase와 연동해서 데이터를 찾는 과정과
등록하는 과정 전부 서버에서 동작하도록 구현
'Axios를 요청을 사용함'

새로운 파일 > Join01.html , server.py

server.py 는 플라스크 언어로 제작 > 이 코드를 main.py에 넣는지 안넣는지 <논의필요>

config.py 에서 supabaseUrl, key 값 불러와서 사용함.

## 3.2 로그인 페이지 변경사항
기본적인 구조는 동일하나
JS 코드 변경 및 서버 코드 추가

새로운 파일 > login01.html
