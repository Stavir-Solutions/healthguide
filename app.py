from flask import Flask, render_template, request
import requests
import logging
from dotenv import load_dotenv

app = Flask(__name__)

# Set up OpenAI API credentials
# load_dotenv()
logging.basicConfig(filename='application.log', level=logging.DEBUG)
#TODO get from environment
openai_api_key = ''
model_id = 'gpt-3.5-turbo'

# Define the Flask route that displays the form
@app.route('/')
def index():
    return render_template('form.html')

# Define the Flask route that handles the form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    logging.info("form submitted")
    # Get the form data from the request
    height = request.form.get('height', '')
    weight = request.form.get('weight', '')
    age = request.form.get('age', '')
    conditions = request.form.get('conditions', '')
    gender = request.form.get('gender', '')
    walk = request.form.get('walk', '')
    exercise = request.form.get('exercise', '')
    fruits_veggies = request.form.get('fruits_veggies', '')
    diet = request.form.get('diet', '')
    sleep = request.form.get('sleep', '')
    sleep_reason = request.form.getlist('sleep_reason[]')
    hypertension = request.form.get('hypertension', '')
    diabetes = request.form.get('diabetes', '')
    smoking = request.form.get('smoking', '')
    alcohol = request.form.get('alcohol', '')
    nervous = request.form.get('nervous', '')
    depressed = request.form.get('depressed', '')
    difficult = request.form.get('difficult', '')
    worthless = request.form.get('worthless', '')

    # Construct the mytext variable based only on non-empty and non-"prefer not to say" fields
    mytext = "As an expert health advisor, prepare lifestyle advice for the Healthy life, for a person with the following characteristics:"
    if height:
        mytext += f" {height}cm tall"
    if weight:
        mytext += f" weights {weight}kg"
    if age:
        mytext += f" and is a {age}-year-old"
    if gender:
        mytext += f" {gender}"
    if conditions:
        mytext += f" following health conditions {conditions}"
    mytext += ". This person took the following lifestyle and medical history questionnaire and next to each question is the answer obtained. Your essay please separate it into Introduction, Exercise, Sleep, Diet, Communication, Alcohol, Hobbies, Mental Health and Conclusion sections."
    if walk:
        mytext += f"\nPhysical Activity:\nHow much do you walk everyday? {walk}."
    if exercise and exercise != 'prefer not to say':
        mytext += f"\nIn a week how many times you exercise more than 30 minutes? {exercise}."
    if fruits_veggies:
        mytext += f"\nDiet:\nEveryday how many portions of fruits and vegetables do you eat? {fruits_veggies}."
    if diet and diet != 'prefer not to say':
        mytext += f"\nThe person follows {diet} diet."
    if sleep and sleep != 'prefer not to say':
        mytext += f"\nSleep:\nIn the past months, how would you qualify your own sleep? {sleep}."
        if sleep_reason:
            mytext += "\nWhich of the following reasons apply to your sleep? Select all that apply."
            for reason in sleep_reason:
                mytext += f"\n- {reason}"
    if hypertension:
        mytext += f"\nMedical History:\nHave you ever been told you have hypertension? Or are you on treatment for hypertension? {hypertension}."
    if diabetes:
        mytext += f"\nHave you ever been told you have diabetes? Or are you on treatment for diabetes? {diabetes}."
    if smoking:
        mytext += f"\nDo you smoke? {smoking}."
    if alcohol and alcohol != 'prefer not to say':
        mytext += f"\nHow much alcohol do you drink per day? {alcohol}."
    if nervous:
        mytext += f"\nMental Health:\nIn the past month, did you feel nervous?{nervous}."
    if depressed:
        mytext += f"\nIn the past month, did you feel depressed and like nothing could make you feel better? {depressed}."
    if difficult:
        mytext += f"\nIn the past month, did you feel that anything you did was foolish?{difficult}."
    if worthless:
        mytext += f"\nIn the past month, did you feel worthless? {worthless}."

    logging.debug(f"mytext{mytext}" )

    # Call the OpenAI API
    URL = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": mytext}],
        "temperature" : 1.0,
        "top_p":0.7,
        "n" : 1,
        "stream": False,
        "presence_penalty":0,
        "frequency_penalty":0,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    response = requests.post(URL, headers=headers, json=payload, stream=False)
    logging.debug(f"response: {response}")
    
    # Process the API response and return the result
    if response.ok:
        response_data = response.json()
        logging.debug(f"response_dataaaaaa:{response_data}")
        generated_text = response_data["choices"][0]["message"]["content"].strip()
        logging.debug(f"generated_text{generated_text}")
        
        # Render the result template
        return render_template('results.html', generated_text=generated_text)
    else:
        return "Error calling OpenAI API"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
