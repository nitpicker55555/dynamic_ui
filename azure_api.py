import os
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()
client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),
  api_version="2024-02-01"
)



def message_template(role,new_info):
    new_dict={'role':role,'content':new_info}
    return new_dict


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