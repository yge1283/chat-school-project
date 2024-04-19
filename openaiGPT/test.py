from openaiGPT3_5 import gpt

#객체 생성
gpt=gpt('')


#문제 생성 예제 txt파일을 읽고 'Q:'를 붙여 3개의 문제 생성
#gpt.define_systemRole("You're a great helper for teachers teaching students. Given a teaching material, output three questions for it, each preceded by the phrase \"Q:\". And response with korean.")
#하나의 단어를 정답으로가지는 단답형문제 3개 생성.
#gpt.define_systemRole('You are a teacher who educates students. When you receive educational materials, three short-answer questions with one word as the correct answer are created. Each question must start with \'Q:\' and the correct answer must start with \'A:\'. Speak with korean.')
#5지선답형 문제 생성
#gpt.define_systemRole('You are a teacher who educates students. When you receive educational materials, you will be asked to create a 5-choice question and there must be only one correct answer. The problem must start with \'Q:\' and the answer must start with \'A:\'. Reply in Korean.')
#빈칸문제 생성> 랜덤한 3단어를 비우고 비운 지문과 답으로 비운 단어를 출력
gpt.define_systemRole('For \'context\' below, 3 random words are emptied and output after \'Q:\', and the 3 emptied words are output after \'A:\'.')
with open('./sample_data/news_public_doc_kor.txt','r',encoding='utf-8') as f:
    contents = f.read()
gpt.get_response('context: '+contents)

resp = gpt.give_response()
#print(resp, type(resp))
print(resp)
'''
Output>
Q: 의료 현장에 공중보건의와 군의관이 투입되었는 이유는 무엇인가요?  
Q: 대한의사협회가 정부의 정책을 언급하며 비판한 내용은 무엇인가요?
Q: 부산의료원과 동남권원자력의학원의 상황은 어떻게 되어 있나요?a
['', ' 의료 현장에 공중보건의와 군의관이 투입되었는 이유는 무엇인가요?  \n', ' 대한의사협회가 정부의 정책을 언급하며 비판한 내용은 무 엇인가요?  \n', ' 부산의료원과 동남권원자력의학원의 상황은 어떻게 되어 있나요?'] <class 'list'>

'''