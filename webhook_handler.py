from flask import Flask, request
from gmail_reader import authenticate_gmail, get_emails

app = Flask(__name__)

@app.route('/gmail_webhook', methods=['POST'])
def gmail_webhook():
    print("Gmail push notification received.")
    service = authenticate_gmail()
    get_emails(service)  # Reuse your existing logic -- FUNCTIONAL
    return '', 204  # Must return 200/204 to acknowledge success, CHECK GPT'S CORRECTNESS HERE FOR ACK #

if __name__ == '__main__':
    app.run(port=5000)
