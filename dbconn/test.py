from connect import Connector
from datetime import datetime


def convert_to_list(objects):
    data_list = []
    for obj in objects:
        data_list.append([getattr(obj, column.name) for column in obj.__table__.columns])
    return data_list
if __name__ == '__main__':
    # config 파일에서 설정을 읽어옵니다. 기본설정시 app.ini의 mysql 부분을 가져옴
    config = Connector.read_config(section='postgres')
    # Connector 클래스의 인스턴스를 생성하고 구성을 전달합니다.
    conn = Connector(config)
    conn.connect()


    student = [(1,'남', '홍길동', '2000-03-10', '010-1234-5678', 1, 1),
        (2,'여', '김철수', '2001-06-20', '010-5678-1234', 2, 3),
        (3,'남', '이영희', '2002-09-15', '010-9876-5432', 3, 2)]
    conn.tb_ninsert("Student",student)
    print(convert_to_list(conn.tb_select("Board","학생_ID",1, 1)))



    
    # board_data = [{
    # '대시보드_key': 1,  # 예시값, 실제로는 어떤 대시보드에 속하는지에 따라 달라집니다.
    # '학생_ID': 1,  # 예시값, 실제로는 어떤 학생이 작성했는지에 따라 달라집니다.
    # '제목': '새로운 게시물 제목',
    # '작성내용': '새로운 게시물 내용',
    # '작성시간': datetime.now()  # 현재 시간으로 설정
    # }]

    # student_data = [{
    #     '학생_ID': '010',
    #     '성별': '여성',  # 예시값, 실제 데이터에 따라 달라집니다.
    #     '이름': '홍길동',  # 예시값, 실제 데이터에 따라 달라집니다.
    #     '생년월일': '2000-01-01',  # 예시값, 실제 데이터에 따라 달라집니다.
    #     '휴대폰번호': '010-1234-5678',  # 예시값, 실제 데이터에 따라 달라집니다.
    #     '학년': 3,  # 예시값, 실제 데이터에 따라 달라집니다.
    #     '학급': 1  # 예시값, 실제 데이터에 따라 달라집니다.
    # }]
    # teacher_data = [(1,'남', '홍길동','2000-03-10','ibo')]
    # db_data = [(1,1,'1_1수학','1','1')]
    # conn.tb_ninsert("Teacher",teacher_data)
    # conn.tb_ninsert("Dashboard",db_data)
    # conn.tb_insert("Student", student_data)
    # conn.tb_insert("Board", board_data)
    # print(convert_to_list(conn.tb_select("Board","학생_ID",1, 1)))
    # print(convert_to_list(conn.bd_select(1,"학생_ID",1, True)))
    # print(convert_to_list(conn.bd_select(1,desc=False)))

