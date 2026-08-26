# load env var
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

# make a request
# message = client.chat.completions.create(
#     model=model,
#     max_tokens=100,
#     messages=[
#         {
#             "role": "user",
#             "content": "What is quantum computing? Answer in one sentence."
#         }
#     ]
# )
#
# print(message.choices[0].message.content)

# now claude can not store message sent and received so for multi msg convo we need to store it and pass it in each call
def add_user_message(messages, text):
    user_msg = {"role": "user", "content": text}
    messages.append(user_msg)

def add_assitant_message(messages, text):
    assitant_msg = {"role": "assitant", "content": text}
    messages.append(assitant_msg)

def chat(messages, stop):
    message = client.chat.completions.create(
        model=model,
        max_tokens=100,
        messages=messages,
        stop=stop
        # temperature=temperature # 1 means randomness incre, 0 means very deterministic o/p
    #     messages=[
    #     {"role": "system", "content": system},*messages
    # ]
    )
    return message.choices[0].message.content

# messages = []
#
# add_user_message(messages, "Define quantum computing in one sentence")
#
# answer = chat(messages)
#
# add_assitant_message(messages, answer)
#
# add_user_message(messages, "Write another sentence")
#
# answer = chat(messages)
# print(answer)

# messages = []
#
# while True:
#     msg = input("> ")
#     print(">", msg)
#     add_user_message(messages, msg)
#     answer = chat(messages)
#     add_assitant_message(messages, answer)
#     print("---")
#     print(messages)
messages = []
# system = '''
# You are a software engineer.
# Give code as concise as possible'''

# add_user_message(messages, "How do I solve 5x + 3 = 2 for x?")
# answer = chat(messages, system) # systems can not be none since it is a paramter to in-built function, so we can if not none add to params else params would be first 3 arguments
# print(answer)

# add_user_message(messages, "write a python function that checks a string for duplicate characters")
# answer = chat(messages, system) # systems can not be none since it is a paramter to in-built function, so we can if not none add to params else params would be first 3 arguments
# print(answer)
# add_user_message(messages, "create a one liner story idea")
# answer = chat(messages, temperature=1.0) # systems can not be none since it is a paramter to in-built function, so we can if not none add to params else params would be first 3 arguments
# print(answer)

# stream so we get response without having to wait for entire block
# add_user_message(messages, "create a one liner story idea")

# with client.chat.completions.create(
#     model=model,
#     max_tokens=100,
#     messages=messages,
#     stream = True
# ) as stream:
#     for chunk in stream:
#         if chunk.choices[0].delta.content:
#             print(chunk.choices[0].delta.content, end="", flush=True)

# we dont want the header, footer or any commentary that it sends as response
add_user_message(messages, "generate three different sample AWS CLI commands.Each should be very short")
add_assitant_message(messages, "here are 3 commands in single block without commands:\n```bash")
print(chat(messages=messages, stop=["```"]))
