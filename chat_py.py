
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
import os
from dotenv import load_dotenv
load_dotenv()

#
os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")
def message_template(role,new_info):
    new_dict={'role':role,'content':new_info}
    return new_dict

GPT_MODEL = "gpt-4o-mini"
client = OpenAI()

def api_answer(messages,mode="",model="gpt-4o"):
    if mode=="json":

        response = client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            temperature=0,
            messages=messages
        )
    elif mode == 'stream':
        response = client.chat.completions.create(
        model=model,
        messages=messages,
            temperature=0,
        stream=True,
            max_tokens=2560

    )
        return response
    else:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        temperature = 0,
            max_tokens=8192
        )
    print(response.choices[0].message.content)
    return response.choices[0].message.content