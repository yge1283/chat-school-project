from connect import MySQLConnector

if __name__ == '__main__':
    # config 파일에서 설정을 읽어옵니다. 기본설정시 app.ini의 mysql 부분을 가져옴
    config = MySQLConnector.read_config()
    # MySQLConnector 클래스의 인스턴스를 생성하고 구성을 전달합니다.
    conn = MySQLConnector(config)

    # call_grade_class 함수를 호출하여 학년과 학급에 해당하는 학생의 정보를 가져옵니다.
    print(conn.call_grade_class(1,1))

    # 삽입할 학생 데이터를 정의합니다.
    student = [
        ('student5', '여성', '김영희', '2005-03-15', '010-1234-5678', 1, 1),
        ('student6', '남성', '박철수', '2006-06-20', '010-2345-6789', 1, 2),
        ('student7', '여성', '이영자', '2007-09-25', '010-3456-7890', 1, 2)
    ]
  
    # istable 함수를 호출하여 학생 테이블에 학생 데이터를 삽입합니다.
    conn.istable("학생", student)
