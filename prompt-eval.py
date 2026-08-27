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


# step2: eval dataset
import json
def generate_dataset():
    prompt = """
Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
each representing task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
    {
        "task": "Description of task",
    },
    ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""
    messages=[]
    add_user_message(messages, prompt)
    add_assitant_message(messages, "```json")
    text = chat(messages)
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    print(text)
    return json.loads(text)

dataset = generate_dataset()
with open("dataset.json", "w") as f:
    json.dump(dataset,f,indent=2)
# print(dataset)


