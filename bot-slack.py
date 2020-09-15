#!/usr/bin/env python

from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
from backend import do_secret_job


load_dotenv()
SLACK_VERIFICATION_TOKEN = os.environ['SLACK_VERIFICATION_TOKEN']
BOT_SECRET = os.getenv('BOT_SECRET')

app = Flask(__name__)

@app.route('/',methods=['POST'])
@app.route('/mc', methods=['POST'])
def slash():
    if request.form['token'] == SLACK_VERIFICATION_TOKEN:
        user = request.form['user_name']
        text = request.form['text']
        channel_name = request.form['channel_name']
        print(f"User: {user} says: {text}")
        
        if channel_name != "minecraft":
            payload = {'text': f'must run from #minecraft'}
        else:
            if text == BOT_SECRET:
                do_secret_job()
                payload = {'text': f'MC server started!! by @{user}'}
            else:
                payload = {'text': f'invalid secret!'}
            
        return jsonify(payload)

if __name__ == '__main__':
    app.run(port=8080)

