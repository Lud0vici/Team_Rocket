import socketserver
from flask import Flask, send_from_directory, request, redirect, url_for
from util import database_handler



app = Flask(__name__)

def add_no_sniff(response):
    response.headers["X-Content-Type-Options"] = "nosniff"

@app.route("/")
def serve_login_page():
    response = send_from_directory('src', 'LoginPage.html')
    add_no_sniff(response)
    return response

@app.route("/functions.js")
def serve_javascript():
    response = send_from_directory("public", "functions.js")
    add_no_sniff(response)
    return response

@app.route("/style.css")
def serve_css():
    response = send_from_directory("public", "style.css")
    add_no_sniff(response)
    return response

@app.route("/rocket_ball.png")
def serve_rocket_ball():
    response = send_from_directory("public", "image/rocket_ball.png")
    add_no_sniff(response)
    return response

#edit function so that it calls on insertUser to put into database 
@app.route("/register", methods=['POST'])
def serve_registration():
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name') 
    email = request.form.get('email')
    username = request.form.get('username') 
    password = request.form.get('password')
    confirmedPassword = request.form.get('confirm-password')
    if password != confirmedPassword: 
        #the flash functio is from Flask which just displays a temp message 
        flash("Passwords do not match") 
        return redirect(url_for("registration_form")) #need to adjust regist.... 
    salt, hashed_password = database_handler.salt_and_hash_password(password) 
    try: 
        database_handler.insert_user(first_name, last_name, email, username, salt, hashed_password)
    except Exception as e: #try if else statments instead of try and except 
        flash(str(e))
        return redirect(url_for("serve_login_page")) #need to adjust serve... 


    # response = send_from_directory("public", "/register")
    # add_no_sniff(response)
    # return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)