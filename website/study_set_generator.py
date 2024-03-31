import openai
import requests
import json

def generate_questions(input_text, api_key):

    data = {
        'model': 'text-davinci-002',
        'prompt': input_text,
        'max_tokens': 100,
        'n_questions': 5
    }


    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    response = requests.post('https://api.openai.com/v1/question-generation', headers=headers, data=json.dumps(data))
    generated_questions = response.json().get('questions', [])

    return generated_questions

