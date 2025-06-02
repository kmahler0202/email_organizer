# Here starts the JSA project, or the JOB SEARCH ASSISTANT PROJECT
# THIS IS THE VERSION 1 CODE. 

from openai import OpenAI

client = OpenAI()

my_assistant = client.beta.assistants.create(
    instructions="You are a personal email assistant. Your job is to ",
    name="Email Organizer",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o",
)
print(my_assistant)