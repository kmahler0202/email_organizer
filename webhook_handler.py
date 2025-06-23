from flask import Flask, request
from gmail_reader import authenticate_gmail, process_newest_message
from watcher import start_gmail_watch 

import base64, json

app = Flask(__name__)  

@app.route('/gmail_webhook', methods=['POST'])
def gmail_webhook():
    envelope = request.get_json()
    if not envelope or 'message' not in envelope:
        return 'Bad Request', 400

    pubsub_message = envelope['message']
    data = json.loads(base64.b64decode(pubsub_message['data']).decode('utf-8'))

    print("Gmail push notification received.")
    print("Decoded data:", data)

    history_id = data.get('historyId')
    if not history_id:
        return 'Missing historyId', 400

    service = authenticate_gmail()
    process_newest_message(service, history_id) 

    return '', 204

if __name__ == '__main__':
    app.run(port=5000)
