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

'''
Output>
Q: 의료 현장에 공중보건의와 군의관이 투입되었는 이유는 무엇인가요?  
Q: 대한의사협회가 정부의 정책을 언급하며 비판한 내용은 무엇인가요?
Q: 부산의료원과 동남권원자력의학원의 상황은 어떻게 되어 있나요?
['', ' 의료 현장에 공중보건의와 군의관이 투입되었는 이유는 무엇인가요?  \n', ' 대한의사협회가 정부의 정책을 언급하며 비판한 내용은 무 엇인가요?  \n', ' 부산의료원과 동남권원자력의학원의 상황은 어떻게 되어 있나요?'] <class 'list'>

'''