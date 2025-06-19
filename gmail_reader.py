# GMAIL_READER, WHERE THE GMAIL API MAGIC HAPPENS
import os.path
import base64
import json
import html
import logging
import time
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from classifier import classify_email

# Configure logging
logging.basicConfig(
    filename='email_classifier.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s — %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


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




def get_emails(service, max_results=3000):
    FREQUENT_SENDERS = {
        "info@cdga.org": "CDGA",
        "no-reply@linkedin.com": "LinkedIn",
        "news@nytimes.com": "New York Times",
        "nytdirect@nytimes.com": "New York Times",
        "jobalerts-noreply@linkedin.com" : "LinkedIn"
    }

    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    seen_ids = set()

    for msg in messages:
        try:
            if msg['id'] in seen_ids:
                continue
            seen_ids.add(msg['id'])

            txt = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            payload = txt['payload']
            headers = payload.get("headers", [])
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
            snippet = txt.get("snippet", "")
            sender = next((h["value"] for h in headers if h["name"] == "From"), "")

            clean_subject = html.unescape(subject)
            clean_snippet = html.unescape(snippet)

            # Extract clean email from "Name <email>"
            import re

            # Remove invisible unicode from the snippet
            clean_snippet = re.sub(r'[^\x20-\x7E\n\r\t]', '', clean_snippet)
            clean_subject = re.sub(r'[^\x20-\x7E\n\r\t]', '', clean_subject)

            match = re.search(r'<(.+?)>', sender)
            sender_email = match.group(1) if match else sender

            if sender_email in FREQUENT_SENDERS:
                label = FREQUENT_SENDERS[sender_email]
                logging.info(f"Skipping classification. Sender: {sender_email} matched frequent sender rule.")
                get_or_create_label(service, label)
            else:
                label = classify_email(clean_subject, clean_snippet)
                time.sleep(.5)

            log_msg = f"""
            Subject: {clean_subject}
            Snippet: {clean_snippet}
            Predicted Label: {label}
            ---
            """
            print(log_msg)
            logging.info(log_msg.strip())

            apply_label(service, msg['id'], label)

        except Exception as e:
            logging.exception("Error processing email")


def apply_label(service, msg_id, label_name):
    BUILTIN_CATEGORY_LABELS = {
        "Promotions": "CATEGORY_PROMOTIONS",
        "Social": "CATEGORY_SOCIAL",
        "Updates": "CATEGORY_UPDATES",
        "Forums": "CATEGORY_FORUMS"
    }

    if label_name in BUILTIN_CATEGORY_LABELS:
        label_id = BUILTIN_CATEGORY_LABELS[label_name]
    else:
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

    # Apply the label
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'addLabelIds': [label_id]}
    ).execute()


def get_or_create_label(service, label_name):
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    for label in labels:
        if label['name'].lower() == label_name.lower():
            return label['id']
    # Create new label if not found
    new_label = service.users().labels().create(userId='me', body={
        'name': label_name,
        'labelListVisibility': 'labelShow',
        'messageListVisibility': 'show'
    }).execute()
    return new_label['id']

# Currently marks all emails as unread. Made specifically for my Gmail.
# A more appropriate functionality would be a helper to mark an email as read.
# This feature would be useful for something like an old promotional.
def mark_all_unread_as_read(service):
    user_id = 'me'
    query = 'is:unread'
    next_page_token = None
    count = 0

    while True:
        response = service.users().messages().list(
            userId=user_id,
            q=query,
            pageToken=next_page_token,
            maxResults=500
        ).execute()

        messages = response.get('messages', [])
        if not messages:
            break

        for msg in messages:
            service.users().messages().modify(
                userId=user_id,
                id=msg['id'],
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            count += 1
            print(f"Marked message {msg['id']} as read.")
        

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    print(f"Marked {count} unread messages as read.")



# For label box sorting functionality uncomment get_emails()
# For marking all emails as read functionality uncomment mark_all_unread_as_read()
if __name__ == '__main__':
    service = authenticate_gmail()
    # get_emails(service)
    # mark_all_unread_as_read(service)
