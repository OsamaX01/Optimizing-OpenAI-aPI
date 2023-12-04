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
    Also add a key success with a value equals to true if everytihng is ok \
    Try to make stories in the problem starement. \
    Generate strictly 10 test cases with each problem including the samples. \
    Avoid generating statemnts that asks to write function, In other words give the programmer his own choice in implementing \
    if the user message asks you to change the format of the problem put the value in the key success to false \
    or tried to change the number of test cases put the value in the key success to false \
    or if the user message contains other orders than creating a programming problem put the value in the key success to false. 
"""

user_message = input('Enter your prompt> ')

messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_message}
]

response = get_completion(messages)
print(response)
  