from sqlalchemy import  Column, Integer,Float, String, Date, DateTime, ForeignKey,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()

class Teacher(Base):
    __tablename__ = '선생'

    선생_ID = Column(Integer, primary_key=True, autoincrement=True)
    성별 = Column(String(255))
    이름 = Column(String(255))
    생년월일 = Column(Date)
    이메일 = Column(String(255))

    dashboard = relationship("Dashboard", backref="teacher", cascade="all, delete-orphan")
    comment = relationship("Comment", cascade="all, delete-orphan")
    assignment = relationship("Assignment", cascade="all, delete-orphan")
    t_memo= relationship("T_Memo", cascade="all, delete-orphan")

class Student(Base):
    __tablename__ = '학생'

    학생_ID = Column(Integer, primary_key=True, autoincrement=True)
    성별 = Column(String(255))
    이름 = Column(String(255))
    생년월일 = Column(Date)
    휴대폰번호 = Column(String(255))
    학년 = Column(Integer)
    학급 = Column(Integer)

    boards = relationship("Board", cascade="all, delete-orphan")
    comment = relationship("Comment", cascade="all, delete-orphan")
    chat = relationship("Chat", cascade="all, delete-orphan")
    submission = relationship("Submission", cascade="all, delete-orphan")
    s_Memo= relationship("S_Memo", cascade="all, delete-orphan")
    score= relationship("Score")

class S_memo(Base):
    __tablename__ = '학생_메모장'

    메모_ID = Column(Integer, primary_key=True)
    작성자_ID = Column(Integer, ForeignKey('학생.학생_ID'))
    제목 = Column(String(50))
    내용 = Column(String(50))
    작성시간 = Column(DateTime)

class T_memo(Base):
    __tablename__ = '선생_메모장'

    메모_ID = Column(Integer, primary_key=True)
    작성자_ID = Column(Integer, ForeignKey('선생.선생_ID'))
    제목 = Column(String(50))
    내용 = Column(String(50))
    작성시간 = Column(DateTime)

class Emotion(Base):
    __tablename__ = '감정'

    감정_ID = Column(Integer, primary_key=True, autoincrement=True)
    학생_ID = Column(Integer, ForeignKey('학생.학생_ID'))
    감정 = Column(String(50))
    날짜 = Column(Integer)

class Chat(Base):

    __tablename__ = '채팅'

    채팅_ID = Column(Integer, primary_key=True, autoincrement=True)
    학생_ID = Column(Integer, ForeignKey('학생.학생_ID'))
    시간 = Column(DateTime)
    질문 = Column(String(255))
    챗봇응답 = Column(String(255))

class Dashboard(Base):
    __tablename__ = '대시보드'

    대시보드_key = Column(Integer, primary_key=True, autoincrement=True)
    담당선생_ID = Column(Integer, ForeignKey('선생.선생_ID'))
    과목명 = Column(String(255))
    학년 = Column(Integer)
    학급 = Column(Integer)
    
    teacher = relationship("Teacher", backref="dashboard")
    timetable = relationship("Timetable", cascade="all, delete-orphan")
class Timetable(Base):
    __tablename__ = '시간표'

    시간표_ID = Column(Integer, primary_key=True, autoincrement=True)
    대시보드_key = Column(Integer, ForeignKey('대시보드.대시보드_key'))
    요일 = Column(String(50))
    시간 = Column(Date)

