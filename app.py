from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_awscognito import AWSCognitoAuthentication
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity


import logging

from openapi_client import query_openapi
from query_builder import build_open_api_prompt_from_user_input

app = Flask(__name__)

logging.basicConfig(filename='application.log', level=logging.DEBUG)

#TODO move the secrets to github secret and access as env variables
app.config["AWS_DEFAULT_REGION"] = "us-east-1"
app.config["AWS_COGNITO_DOMAIN"] = "https://lifestyle-advise.auth.us-east-1.amazoncognito.com"
app.config["AWS_COGNITO_USER_POOL_ID"] = "us-east-1_9KNLru65q"
app.config["AWS_COGNITO_USER_POOL_CLIENT_ID"] = "3vve5j1t85tjp6lrheibta9eka"
app.config["SECRET_KEY"] = "AKIAYRUCY23SC7U2YXCC"
#TODO it should be an evironment configuration
app.config["AWS_COGNITO_REDIRECT_URL"] = "http://localhost:5000/loggedin"
app.config["AWS_COGNITO_LOGOUT_URL"] = "http://localhost:5000"
app.config["AWS_COGNITO_USER_POOL_CLIENT_SECRET"] = "abdpbt9vjuuqn7rsh57mod3u6a3m244feu0cg0aoflkerkvknlj"
app.config["JWT_PUBLIC_KEY"] = "RSAAlgorithm.from_jwk"
JWT_TOKEN_LOCATION = ["cookies"]
JWT_COOKIE_SECURE = True

# We're ok to set this off, as Cognito OAuth state provides protection
JWT_COOKIE_CSRF_PROTECT = False
JWT_ALGORITHM = "RS256"
JWT_IDENTITY_CLAIM = "sub"
app.config["JWT_PRIVATE_KEY"] = ""
#  We're using Cognito to generate keys, so this is never used
app.config["JWT_SECRET_KEY"] = ""



CORS(app)
aws_auth = AWSCognitoAuthentication(app)
jwt = JWTManager(app)



@app.route('/')
def home():
    logged_in = False
    access_token = session.get("access_token")

    if access_token:
        try:
            # Validate the access token
            identity = get_jwt_identity()
            if identity is None:
                logging.info("User is token is not valid (identity is none")
                logged_in = False
            else:
                logging.info(f"User identity {identity}")
                logged_in = True
        except:
            # Token is valid
            logged_in = True
    
    return render_template('form.html', logged_in=logged_in)


@app.route('/submit', methods=['POST'])
def submit():
    logging.info("Generating lifestyle advise")

    api_response = query_openapi(build_open_api_prompt_from_user_input(request))
    logging.debug(f'api_response: {api_response}')
    return render_template('results.html', generated_text=api_response)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Disable the login button after it's clicked
    url = aws_auth.get_sign_in_url()
    logging.info(f"Cognito url :{ url}")
    return redirect(url)


@app.route("/loggedin", methods=["GET"])
def logged_in():
    logging.info("Logged in called")
    access_token = aws_auth.get_access_token(request.args)
    if access_token:
        session["access_token"] = access_token
        # TODO once the login code is working try commenting it
        # session["logged_in"] = True
        return redirect(url_for("home"))
    else:
        # Handle failed login
        logging.error("access_token is not generated")
        return redirect(url_for("home"))
    

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()  # Clear Flask session
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

