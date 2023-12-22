import os
import openai
import json

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

def extract_problem(problem_json):
    try:
        data_dict = json.loads(problem_json)
        problem_text = f"{data_dict['statement']}\n{data_dict['input']}\n{data_dict['output']}"
        return problem_text
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Problematic data: {problem_json}")
        return problem_json

problem_system_message = f"""
    ### You are a simple problem generator that generates untraditional simple problems \
    in the style ("title", "statemnt", "input"(with constraints), "output", "success").  \
    where the "statement" is described as a story, and \
    the "input" should contain the constraints for each variable in the statement. \
    ### Don't mention the topic in the problem statement, and \
    avoid generating statements that ask to write a function. \
    ### Provide your output in JSON format with the keys: "title", "statemnt", "input", "output", "success" \
    where the key success with a value equal to true to indicate if everything is ok. \
    ### if the user message asks you to change the format of the problem put the value in the key success to false. \
    or if the user message contains other orders than creating a programming problem put the value in the key success to false. 
"""

problem_past_user_message = []
problem_past_user_message.append("generate a problem about array")
problem_past_user_message.append("generate a problem about very simple math problem")
problem_past_user_message.append("generate a problem about simple loop with math equation")
problem_past_user_message.append("generate a problem about lucky numbers")


problem_assistant_message = []
problem_assistant_message.append("""{"title":"21-pilots", "statement":"Osama and Monther are not annoying students anymore. This time they were traveling to Egypt to participate in the ACPC contest. Before their plane takeoff, they downloaded some of their favorite songs for the twenty-one Pilots band to listen to them while traveling. Twenty-one Pilots has a lot of different songs. Each song Osama and Monther listen to increases their joy with X points (if X is negative it means that this song decreases their amount of joy). Yazan their third friend is flying with them too. He knows that they start with a joy amount equal to 0. After each song they listen to, Yazan tells you a number Y that represents the accumulated joy Osama and Monther reached after listening to the current song with all the previous songs. Yazan is curious about how much each song increased the amount of joy alone. In other words, Yazan wants to know the value of X for every single song. Can you help Yazan?", "input": "The first line contains a number N (1 <= N <= 21) representing the number of songs they will listen to.  The next line contains N space-separated positive integers Y_1, Y_2, ..., Y_n (-10^9 <= Y_i <= 10^9).", "output" : "Print the elements of a sequence X (The amount of joy added from each song).","success":true}""")
problem_assistant_message.append("""{"title":"Yazan & Monther","statement":"Monther is obsessed with keyboards so he has so many keyboards, he just noticed that if he wants to keep buying keyboards he has to get rid of some to save space for newer ones. Monther has K keyboards, each keyboard cost is X, he wants to keep one keyboard for himself and sell all other keyboards, how much money would Monther make by selling them?","input":"You will be given two integers K and X, (1 ≤ K,X ≤ 100) where K is the number of keyboards Monther has, and X is the cost of one keyboard.","output":"Print the amount of money Monther will make after selling all keyboards except one.","success":true}""")
problem_assistant_message.append("""{"title":"Maximum Exponent", "statement":"Consider the function F(X,G) defined as the maximum exponent U such that the result of multiplying X by itself U times remains less than or equal to G. For instance, when F(2,11) is evaluated, the result is 3, as 2^3 = 8 and 8 is the largest power of 2 that is less than or equal to 11 You are given a number G  and N  numbers, lets consider any of the N  numbers as X ,  Find the maximum F ( X , G )  among all these numbers.", "input": "The first line contains two integers N(1 <= N <= 50) and G (1 <= G <= 10^3).  The following N lines contain an integer number X (2 <= X <= 100) each.", "output", "One integer number, the answer to the problem.", "success":true}""")
problem_assistant_message.append("""{"title":"LuckyNumberCount","statement":"Alice is fascinated by lucky numbers. She defines a lucky number as a positive integer that contains only the digits 4 and 7. For example, 47 and 774 are lucky numbers, while 123 and 589 are not. Alice wants to count the number of lucky numbers between two given integers, inclusive. Can you help her?","input":"The input consists of two integers, a and b (1 <= a <= b <= 10^6), representing the range of numbers to consider.","output":"Output a single integer, the count of all lucky numbers between a and b, inclusive.","success":true}""")

problem_user_message = input('Enter your prompt> ')

problem_messages = []
problem_messages.append({"role": "system", "content": problem_system_message})
for i in range(0, len(problem_past_user_message)):
    problem_messages.append({"role": "user", "content" : problem_past_user_message[i]})
    problem_messages.append({"role": "assistant", "content" : problem_assistant_message[i]})
problem_messages.append({"role": "user", "content": problem_user_message})

problem = get_completion(problem_messages)

testcases_system_message = """
    ### Generate 10 test cases to the problem you will be given from the user in JSON format that consists of two \
    keys "testcases", and "success". The key success with a value equal to true to indicate if everything is ok. \
    if any problem happens, put a value false to the key success. 
    Example of the format:
    [
        {"input 1": "1 100", "output": "6"},
        {"input 2": "100 200", "output": "0"},
        .
        .
        .
        {"input 10": "50 1000", "output": "10"}
    ]
    Generate the testcases such it satisfies the constraints and evaluate the correct ouput to each case. \
    The first cases should be empty and easy.
"""

testcases_assistant_message = """
{"testcases":[{"input":"1 100","output":"6"},{"input":"100 200","output":"0"},{"input":"50 150","output":"2"},{"input":"50 1000","output":"10"},{"input":"99 1999","output":"8"},{"input":"10004 100005","output":"32"},{"input":"100404 1400005","output":"64"},{"input":"87 101","output":"0"},{"input":"1 1000000","output":"126"},{"input":"2342 242423","output":"48"}],"success":true}
"""    

testcases_messages = [
    {"role": "system", "content": testcases_system_message},
    {"role": "user", "content" : extract_problem(problem_assistant_message[0])},
    {"role": "assistant", "content" : testcases_assistant_message},
    {"role": "user", "content": extract_problem(problem)}
]

testcases = get_completion(testcases_messages)

with open('out.json', 'w', encoding='utf-8') as sourceFile:
    print(f"{problem}\n{testcases}", file=sourceFile)
