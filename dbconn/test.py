from connect import MySQLConnector

if __name__ == '__main__':
    # config 파일에서 설정을 읽어옵니다. 기본설정시 app.ini의 mysql 부분을 가져옴
    config = MySQLConnector.read_config()
    # MySQLConnector 클래스의 인스턴스를 생성하고 구성을 전달합니다.
    conn = MySQLConnector(config)
    conn.connect()
    
    # call_grade_class 함수를 호출하여 학년과 학급에 해당하는 학생의 정보를 가져옵니다.
    # board는 테이블상 학생, 선생이 나누어 있는 관계로 테이블 잘봐서 입력값 필요
    student = [(1,'남', '홍길동', '2000-03-10', '010-1234-5678', 1, 1),
        (1,'여', '김철수', '2001-06-20', '010-5678-1234', 2, 3),
        (1,'남', '이영희', '2002-09-15', '010-9876-5432', 3, 2)]
    conn.n_table("Student",student)
    chat = [('2024-04-19 16:59:45' ,'1', '홍길동', '223daf'),]
    conn.n_table("Chatbot",chat)
    student = [{
    '성별': '여성',
    '이름': '김영희',
    '생년월일': '2005-03-15',
    '휴대폰번호': '010-1234-5678',
    '학년': 1,
    '학급': 1
    }]
    conn.it_table("Student", student)
    print(conn.sl_table("Student","학년",1))
    print(conn.sl_table("Student","과목명","수학"))
    conn.tb_del("Student","학생ID",3)