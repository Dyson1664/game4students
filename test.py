import openai
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

def generate_question():
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use "gpt-3.5-turbo" as GPT-4 is not publicly available yet
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Create a question based on english vocab for a grade 3 ESL class"}
        ],
        max_tokens=50,
        temperature=0.7
    )
    question = response['choices'][0]['message']['content'].strip()
    return question

# Usage:
question = generate_question()
print(question)


