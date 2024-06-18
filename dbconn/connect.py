from sqlalchemy.orm import sessionmaker
from configparser import ConfigParser, ExtendedInterpolation
from .models import Base,Student, Board, Dashboard, Comment, Teacher, Chat, Attachment, Choice,Short_answer,Long_answer, Test,Emotion, Attendee, S_memo, T_memo, Assignment,Assignment_attachment,Submission,Submission_attachment ,Chatbot,Classdata,Userinfo
from sqlalchemy import create_engine,text
from sqlalchemy_utils import database_exists, create_database
from datetime import datetime, date
from sqlalchemy.sql import func
from sqlalchemy.exc import PendingRollbackError, SQLAlchemyError
import json

class Connector:
    def __init__(self, config):
        self.engine = create_engine(config)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def read_config(filename='./dbconn/app.ini', section='postgres'):
        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read(filename)
        
        if config.has_section(section):
            database_type = config.get(section, 'database')
            
            if database_type in ['mysql','postgresql', 'postgres']:
                # MySQL의 경우 데이터베이스 선택 필요
                username = config.get(section, 'username')
                password = config.get(section, 'password')
                host = config.get(section, 'host')
                port = config.get(section, 'port')
                dbname = config.get(section, 'dbname')  # MySQL의 경우 데이터베이스 명 필요
                
                return f"{database_type}://{username}:{password}@{host}:{port}/{dbname}"
            
            else:
                raise Exception(f"Invalid database type '{database_type}' in the configuration file")
        else:
            raise Exception(f"{section} section not found in the {filename} file")


    def connect(self):
        print('데이터베이스에 연결 중...')
        try:
            connection = self.engine.connect()
            print('연결이 성공적으로 수립되었습니다.')
            connection.close()
        except Exception as e:
            print(f'연결에 실패했습니다: {e}')

    def tb_insert(self, tb_name, data):
        try:
            table = globals()[tb_name]
            for item in data:
                obj_data = {}
                for column, value in item.items():
                    obj_data[column] = value
                obj = table(**obj_data)
                self.session.add(obj)
            self.session.commit()
            return tb_name
        except Exception as e:
            self.session.rollback()
            raise e

    def tb_ninsert(self, tb_name, data):
        try:
            table = globals()[tb_name]
            obj_data = {}
            for item in data:
                for col, val in zip(table.__table__.columns, item):
                    if col.primary_key and tb_name != "챗봇":  # 컬럼 이름으로 비교해야 합니다.
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



    def tb_select(self, tb_name, col=None, search=None, db_key=None, today_only=None):
        try:
            # 테이블 클래스를 가져옵니다.
            table = globals()[tb_name]
            query = self.session.query(table, Student.학생이름).join(Student, table.학생_ID == Student.학생_ID)

            # db_key 조건이 있는 경우
            if db_key is not None:
                query = query.filter(getattr(table, "대시보드_key") == db_key)
            
            # search와 title 조건이 있는 경우
            if col is not None and search is not None:
                query = query.filter(getattr(table, col) == search)
            
            # 오늘 날짜 조건 추가
            if today_only:
                today = date.today()
                query = query.filter(func.date(table.시간) == today)
            
            json_results = []
            results = query.all()
            for board, user_name in results:
                board_dict = board.to_dict()
                board_dict['user_name'] = user_name
                json_results.append(board_dict)
            
            return json.dumps(json_results, ensure_ascii=False, indent=4, default=str)
        
        except PendingRollbackError:
            self.session.rollback()
            return self.tb_select(tb_name, col, search, db_key, today_only)
        
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        
        except Exception as e:
            raise e
        
    def tb_get(self, tb_name, col, search, dashboard_key=None):
        try:
            table = globals()[tb_name]
            query = self.session.query(table, Student.user_name).join(Student, table.학생_ID == Student.user_id).filter(getattr(table, col) == search)
            
            if dashboard_key:
                query = query.filter(getattr(table, '대시보드_key') == dashboard_key)

            results = query.all()
            json_results = []
            for board, user_name in results:
                    board_dict = board.to_dict()
                    board_dict['user_name'] = user_name
                    json_results.append(board_dict)
            return json.dumps(json_results, ensure_ascii=False, indent=4, default=str)

        except Exception as e:
            self.session.rollback()
            raise e

            

    

    def tb_delete(self, tb_name, col, search):
        try:
            table = globals()[tb_name]
            # 테이블에서 조건을 만족하는 데이터를 필터링합니다.
            self.session.query(table).filter(getattr(table, col) == search).delete()
            # 변경사항을 커밋합니다.
            self.session.commit()
        except Exception as e:
            # 오류가 발생한 경우 롤백합니다.
            self.session.rollback()
            raise e
        return 0

    def tb_update(self,tb_name,col,search,student_new):
        try:
            # 테이블에서 조건을 만족하는 데이터를 필터링합니다.
            table = globals()[tb_name]
            self.session.query(table).filter(getattr(table, col) == search).update(student_new)
            # 변경사항을 커밋합니다.
            self.session.commit()
        except Exception as e:
            # 오류가 발생한 경우 롤백합니다.
            self.session.rollback()
            raise e
        return 0

    def bd_select(self, db_key, col=None, search=None, desc=True,page=None):
        try:
            
            query = self.session.query(Board, Student.학생이름).join(Student, Board.학생_ID == Student.학생_ID)
            
            if col:
                query = query.filter(Board.대시보드_key == db_key).filter(getattr(Board, col) == search)
            else:
                query = query.filter(Board.대시보드_key == db_key)

            if desc:
                query = query.order_by(Board.작성시간.desc())
            else:
                query = query.order_by(Board.작성시간.asc())
            if page:
                query=query.offset((int(page)-1)*6)
            results = query.limit(6).all()
            json_results = []
            for board, user_name in results:
                board_dict = board.to_dict()
                board_dict['user_name'] = user_name
                json_results.append(board_dict)
            return json.dumps(json_results, ensure_ascii=False, indent=4, default=str)
        except Exception as e:
            self.session.rollback()
            raise e

    def me_get(self, tb_name, search, memo_ID=None, page=None):
        try:
            table = globals()[tb_name]
            if memo_ID:
                # memo_ID가 제공된 경우 해당 메모를 바로 반환
                results = [self.session.query(table).filter(getattr(table, "메모_ID") == memo_ID).first()]
                return Connector.convert_to_json(results)
            
            results = self.session.query(table).filter(getattr(table, "작성자_ID") == search).order_by(table.작성시간.desc())
            
            if page:
                results = results.offset(int(page) * 4).all()
            else:
                results=[results.first()]
            return Connector.convert_to_json(results)
        except Exception as e:
            self.session.rollback()
            raise e
    
    def sn_persent(self, db_name, ass_id,st_id):
        try:
            ass=self.session.query(Assignment).filter(Assignment.대시보드_key==db_name).count()
            sub=self.session.query(Submission).filter(Submission.과제_ID==ass_id).filter(Submission.제출자_ID==st_id).count()
            results=(ass/sub)*100
            return results
        except Exception as e:
            # 검색 과정에서 예외가 발생하면 예외를 다시 발생시킵니다.
            raise e
    def at_sn_join(self, db_key,search=None, desc=None,page=None):
        try:
            # 쿼리를 통해 과제와 사용자 이름을 가져옵니다.
            results = self.session.query(
                Assignment,
                Userinfo.user_name,
                Submission.작성시간
            ).join(
                Submission, Assignment.과제_ID == Submission.과제_ID
            ).join(
                Userinfo, Submission.제출자_ID == Userinfo.user_id
            ).filter(
                Assignment.대시보드_key == db_key
            )
            if search:
                results=results.filter(Assignment.제목==f'%{search}%')
            if desc:
                results = results.order_by(Board.작성시간.desc())
            if page:
                results=results.offset(int(page)*6)
            results=results.limit(6).all()
            
            json_results = []
            for board, user_name,time in results:
                board_dict = board.to_dict()
                board_dict['user_name'] = user_name
                board_dict['작성시간'] = time
                json_results.append(board_dict)
            return json.dumps(json_results, ensure_ascii=False, indent=4, default=str)
        except Exception as e:
            self.session.rollback()
            raise e
    def tb_len(self, tb_name, col=None, search=None, db_key=None, today_only=None):
            session = self.session
            try:
                # 테이블 클래스를 가져옵니다.
                table = globals()[tb_name]
                query = session.query(table)
                
                # db_key 조건이 있는 경우
                if db_key is not None:
                    query = query.filter(getattr(table, "대시보드_key") == db_key)
                
                # search와 title 조건이 있는 경우
                if col is not None and search is not None:
                    query = query.filter(getattr(table, col) == search)
                
                # 오늘 날짜 조건 추가
                if today_only:
                    today = date.today()
                    query = query.filter(func.date(table.시간) == today)
                
                results = query.count()

                return results
            
            except Exception as e:
                self.session.rollback()
                raise e 
    def convert_to_list(self,objects):
        data_list = []
        for obj in objects:
            # 객체가 SQLAlchemy 결과 행인지 확인합니다.
            if hasattr(obj, '__table__'):
                data_list.append([getattr(obj, column.name) for column in obj.__table__.columns])
            else:
                # 객체가 테이블이 아닌 경우에는 그대로 추가합니다.
                data_list.append(obj)
        return data_list

    def convert_to_json(self, results):
        json_results = []
        for board in results:
            board_dict = board.to_dict()
            json_results.append(board_dict)
        return json.dumps(json_results, ensure_ascii=False, indent=4, default=str)




    # 과목, 시간표 ORM
    def fetch_timetable_data(self):
        try:
            if session['role'] == 'teacher':
                uid = session['user']['uid']
                results = self.session.query(Dashboard.과목명, Dashboard.시간표).filter(Dashboard.담당선생_ID == uid).all()

            elif session['role'] == 'student':
                uid = session['user']['uid']
                keys_results = self.session.query(Student.대시보드_key).filter(Student.uid == uid).all()
                keys = [item.대시보드_key for item in keys_results]
                results = self.session.query(Dashboard.과목명, Dashboard.시간표).filter(Dashboard.대시보드_key.in_(keys)).all()
            data = [{'과목명': result.과목명, '시간표': result.시간표} for result in results]
            return data
        except Exception as e:
            raise e




