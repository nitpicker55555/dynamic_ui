# from fake_api import *
from chat_py import *
def know_data_agent(query):
    messages=[]

    messages.append(message_template('user',query))
    know_data_agent_response=api_answer(messages,'json')
    print(know_data_agent_response)

know_data_agent('今天有多少笔画？回复json')
