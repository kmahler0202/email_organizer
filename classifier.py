# Here starts the EMAIL ORGANIZER project
# THIS IS THE VERSION 1 CODE. 
# THIS IS THE AI CLASSIFIER V2
# USES THE NEW OPENAI API INTERFACE

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_email(subject, snippet):
    prompt = f"""Classify the following email into one of the categories: 
                                                                            Work, 
                                                                            Personal, 
                                                                            Promotion, 
                                                                            Spam, 
                                                                            Newsletter, 
                                                                            Receipt, 
                                                                            Sportsbook, 
                                                                            Professional 
                                                                            Development, 
                                                                            Subscriptions, 
                                                                            Other.

                Subject: {subject}
                Body: {snippet}

                Respond only with the category name."""
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
