# Here starts the EMAIL ORGANIZER project
# THIS IS THE VERSION 1 CODE. 
# THIS IS THE AI CLASSIFIER V1

import os
from dotenv import load_dotenv

load_dotenv()
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()

my_assistant = client.beta.assistants.create(
    instructions="You are a personal email assistant. Your job is to ",
    name="Email Organizer",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o",
)
print(my_assistant)