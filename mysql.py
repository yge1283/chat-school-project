import pymysql


#로컬 DB연결
conn = pymysql.connect(
    host = 'localhost',
    user = '',      
    password= "",  #비번
    database='',   #DB이름
    charset='utf8'
)

curs = conn.cursor()

query = "SELECT * FROM 테이블명"  #sql검색어
curs.execute(query)

'''
fetchall() : 지정 테이블 안의 모든 데이터를 추출
fetchone() : 지정 테이블 안의 데이터를 한 행씩 추출
fetchmany(size=원하는 데이터 수) : 지정 테이블 안의 데이터를 size 개의 행을 추출
'''
datas = curs.fetchall()
#datas = curs.fetchone()
print(datas)