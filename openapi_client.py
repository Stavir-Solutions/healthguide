import logging
import os

import requests

URL = "https://api.openai.com/v1/chat/completions"
API_KEY = os.getenv('OPENAI_SECRET_KEY')
MODEL_ID = 'gpt-3.5-turbo'

CACHE = {}


def query_openapi(prompt):
    print(f'cache-{CACHE}')
    if prompt in CACHE:
        logging.info("Cache hit")
        result = CACHE[prompt]
    else:
        result = invoke_openapi(prompt)
    return result


def invoke_openapi(prompt):
    # Call the OpenAI API
    payload = build_payload(prompt)
    headers = build_headers()
    response = requests.post(URL, headers=headers, json=payload, stream=False)
    logging.debug(f"response: {response}")

    # Process the API response and return the result
    if response.ok:
        generated_text = response.json()["choices"][0]["message"]["content"].strip()
        logging.debug(f"generated_text{generated_text}")
        result = generated_text
        CACHE[prompt] = generated_text;
    else:
        logging.error(f'Error invoking open api {response}')
        result = "Error calling OpenAI API"
    return result


def build_headers():
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }


def build_payload(prompt):
    return {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 1.0,
        "top_p": 0.7,
        "n": 1,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 0,
    }
