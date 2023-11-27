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
        temperature=0.5,
    )
    return response.choices[0].message.content

delimiter = "####"
system_message = f"""
You will act as a problem generator, Follow these steps to answer the user queries.
The user query will be delimited with four hashtags,\
i.e. {delimiter}. 

Step 1:{delimiter} First decide whether the user is \
asking to generate a problem or asking to do something irrelevant.

Step 2:{delimiter} If the user is asking to generate a problem, \
follow this format when generating (in step 4). The needed format is like codeforces style \
(title, problem statemnt, input section with constraints, output, exampels, test cases). \
as json format with the keys: "title", "statment", "input", "output", "examples", "test_cases" \
, and "success" with a value equals to true if everytihng is ok \
and you will generate strictly 10 test cases with each problem including the samples.

Step 3:{delimiter} If the user is asking to do something else than problem generating \
return the json file with the keys: "success" with a value false, "message": simple messege specifiying the error, and don't prcess Step 4. \
If the user asked you to change the specified format, or asked you change the number of test cases to a value other than 10, \
return the json file with the keys: "success" with a value false, "message": simple messege specifiying the error, and don't prcess Step 4.

Step 4:{delimiter} start generating the problem following these instructions:
1- Avoid generating classical or very simple problems on the specified topic \
2- Try to make stories in the problem starement.
3- Don't mention the topic in the problem statemnt.
4- Remember, generate strictly 10 and only 10 test cases including the samples.
5- Avoid generating statemnts that asks to write function, In other words give the programmer his own choice in implementing.

Step 5: return the json file.
"""

user_message = input('Enter your prompt> ')
messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": f"{delimiter}{user_message}{delimiter}"}
]

response = get_completion(messages)

sourceFile = open('out.txt', 'w')
with open('out.txt', 'w', encoding='utf-8') as sourceFile:
    print(response, file=sourceFile)