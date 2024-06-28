import os

from openai import OpenAI
import openai
from dotenv import load_dotenv
load_dotenv()


# openai.api_key = os.getenv('OPENAI_API_KEY')


client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
)

"""Git hub Code"""
def text_complition(prompt: str) -> dict: 
    try:
        response = client.completions.create(model='gpt-3.5-turbo-instruct',
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5)
        return {
        'status': 1,
        'response': response.choices[0].text.strip()
        } 
    except Exception as e:
        return {
            'status': 0,
            'response': str(e)
        }


anse = text_complition("WHAT IS AI") 
print(anse)