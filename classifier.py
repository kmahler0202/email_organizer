# Here starts the EMAIL ORGANIZER project
# THIS IS THE VERSION 1 CODE. 
# THIS IS THE AI CLASSIFIER V1

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def classify_email(subject, snippet):
    prompt = f"""Classify the following email into one of the categories: Work, Personal, Promotion, Spam, Newsletter, Receipt, Other.

Subject: {subject}
Body: {snippet}

Respond only with the category name."""
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
