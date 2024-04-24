
from openai import OpenAI

class gpt:
    '''
    객체 생성시 API키 입력하기
    '''

    def __init__(self,apikey='') -> None:      #객체 생성시 api키를 받음
        self.apikey = apikey
        self.set_token= 256                 # 출력 토큰 제한 설정
        self.totalUsed_tokens = 0
        self.systemRole ="You are a helpful educator. response with korean."
        self.response = ''
        self.historyLog=[]
        self.client = OpenAI(api_key=self.apikey)  #gpt 클라이언트 생성

    # def gpt_apiKey(self):
    #     client = OpenAI(api_key=self.apikey)
    #     return client
    
    def define_systemRole(self, role_message):
        '''
        역할 정하기(자연어로)
        role_message = (str)

        예제(기본값)>
        "You are a helpful educator. response with korean."
        '''
        self.systemRole = str(role_message)
        print(f'변경된 System Role:{self.systemRole}')
    def setApiKey(self,your_key):   #api키 변경
        self.client = OpenAI(api_key=your_key)
    
    def applyHistoryLog(self,historyLog=[]):
        '''
        이전 대화기록을 불러와 붙임
        형식은 다음과 같아야함.

        [
            {
                "role":"system"
                "role":"(ai 역할)"
            },
            {
                "role":"user"
                "content":"(유저입력)"
            },
            {
                "role":"assistance"
                "content":"(ai 답변)"
            },
            {
                "role":"user"
                "content":"(유저입력)"
            },
            ...
        ]
        '''
        self.historyLog.append(historyLog)

    def give_response(self):
        '''
        마지막 답변 불러오기
        '''
        return str(self.response)
    
    
    def get_response(self, input_message, rememberChat=False):
        '''
        gpt로부터 답변 받아오기

        input_message=(str)      입력할 채팅
        historyLog=(list)        이전 대화기록
        rememberChat=(bool)True  이전 대화 기억하여 답변
        
        '''
        if self.apikey == '':
            raise Exception("API key가 입력되지 않음")
        if self.historyLog == []:
            self.historyLog =[{
                "role": "system",
                "content": self.systemRole
            }]
        if rememberChat == True:  # 이전 채팅 기록 같이 input
            response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",   #모델3.5 고정. 
            messages=self.historyLog.append(
                {
                "role": "user",
                "content": str(input_message)
                }
            ),
            temperature=1,
            max_tokens=self.set_token,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
            self.historyLog.append(
                {
                "role": "user",
                "content": str(response.choices[0].message.content)
                })
            
        else:
            response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",   #모델3.5 고정. 변경 ㄴ
            messages=[
            {
                "role": "system",
                "content": self.systemRole
            },
            {
                "role": "user",
                "content": str(input_message)
            }
            ],
            temperature=1,
            max_tokens=self.set_token,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        
        self.totalUsed_tokens += response.usage.total_tokens # 토큰 누적사용량 기록
        self.response = response.choices[0].message.content
        return print(self.response)
