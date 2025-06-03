# GMAIL_READER, WHERE THE GMAIL API MAGIC HAPPENS
import os.path
import base64
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from classifier import classify_email

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)




def get_emails(service, max_results=100):
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = txt['payload']
        headers = payload.get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
        snippet = txt.get("snippet", "")
        label = classify_email(subject, snippet)
        print(f"Labeling as: {label}")

        print(f"Subject: {subject}\nSnippet: {snippet}\nPredicted Label: {label}\n---")

        apply_label(service, msg['id'], label)

def apply_label(service, msg_id, label_name):
    labels_res = service.users().labels().list(userId='me').execute()
    label_id = None
    for label in labels_res['labels']:
        if label['name'].lower() == label_name.lower():
            label_id = label['id']
            break
    if not label_id:
        new_label = service.users().labels().create(userId='me', body={
            'name': label_name,
            'labelListVisibility': 'labelShow',
            'messageListVisibility': 'show'
        }).execute()
        label_id = new_label['id']
    
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'addLabelIds': [label_id]}
    ).execute()


if __name__ == '__main__':
    service = authenticate_gmail()
    get_emails(service)
