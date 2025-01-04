from fake_api import *
messages=[]
system_prompt='hello'
messages.append(message_template('system',system_prompt))
messages.append(message_template('user',"你叫什么"))
answer=api_answer(messages)
print(answer)