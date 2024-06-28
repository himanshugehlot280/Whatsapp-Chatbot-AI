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

"""Wrong Code"""
# import os


# import openai
# from dotenv import load_dotenv 
# from openai import OpenAI
# load_dotenv()

# # openai.api_key = os.getenv('OPENAI_API_KEY')



# # openai.api_key = os.getenv('OPENAI_API_KEY')

# client = OpenAI(
#     api_key = os.getenv("OPENAI_API_KEY"),
# )

# def text_complition(prompt: str) -> dict:
#     '''
#     Call Openai API for text completion

#     Parameters:
#         - prompt: user query (str)

#     Returns:
#         - dict
#     '''
#     try:
#         response = client.completions.create(model='gpt-3.5-turbo-instruct',
#         prompt=prompt,
#         max_tokens=100,
#         n=1,
#         stop=None,
#         temperature=0.5)
#         return {
#         'status': 1,
#         'response': response.choices[0].text.strip()
#         } 
#     except:
#         return {
#             'status': 0,
#             'response': 'No response'
#         }