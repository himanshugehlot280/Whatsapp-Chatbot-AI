from helper.twilio_api import send_message
from flask import Flask, request, jsonify
from dotenv import load_dotenv 
from langchain_core.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain  
from langchain.memory import ConversationBufferMemory 
from langchain.llms import OpenAI
from jobs import mainjob
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

counter = 1

template = """
The following is a friendly conversation between a human and an AI. The AI acts as a recruiter.
The AI is talkative and asks the user specific details in an interactive way.

1) AI firstly asks the user's name.
2) Then the AI asks for the user's expected position.
3) Then the AI asks for the user's vessel type.
4) Then the AI asks for the user's salary expectation.
5) Finally, the AI asks for the user's citizenship.

The AI ensures to ask one question at a time and waits for the user's response before proceeding to the next question. The AI does not provide any feedback on the availability of positions; it only collects the required information.

Based on the current conversation history, the AI will determine which questions have already been answered and ask the next appropriate question.

Current conversation:
{history}
Human: {input}
AI Assistant:
"""

PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)

llm = OpenAI(
    openai_api_key=os.getenv('OPENAI_API_KEY'), 
    temperature=0.5
)

conversation = ConversationChain(
    prompt=PROMPT,
    llm=llm,
    verbose=False,
    memory=ConversationBufferMemory(human_prefix="Candidate", ai_prefix="AI"),
)

def get_next_question(history):
    if "What is your name?" not in history:
        return "Hello! What is your name?"
    elif "What position are you interested in?" not in history:
        return "Nice to meet you. What position are you interested in?"
    elif "What is your vessel type?" not in history:
        return "What is your vessel type?"
    elif "What is your salary expectation?" not in history:
        return "What is your salary expectation?"
    elif "What is your citizenship?" not in history:
        return "What is your citizenship?"
    else:
        return "Thank you for sharing all the information with me. Is there anything else you would like to add or any questions you have for me?"

user_input = "your last user input here"
history = "the conversation history here"

response = conversation({"history": history, "input": user_input}) 
print(response)
next_question = get_next_question(history)
print(next_question)

user_answers = []

@app.route('/')
def home():
    return 'All is well...'

@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():    
    try:     
        print('HI')  
        message = request.form['Body']  
        sender_id = request.form['From'] 
        print(message) 
        print(sender_id)
        # Get response from OpenAI  
        result = conversation.invoke(input=message)  
        ans = result['response'] 
        ans = ans.split('\n') 
        ans = ans[0].strip()
        user_answers.append(message)   
        print(len(user_answers))  
        if len(user_answers) % 6 == 0: 
            print(ans)
            query = str(user_answers)   
            relevant = mainjob(query)  
            send_message(sender_id, relevant) 
            return 'Valid response', 200
        else: 
            print(sender_id) 
            print(ans)
            send_message(sender_id, ans) 
        return 'Valid response', 200
    except Exception as e: 
        print(f"Error: {e}")
        return 'Error', 500

if __name__ == '__main__':
    app.run(debug=True)
