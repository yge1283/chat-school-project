import pymysql


#로컬 MySQL DB연결
#현재 로컬로만 연결되기에 본인 컴퓨터에 아래 정보가 다르면 작동x, 아님 본인걸로 수정.
conn = pymysql.connect(
    host = 'localhost',
    user = 'root',     #user이름
    password= "0000",  #비번
    database='chatbot',   #DB이름
    charset='utf8'
)

# curs = conn.cursor()

# query = "SELECT * FROM 선생"  #sql검색어 "SELECT * FROM 테이블명"
# curs.execute(query)

'''
fetchall() : 지정 테이블 안의 모든 데이터를 추출
fetchone() : 지정 테이블 안의 데이터를 한 행씩 추출
fetchmany(size=원하는 데이터 수) : 지정 테이블 안의 데이터를 size 개의 행을 추출
'''
# datas = curs.fetchall()
# #datas = curs.fetchone()
# print(datas)