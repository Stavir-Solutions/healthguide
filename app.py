from flask import Flask, render_template, request

import logging

from openapi_client import query_openapi
from query_builder import build_open_api_prompt_from_user_input

app = Flask(__name__)

logging.basicConfig(filename='application.log', level=logging.DEBUG)


@app.route('/')
def home():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    logging.info("Generating lifestyle advise")

    api_response = query_openapi(build_open_api_prompt_from_user_input(request))
    return render_template('results.html', generated_text=api_response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
