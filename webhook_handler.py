from flask import Flask, request
from gmail_reader import authenticate_gmail, process_newest_message
from watcher import start_gmail_watch 

import base64, json

app = Flask(__name__)  

@app.route('/gmail_webhook', methods=['POST'])
def gmail_webhook():
    try:
        envelope = request.get_json()
        if not envelope or 'message' not in envelope:
            print("❌ Invalid Pub/Sub message: no 'message' field")
            return 'Bad Request', 400

        pubsub_message = envelope['message']
        print("🔵 Raw Pub/Sub message:", pubsub_message)

        data_field = pubsub_message.get('data')
        if not data_field:
            print("❌ Missing 'data' field in message")
            return 'Bad Request', 400

        data = json.loads(base64.b64decode(data_field).decode('utf-8'))
        print("✅ Gmail push notification received.")
        print("📬 Decoded data:", data)

        history_id = data.get('historyId')
        if not history_id:
            print("❌ Missing historyId in decoded data")
            return 'Bad Request', 400

        service = authenticate_gmail()
        process_newest_message(service, history_id)

        return '', 204

    except Exception as e:
        print(f"🔥 Error in webhook handler: {e}")
        import traceback
        traceback.print_exc()
        return 'Internal Server Error', 500


if __name__ == '__main__':
    app.run(port=5000)
