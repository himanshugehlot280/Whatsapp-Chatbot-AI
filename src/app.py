from helper.openai_api import text_complition
from helper.twilio_api import send_message


import logging
from flask import Flask, request, jsonify






from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)


@app.route('/')
def home():
    return 'All is well...'


@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():  
    try:
        data = request.get_json()
        sender_id = data.get('sender_id')
        message = data.get('message')
        print(sender_id , message)
        # Get response from Openai
        result = text_complition(message)
        if result['status'] == 1: 
            send_message(sender_id, result['response'])
        return result, 200
    except:
        pass


# @app.route('/twilio/receiveMessage', methods=['POST'])
# def receiveMessage():
#     try:
#         # Extract incoming parameters from Twilio
#         message = request.form['Body']
#         sender_id = request.form['From']

#         # Log the received message and sender ID
#         logging.debug(f"Received message: {message}")
#         logging.debug(f"Sender ID: {sender_id}")

#         # Get response from OpenAI
#         result = text_complition(message)
#         if result['status'] == 1:
#             logging.debug(f"OpenAI response: {result['response']}")
#             send_message(sender_id, result['response'])
#         else:
#             logging.error(f"Failed to get response from OpenAI: {result['response']}")
#     except Exception as e:
#         logging.exception("Error handling Twilio message:")
#     return 'OK', 200