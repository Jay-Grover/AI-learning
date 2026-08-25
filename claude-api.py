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
message = client.chat.completions.create(
    model=model,
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": "What is quantum computing? Answer in one sentence."
        }
    ]
)

print(message.choices[0].message.content)
