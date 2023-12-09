import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key  = os.environ['OPENAI_API_KEY']

client = openai.OpenAI()

def get_completion(messages, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content

prompt = input('Enter your prompt> ')
messages = [ 
    {"role": "system", "content": "You are a simple problem generator"},
    {"role": "system", "content": "Avoid generating classical problems"},
    {"role": "system", "content": "Avoid generating very simple problems"},
    {"role": "system", "content": "Generate the problem in codeforces style"},
    {"role": "system", "content": "Try to make stories in the problem starement"},
    {"role": "user", "content": prompt}
]

response = get_completion(messages)
print(response)