from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser
class MySQLConnector:
    def __init__(self, config):
        self.config = config

    def read_config(filename='app.ini', section='mysql'):    
        # Create a ConfigParser object to handle INI file parsing
        config = ConfigParser()

        # Read the specified INI configuration file
        config.read(filename)

        # Initialize an empty dictionary to store configuration data
        data = {}

        # Check if the specified section exists in the INI file
        if config.has_section(section):
            # Retrieve all key-value pairs within the specified section
            items = config.items(section)

            # Populate the data dictionary with the key-value pairs
            for item in items:
                data[item[0]] = item[1]
        else:
            # Raise an exception if the specified section is not found
            raise Exception(f'{section} section not found in the {filename} file')

        # Return the populated data dictionary
        return data
    def connect(self):
        """ MySQL 데이터베이스에 연결합니다. """
        conn = None
        try:
            print('MySQL 데이터베이스에 연결 중...')
            conn = MySQLConnection(**self.config)

            if conn.is_connected():
                print('연결이 성공적으로 수립되었습니다.')
            else:
                print('연결에 실패했습니다.')
        except Error as error:
            print(error)
        finally:
            if conn is not None and conn.is_connected():
                conn.close()
                print('연결이 종료되었습니다.')

    def call_grade_class(self, year, class_num):
        try:
            # MySQL 데이터베이스에 연결합니다.
            with MySQLConnection(**self.config) as conn:
                # SQL 쿼리를 실행할 커서를 생성합니다.
                with conn.cursor() as cursor:
                    # grade_class 저장 프로시저를 호출하고 결과를 받습니다.
                    cursor.callproc('grade_class', [year, class_num])

                    # 저장 프로시저의 결과를 저장하기 위한 리스트를 생성합니다.
                    students = []

                    # OUT 매개변수의 값을 가져와 리스트에 추가합니다.
                    for result in cursor.stored_results():
                        students.extend(result.fetchall())

                    # 결과를 반환합니다.
                    return students

        except Error as e:
            # 예외가 발생한 경우 해당 예외를 다시 발생시킵니다.
            raise e
    def board(self, search, title):
        try:
            # MySQL 데이터베이스에 연결합니다.
            with MySQLConnection(**self.config) as conn:
                # SQL 쿼리를 실행할 커서를 생성합니다.
                with conn.cursor() as cursor:
                    # SQL 쿼리를 실행합니다. search가 제목, 내용 등의 칼럼명이라고 가정합니다.
                    query = f"SELECT * FROM 게시판 WHERE {search} = %s"
                    cursor.execute(query, (title,))

                    # 결과를 저장하기 위한 리스트를 생성합니다.
                    results = []

                    # 결과를 가져와 리스트에 추가합니다.
                    for row in cursor.fetchall():
                        results.append(row)

                    # 결과를 반환합니다.
                    return results
        except Error as e:
            # 예외가 발생한 경우 해당 예외를 다시 발생시킵니다.
            raise e

    def istable(self, tbname, data):
        try:
            # MySQL 데이터베이스에 연결합니다.
            with MySQLConnection(**self.config) as conn:
                # SQL 쿼리를 실행할 커서를 생성합니다.
                with conn.cursor() as cursor:
                    # 삽입 쿼리를 생성합니다.
                    if tbname == "게시판":
                        query = "INSERT INTO 게시판 (게시물ID, 대시보드key, 제목, 학생ID, 선생ID, 작성내용, 작성시간) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    elif tbname == "대시보드":
                        query = "INSERT INTO 대시보드 (대시보드key, 과목명, 학년, 학급, 담당선생ID) VALUES (%s, %s, %s, %s, %s)"
                    elif tbname == "댓글":
                        query = "INSERT INTO 댓글 (댓글ID, 작성자ID, 내용, 댓글시간, 게시물ID) VALUES (%s, %s, %s, %s, %s)"
                    elif tbname == "선생":
                        query = "INSERT INTO 선생 (선생ID, 성별, 이름, 생년월일, 이메일) VALUES (%s, %s, %s, %s, %s)"
                    elif tbname == "챗봇":
                        query = "INSERT INTO 챗봇 (시간, 학생ID, 질문, 챗봇응답) VALUES (%s, %s, %s, %s)"
                    elif tbname == "첨부파일":
                        query = "INSERT INTO 첨부파일 (파일ID, 게시물ID, 파일명, 파일경로, 시간) VALUES (%s, %s, %s, %s, %s)"
                    elif tbname=="학생":
                        query = "INSERT INTO 학생 (학생ID, 성별, 이름, 생년월일, 휴대폰번호, 학년, 학급) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    elif tbname=="문제":
                        query = "INSERT INTO 문제 (학생ID, 성별, 이름, 생년월일, 휴대폰번호, 학년, 학급) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    else:
                        # 테이블이 없는 경우 예외를 발생시킵니다.
                        raise ValueError(f"테이블 '{tbname}'이 존재하지 않습니다.")

                    # 데이터를 순서대로 삽입합니다.
                    for item in data:
                        cursor.execute(query, item)
                    conn.commit()

        except Error as e:
            # 예외가 발생한 경우 해당 예외를 다시 발생시킵니다.
            raise e