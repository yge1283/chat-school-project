from sqlalchemy.orm import sessionmaker
from configparser import ConfigParser
from models import Student, Board, Dashboard, Comment, Teacher, Chat, Attachment, Choice,Short_answer,Long_answer, Test,Emotion, Timetable, S_memo, T_memo, Assignment,Assignment_attachment,Submission,Submission_attachment ,Chatbot
from sqlalchemy import create_engine,text
from models import Base
from sqlalchemy_utils import database_exists, create_database
class MySQLConnector:
    def __init__(self, config):
        self.engine = create_engine(config)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def read_config(filename='app.ini', section='mysql'):
        config = ConfigParser()
        config.read(filename)
        if config.has_section(section):
            # 설정 파일에서 필요한 정보를 추출합니다.
            username = config.get(section, 'username')
            password = config.get(section, 'password')
            host = config.get(section, 'host')
            port = config.get(section, 'port')
            database = config.get(section, 'database')
            # 연결 문자열을 생성하여 반환합니다.
            return f"mysql://{username}:{password}@{host}:{port}/{database}"
        else:
            raise Exception(f'{section} section not found in the {filename} file')

    def connect(self):
        print('MySQL 데이터베이스에 연결 중...')
        try:
            connection = self.engine.connect()
            print('연결이 성공적으로 수립되었습니다.')
            connection.close()
        except Exception as e:
            print(f'연결에 실패했습니다: {e}')
    def tb_insert(self, tbname, data):
        try:
            table = globals()[tbname]
            for item in data:
                obj_data = {}
                for column, value in item.items():
                    obj_data[column] = value
                obj = table(**obj_data)
                self.session.add(obj)
            self.session.commit()
            return tbname
        except Exception as e:
            self.session.rollback()
            raise e

    def tb_ninsert(self, tbname, data):
        try:
            table = globals()[tbname]
            obj_data = {}
            for item in data:
                for col, val in zip(table.__table__.columns, item):
                    if col.primary_key and tbname != "챗봇":  # 컬럼 이름으로 비교해야 합니다.
                        continue
                    else:
                        obj_data[col.name] = val  # 컬럼의 이름을 키로 사용합니다.
                obj = table(**obj_data)
                self.session.add(obj)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        return 0

    def bd_select(self, search, title, desc=True):
        try:
            # 검색 조건(search)에 해당하는 열을 사용하여 데이터베이스에서 게시글을 검색합니다.
            query = self.session.query(Board).filter(getattr(Board, search) == title)
            # 정렬 방식을 설정합니다.
            if desc:
                # 내림차순으로 정렬합니다.
                query = query.order_by(Board.작성시간.desc())
            else:
                # 오름차순으로 정렬합니다.
                query = query.order_by(Board.작성시간.asc())
            # 정렬된 결과를 리스트로 반환합니다.
            results = query.all()
            return results
        except Exception as e:
            # 검색 과정에서 예외가 발생하면 예외를 다시 발생시킵니다.
            raise e

    def tb_select(self, tbname, search, title):
        try:
            # 테이블 클래스를 가져옵니다.
            table = globals()[tbname]
            # 검색 조건을 설정하여 쿼리를 수행합니다.
            results = self.session.query(table).filter(getattr(table, search) == title).all()
            return results
        except Exception as e:
            raise e

    def tb_delete(self, tbname, column, title):
        try:
            table = globals()[tbname]
            # 테이블에서 조건을 만족하는 데이터를 필터링합니다.
            self.session.query(table).filter(getattr(table, column) == title).delete()
            # 변경사항을 커밋합니다.
            self.session.commit()
        except Exception as e:
            # 오류가 발생한 경우 롤백합니다.
            self.session.rollback()
            raise e
        return 0

    def st_update(self,studend_id,student_new):
        try:
            # 테이블에서 조건을 만족하는 데이터를 필터링합니다.
            self.session.query(Student).filter(Student.ㅎ == studend_id).update()
            # 변경사항을 커밋합니다.
            self.session.commit()
        except Exception as e:
            # 오류가 발생한 경우 롤백합니다.
            self.session.rollback()
            raise e
        return 0



if __name__ == '__main__':
    # config 파일에서 설정을 읽어옵니다. 기본설정시 app.ini의 mysql 부분을 가져옴
    config = MySQLConnector.read_config()
    # MySQLConnector 클래스의 인스턴스를 생성하고 구성을 전달합니다.
    conn = MySQLConnector(config)
    engine = create_engine(config)
    if not database_exists(engine.url):
        create_database(engine.url)   
    else:
        print("이미 데이터베이스가 있습니다.")

    Session = sessionmaker(bind=engine)
    session = Session()
    
    Base.metadata.create_all(engine)
    session.commit()
    # 세션 종료
    session.close()
    

