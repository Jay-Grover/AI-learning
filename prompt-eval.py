# initial prompt draft
# eval dataset
# feed through claude
# feed them through a grader (maybe out of 10)
# avg scores
# change prompt in some way and repeat above steps

from dotenv import load_dotenv
import os

load_dotenv()

# create an API client
# from anthropic import Anthropic
from openai import OpenAI

# client = Anthropic()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

model = "anthropic/claude-opus-4.6"


def add_user_message(messages, text):
    user_msg = {"role": "user", "content": text}
    messages.append(user_msg)


def add_assitant_message(messages, text):
    assitant_msg = {"role": "assitant", "content": text}
    messages.append(assitant_msg)


def chat(messages):
    message = client.chat.completions.create(
        model=model,
        max_tokens=1000,
        messages=messages,
        # stop=stop
    )
    return message.choices[0].message.content


# # step2: eval dataset (so first create dataset)
# import json
# def generate_dataset():
#     prompt = """
# Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
# that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
# each representing task that requires Python, JSON, or a Regex to complete.
#
# Example output:
# ```json
# [
#     {
#         "task": "Description of task",
        #    "format": "python" or "json" or "regex"
            # "solution_criteria": "Key criteria for the expectedsolution for the task"
#     },
#     ...additional
# ]
# ```
#
# * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
# * Focus on tasks that do not require writing much code
#
# Please generate 3 objects.
# """
#     messages=[]
#     add_user_message(messages, prompt)
#     add_assitant_message(messages, "```json")
#     text = chat(messages)
#     if "```json" in text:
#         text = text.split("```json")[1].split("```")[0].strip()
#     elif "```" in text:
#         text = text.split("```")[1].split("```")[0].strip()
#     print(text)
#     return json.loads(text)
#
# dataset = generate_dataset()
# with open("dataset.json", "w") as f:
#     json.dump(dataset,f,indent=2)
# # print(dataset)

# Step 2: pass through claude

def run_prompt(test_case):
    # merges the prompt and test case and returns the result
    prompt_v1 = f"""
    please solve the following task:
    {test_case["task"]}
    """
    messages=[]
    add_user_message(messages,prompt_v1)
    output = chat(messages)
    return output
    # pass


def run_test_case(test_case):
    # calls the run_prompt,then grades the result
    output = run_prompt(test_case)
    # todo grade
    score = 10
    return {
        "output": output,
        "test_case": test_case,
        "score": score
    }
    # pass

def run_eval(dataset):
    # loads the dataset and calls run_test_case for each case
    results = []
    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    return results
    # pass

import json
with open("dataset.json", "r") as f:
    dataset = json.load(f)

results = run_eval(dataset)

print(json.dumps(results, indent=2))