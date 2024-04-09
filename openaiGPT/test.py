from openaiGPT3_5 import gpt

#객체 생성
gpt=gpt('')


#문제 생성 예제 txt파일을 읽고 'Q:'를 붙여 3개의 문제 생성
gpt.define_systemRole("You're a great helper for teachers teaching students. Given a teaching material, output three questions for it, each preceded by the phrase \"Q:\". And response with korean.")
with open('./sample_data/news_public_doc_kor.txt','r',encoding='utf-8') as f:
    contents = f.read()
gpt.get_response(contents)

resp = gpt.give_response().split("Q: ")
print(resp, type(resp))