import requests
import json
from dotenv import load_dotenv
import os
import time

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

### NOTE: I COULD NOT GET THE OPENAI API TO WORK HERE SO NONE OF THE BELOW WORK!
### The error - 492: too many requests

def generate_question_answers(input_text: str, num_of_questions: int, max_retries=5, initial_delay=1):
    url = 'https://api.openai.com/v1/completions' # define the URL for the OpenAI completion endpoint

    # structure the prompt to enforce a specific format for Q&A pairs
    prompt = f"Based on the following text, generate a list of {num_of_questions} question and answer pairs, each formatted as 'Q: <Question> A: <Answer>':\n\n{input_text}\n"
    
    # set the parameters for the API request
    data = {
        'model': 'gpt-3.5-turbo',
        'prompt': prompt,
        'temperature': 0.5,
        'max_tokens': 10,
        'n_questions': 1
    }

    # configure the request headers with your API key for authentication
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    delay = initial_delay
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data)) # make the API request
            response.raise_for_status() # raises an exception for HTTP errors

            response_text = response.json().get('choices', [{}])[0].get('text', '').strip() # extract the response text

            # parse the formatted Q&A pairs from the response text
            qa_pairs = response_text.split('Q: ')[1:]  # split and ignore the first empty item
            qa_pairs = [(f"Q: {qa.split(' A: ')[0]}", f"A: {qa.split(' A: ')[1]}") for qa in qa_pairs]

            return qa_pairs
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
    return []

# example I was trying to run (it was unsuccessful of course)
input_text = "Describe the process of photosynthesis."
qa_pairs = generate_question_answers(input_text=input_text, num_of_questions=1)
for qa in qa_pairs:
    print(qa)

# client = OpenAI()

# audio_file = open("/path/to/file/speech.mp3", "rb")
# transcription = client.audio.transcriptions.create(
#   model="whisper-1", 
#   file=audio_file, 
#   response_format="text",
#   prompt="ZyntriQix, Digique Plus, CynapseFive, VortiQore V8, EchoNix Array, OrbitalLink Seven, DigiFractal Matrix, PULSE, RAPT, B.R.I.C.K., Q.U.A.R.T.Z., F.L.I.N.T."
# )
# print(transcription.text)

# def audio_to_text(path: String):
    

