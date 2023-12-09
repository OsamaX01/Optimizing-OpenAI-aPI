import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
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
    ### You are a simple problem generator that generates untraditional simple problems \
    in the style ("title", "statemnt", "input"(with constraints), "output", "exampels", "testcases", "success").  \
    where the "statement" is described as a story, and \
    the "input" should contain the constraints for each variable in the statement. \
    ### Don't mention the topic in the problem statement, and \
    avoid generating statements that ask to write a function. \
    ### Generate 10 test cases with each problem including the samples, and \
    the test cases should be a plain value only with no extra words or punctuation marks or Python lists [], and \
    make sure that the test cases follows the constraints. \
    ### Provide your output in JSON format with the keys: "title", "statemnt", "input", "output", "exampels", "testcases", "success" \
    where the key success with a value equal to true to indicate if everything is ok. \
    ### if the user message asks you to change the format of the problem put the value in the key success to false. \
    or if the user tried to change the number of test cases put the value in the key success to false. \
    or if the user message contains other orders than creating a programming problem put the value in the key success to false. 
"""

old_user_message = "generate a problem about lucky numbers"
assistant_message = """
{"title":"LuckyNumberCount","statement":"Alice is fascinated by lucky numbers. She defines a lucky number as a positive integer that contains only the digits 4 and 7. For example, 47 and 774 are lucky numbers, while 123 and 589 are not. Alice wants to count the number of lucky numbers between two given integers, inclusive. Can you help her?","input":"The input consists of two integers, a and b (1 <= a <= b <= 10^6), representing the range of numbers to consider.","output":"Output a single integer, the count of all lucky numbers between a and b, inclusive.","exampels":[{"input":"1 100","output":"6"},{"input":"100 200","output":"0"}],"testcases":[{"input":"1 100","output":"6"},{"input":"100 200","output":"0"},{"input":"50 150","output":"2"},{"input":"50 1000","output":"10"},{"input":"99 1999","output":"8"},{"input":"10004 100005","output":"32"},{"input":"100404 1400005","output":"64"},{"input":"87 101","output":"0"},{"input":"1 1000000","output":"126"},{"input":"2342 242423","output":"48"}],"success":true}
"""

user_message = input('Enter your prompt> ')

messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content" : old_user_message},
    {"role": "assistant", "content" : assistant_message},
    {"role": "user", "content": user_message}
]

response = get_completion(messages)

with open('out.json', 'w', encoding='utf-8') as sourceFile:
    print(response, file=sourceFile)
