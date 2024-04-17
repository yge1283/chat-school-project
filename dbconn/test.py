from connect import MySQLConnector
if __name__ == '__main__':
  # config 파일에서 설정을 읽어옵니다.
  config = MySQLConnector.read_config()
  # MySQLConnector 클래스의 인스턴스를 생성하고 구성을 전달합니다.
  conn = MySQLConnector(config)
  print(conn.call_grade_class(1,1))
  student=[('student5', '여성', '김영희', '2005-03-15', '010-1234-5678', 1, 1),
          ('student6', '남성', '박철수', '2006-06-20', '010-2345-6789', 1, 2),
          ('student7', '여성', '이영자', '2007-09-25', '010-3456-7890', 1, 2)]
  conn.istable("학생",student)