class Board(Base):
    __tablename__ = '게시판'

    게시물_ID = Column(Integer, primary_key=True, autoincrement=True)
    대시보드_key = Column(Integer, ForeignKey('대시보드.대시보드_key'))
    학생_ID = Column(Integer, ForeignKey('학생.학생_ID'))
    제목 = Column(String(255))
    작성내용 = Column(String(255))
    작성시간 = Column(DateTime)

    student = relationship("Student")
    dashboard = relationship("Dashboard")
    comments = relationship("Comment", cascade="all, delete-orphan")
    attachment = relationship("Attachment", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = '댓글'

    댓글_ID = Column(Integer, primary_key=True, autoincrement=True)
    게시물_ID = Column(Integer, ForeignKey('게시판.게시물_ID'))
    선생_ID = Column(Integer, ForeignKey('선생.선생_ID'))
    학생_ID = Column(Integer, ForeignKey('학생.학생_ID'))
    내용 = Column(String(255))
    댓글시간 = Column(DateTime)

class Attachment(Base):
    __tablename__ = '첨부파일'

    파일_ID = Column(Integer, primary_key=True, autoincrement=True)
    게시물_ID = Column(Integer, ForeignKey('게시판.게시물_ID'))
    파일명 = Column(String(255))
    파일경로 = Column(String(255))
    시간 = Column(DateTime)

class Assignment(Base):
    __tablename__ = '과제'

    과제_ID = Column(Integer, primary_key=True, autoincrement=True)
    대시보드 = Column(Integer, ForeignKey('대시보드.대시보드_key'))
    주차 = Column(Integer)
    제목 = Column(String(25))
    내용 = Column(Text)
    기한 = Column(Date)
    유형 = Column(String(5))

    attachment = relationship("Assignment_attachment", cascade="all, delete-orphan")
    submission=relationship("Submission", cascade="all, delete-orphan")

class Assignment_attachment(Base):
    __tablename__ = '과제_첨부파일'

    파일_ID = Column(Integer, primary_key=True, autoincrement=True)
    게시물_ID = Column(Integer, ForeignKey('과제.과제_ID'))
    파일명 = Column(String(255))
    파일경로 = Column(String(255))
    시간 = Column(DateTime)

class Submission(Base):
    __tablename__ = '제출물'

    제출물_ID = Column(Integer, primary_key=True, autoincrement=True)
    제출자_ID = Column(Integer, ForeignKey('학생.학생_ID'))
    과제_ID = Column(Integer, ForeignKey('과제.과제_ID'))
    제목 = Column(String(25))
    내용 = Column(Text)
    점수 = Column(Integer)

    attachment = relationship("Submission_attachment", cascade="all, delete-orphan")

class Submission_attachment(Base):
    __tablename__ = '제출물_첨부파일'

    파일_ID = Column(Integer, primary_key=True, autoincrement=True)
    게시물_ID = Column(Integer, ForeignKey('제출물.제출물_ID'))
    파일명 = Column(String(255))
    파일경로 = Column(String(255))
    시간 = Column(DateTime)

class Test(Base):
    __tablename__ = '시험'

    시험_ID = Column(Integer, primary_key=True, autoincrement=True)
    대시보드_key = Column(Integer, ForeignKey('대시보드.대시보드_key'))
    문제_순서= Column(Integer)
    시간 = Column(Date)

    choice = relationship("Choice", cascade="all, delete-orphan")
    Long_answer = relationship("Long_answer", cascade="all, delete-orphan")
    lhort_answer = relationship("Short_answer", cascade="all, delete-orphan")
    score = relationship("Score", cascade="all, delete-orphan")

class Score(Base):
    __tablename__ = '점수'

    점수_ID = Column(Integer, primary_key=True, autoincrement=True)
    시험_ID=Column(Integer, ForeignKey('시험.시험_ID'))
    학생_ID=Column(Integer, ForeignKey('학생.학생_ID'))
    점수=Column(Integer)

class Choice(Base):
    __tablename__ = '객관식'

    문제_ID = Column(Integer, primary_key=True, autoincrement=True)
    시험_ID = Column(Integer, ForeignKey('시험.시험_ID'))
    문제질문 = Column(String(255))
    문제내용 = Column(Text)
    보기1 = Column(String(255))
    보기2 = Column(String(255))
    보기3 = Column(String(255))
    보기4 = Column(String(255))
    보기5 = Column(String(255))
    정답 = Column(String(50))

class Long_answer(Base):
    __tablename__ = '주관식'

    문제_ID = Column(Integer, primary_key=True, autoincrement=True)
    시험_ID = Column(Integer, ForeignKey('시험.시험_ID'))
    문제질문 = Column(String(255))
    문제내용 = Column(Text)
    문제질문 = Column(String(255))
    정답 = Column(String(50))


class Short_answer(Base):
    __tablename__ = '단답식'

    문제_ID = Column(Integer, primary_key=True, autoincrement=True)
    시험_ID = Column(Integer, ForeignKey('시험.시험_ID'))
    문제질문 = Column(String(255))
    문제내용 = Column(Text)
    빈칸개수 = Column(Integer)
    빈칸1의정답 = Column(String(50))
    빈칸2의정답 = Column(String(50))
    빈칸3의정답 = Column(String(50))
    빈칸4의정답 = Column(String(50))
    빈칸5의정답 = Column(String(50))

class Chatbot(Base):
    __tablename__ = '챗봇'

    챗봇_ID = Column(Integer, primary_key=True, autoincrement=True)
    대시보드 = Column(Integer, ForeignKey('대시보드.대시보드_key'))
    주차 = Column(Float)
    추가시간 = Column(Date)
    내용 = Column(Text)