#이 파일은 기본적으로 상대주소로 작동하지 않고 한 파일내에 다 있다는 가정하에 작동되게 대기 때문에 이상이 import에 문제가 생길 수 있습니다.
if __name__ == '__main__':
    # config 파일에서 설정을 읽어옵니다. 기본설정시 app.ini의 mysql 부분을 가져옴
    config = Connector.read_config(section='postgres')
    # MySQLConnector 클래스의 인스턴스를 생성하고 구성을 전달합니다.
    conn = Connector(config)
    engine = create_engine(config)
    # SQLALCHEMY    
    
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
    

# Score.__table__.drop(engine, checkfirst=True)
# Choice.__table__.drop(engine, checkfirst=True)
# Long_answer.__table__.drop(engine, checkfirst=True)
# Short_answer.__table__.drop(engine, checkfirst=True)
# Test.__table__.drop(engine, checkfirst=True)
# Submission_attachment.__table__.drop(engine, checkfirst=True)
# Submission.__table__.drop(engine, checkfirst=True)
# Assignment_attachment.__table__.drop(engine, checkfirst=True)
# Assignment.__table__.drop(engine, checkfirst=True)
# Attachment.__table__.drop(engine, checkfirst=True)
# Comment.__table__.drop(engine, checkfirst=True)
# Board.__table__.drop(engine, checkfirst=True)
# Attendee.__table__.drop(engine, checkfirst=True)
# Dashboard.__table__.drop(engine, checkfirst=True)
# Chat.__table__.drop(engine, checkfirst=True)
# Emotion.__table__.drop(engine, checkfirst=True)
# S_memo.__table__.drop(engine, checkfirst=True)
# T_memo.__table__.drop(engine, checkfirst=True)
# Student.__table__.drop(engine, checkfirst=True)
# Teacher.__table__.drop(engine, checkfirst=True)
# Chatbot.__table__.drop(engine, checkfirst=True)
# Classdata.__table__.drop(engine, checkfirst=True)