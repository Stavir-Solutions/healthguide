import logging


def build_open_api_prompt_from_user_input(request):

    patient_height = request.form.get('height', '')
    weight = request.form.get('weight', '')
    age = request.form.get('age', '')
    symptoms = request.form.get('symptoms', '')
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

    # Construct the prompt variable based only on non-empty and non-"prefer not to say" fields
    prompt = "Prepare a set of lifestyle advice for a Healthy and long living, for a person with the following characteristics:"
    if patient_height:
        prompt += f" {patient_height}cm tall,"
    if weight:
        prompt += f" weights {weight}kg"
    if age:
        prompt += f" and is {age}-year-old"
    if gender:
        prompt += f" {gender}"
        # If "prefer not to say" is selected, set gender to an empty string
    if gender == 'prefer_not_to_say':
        gender = ''
    prompt += f'. The person also have the following life style issues and symptoms, {symptoms}. '
    prompt += ("This person has completed a lifestyle and medical history questionnaire, with answers provided for each question as below. "
               "Can you provide this person with lifestyle advises in the following areas: Exercise, Sleep, Diet, Hobbies, Social life. "
               "Give top 10 most impactful advises for this person. Provide Each piece of advice with its category and keep it up to 150 characters long.")
    if walk and walk != 'I dont know':  # Exclude 'I dont know'
        prompt += f"\nPhysical Activity:\nHow much do you walk everyday? {walk}."
    if exercise and exercise != 'I dont know':  # Exclude 'I dont know'
        prompt += f"\nIn a week how many times you exercise more than 30 minutes? {exercise}."
    if fruits_veggies and fruits_veggies != 'I dont know':  # Exclude 'I dont know'
        prompt += f"\nDiet:\nEveryday how many portions of fruits and vegetables do you eat? {fruits_veggies}."
    if diet and diet != 'prefer not to say':
        prompt += f"\nWhat diet do you follow?{diet}"
    if sleep and sleep != 'I dont know':  # Exclude 'I dont know'
        prompt += f"\nSleep:\nIn the past months, how would you qualify your own sleep? {sleep}."
        if sleep_reason:
            prompt += "\nWhich of the following reasons apply to your sleep? Select all that apply."
            for reason in sleep_reason:
                prompt += f"\n- {reason}"
    if hypertension:
        prompt += f"\nMedical History:\nHave you ever been told you have hypertension? Or are you on treatment for hypertension? {hypertension}."
    if diabetes:
        prompt += f"\nHave you ever been told you have diabetes? Or are you on treatment for diabetes? {diabetes}."
    if smoking:
        prompt += f"\nDo you smoke or consume tobaco? {smoking}."
    if alcohol and alcohol != 'prefer not to say':
        prompt += f"\nHow much alcohol do you drink per day? {alcohol}."
    if nervous:
        prompt += f"\nMental Health:\nIn the past month, did you feel nervous?{nervous}."
    if depressed and depressed != 'I dont know':  # Exclude 'I dont know'
        prompt += f"\nIn the past month, did you feel depressed and like nothing could make you feel better? {depressed}."
    if difficult:
        prompt += f"\nIn the past month, did you feel that anything you did was foolish?{difficult}."
    if worthless:
        prompt += f"\nIn the past month, did you feel worthless? {worthless}."
    logging.debug(f"prompt{prompt}")
    return prompt
