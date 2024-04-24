from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_awscognito import AWSCognitoAuthentication
from flask import session
 

import logging

from openapi_client import query_openapi
from query_builder import build_open_api_prompt_from_user_input

app = Flask(__name__)


logging.basicConfig(filename='application.log', level=logging.DEBUG)

app = Flask(__name__)
app.config["AWS_DEFAULT_REGION"] = "us-east-1"
app.config["AWS_COGNITO_DOMAIN"] = "https://lifestyle-advise.auth.us-east-1.amazoncognito.com"
app.config["AWS_COGNITO_USER_POOL_ID"] = "us-east-1_9KNLru65q"
app.config["AWS_COGNITO_USER_POOL_CLIENT_ID"] = "3vve5j1t85tjp6lrheibta9eka"
app.config["AWS_COGNITO_REDIRECT_URL"] = "http://localhost:5000"
app.config["AWS_COGNITO_LOGOUT_URL"] = "https://lifestyle-advise.auth.us-east-1.amazoncognito.com"
app.config["AWS_COGNITO_USER_POOL_CLIENT_SECRET"] = "abdpbt9vjuuqn7rsh57mod3u6a3m244feu0cg0aoflkerkvknlj"


aws_auth = AWSCognitoAuthentication(app)



@app.route('/')
def home():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    logging.info("Generating lifestyle advise")

    api_response = query_openapi(build_open_api_prompt_from_user_input(request))
    return render_template('results.html', generated_text=api_response)

@app.route("/login", methods=["GET", "POST"])
def login():
    # Disable the login button after it's clicked
    return redirect(aws_auth.get_sign_in_url())

@app.route("/loggedin", methods=["GET"])
def logged_in():
    access_token = aws_auth.get_access_token(request.args)
    if access_token:
        session["access_token"] = access_token
        return redirect(url_for("protected"))
    else:
        # Handle failed login
        return redirect(url_for("login"))





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

