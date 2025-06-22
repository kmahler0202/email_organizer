from flask import Flask, request
from gmail_reader import authenticate_gmail, get_emails

app = Flask(__name__)

@app.route('/gmail_webhook', methods=['POST'])
def gmail_webhook():
    print("New Gmail activity notification received.")
    service = authenticate_gmail()
    get_emails(service)  # Necessary?
    return '', 204

if __name__ == '__main__':
    app.run(port=5000)
