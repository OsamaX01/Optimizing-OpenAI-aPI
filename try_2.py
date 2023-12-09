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

system_message = f"""
    You are a simple problem generator. \
    Avoid classical problems. \
    Avoid very simple problems. \
    Generate the problem in codeforces style (title, problem statemnt, input section with constraints, output, exampels, test cases).  \
    Don't mention the topic in the problem statemnt \
    Provide your output in json format with the keys: title, statment, input, output, examples, test_cases \
    Try to make stories in the problem starement. \
    Generate 10 test cases with each problem including the samples. \
"""



user_message = input('Enter your prompt> ')

messages = [
    {"role": "system", "content": system_message},
    {"role": "system", "content": user_message}
]

response = get_completion(messages)
print(response)