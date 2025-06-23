from googleapiclient.discovery import build
from gmail_reader import authenticate_gmail

# for testing for real time watching and email sorting 
# run webhook_handlerpy, run ngrok (ngrok http 5000 in ngrok terminal), update Pub/Sub endpoint URL for push sub, run watcher.py 

def start_gmail_watch():
    service = authenticate_gmail()
    request = {
        'labelIds': ['INBOX'],
        'topicName': 'projects/email-organizer-461719/topics/gmail-push-topic'  # Correct path
    }

    response = service.users().watch(userId='me', body=request).execute()
    print("Watch started:", response)

if __name__ == '__main__':
    start_gmail_watch()
