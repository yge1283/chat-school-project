from openai import OpenAI
import fitz  #PymuPDF


client = OpenAI(api_key='') #openai api key입력



file_name='lucky_dayPDF'
pdf_path = "SummaryChatbot/"+file_name+".pdf"
text=""
doc = fitz.open(pdf_path)
for page_num in range(doc.page_count):
    page = doc[page_num]
    text += page.get_text()

doc.close()

print(text)
# prompt =f'문서: {text}\n\n질문: {question}\n답변:'
def ask(question,text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system",
             "content":"A helper that receives and answers questions following \'Q:\' based on the content in \'context:\'"},
             {"role":"user",
              "content":"context:" + text+"\nQ:" + question}
        ],
        temperature=0.5,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    print("답변: "+ response.choices[0].message.content)
    return response.choices[0].message.content

ask('이 이야기의 모든 등장인물을 알려줘.',text)

'''
output:
답변: 이 이야기에 등장하는 주요 등장인물은 다음과 같습니다:
1. 김첨지: 주인공으로 인력거꾼이며 가난한 사람으로 묘사됨.
2. 치삼: 김첨지의 친구로 함께 술을 마시는 인물.
3. 김첨지의 아내: 병에 걸려 치료를 받고 있는 인물.
4. 중대가리: 선술집 주인으로 술을 판매하는 인물.
5. 여학생(마마님): 김첨지가 인력거를 태워다줄려는 여자.
6. 개똥이: 김첨지의 아이로 젖을 빼어 먹는 어린아이.
7. 주정뱅이: 김첨지의 아내로 병에 걸려
'''