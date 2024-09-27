from flask import Flask, json, request, jsonify, session, redirect, url_for, render_template
import os
from datetime import timedelta
from flask_session.__init__ import Session

from firebase_config import firebase,auth, firebaseConfig

app = Flask(__name__)

# This is important for Flask Session Handling
# Do not change this
app.secret_key = os.getenv('APP_SECRET_KEY')
app.permanent_session_lifetime = timedelta(days=7)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.before_request
def validate_user_session():
    auth_routes = ['login','signup']
    # check if Session['user'] is present or not
    # Check if 'user' is in session, if not, redirect to login page
    print(request.endpoint)
    if 'user' not in session:
        # if the requested url was '/login' or '/signup' then let it proceed
        # else redirect it to the '/login'
        if request.endpoint not in auth_routes:
            return redirect(url_for('login'))
    else:
        # if the requested url was '/login' or '/signup' redirect to '/'
        # else let it proceed
        if request.endpoint in auth_routes:
            return redirect(url_for('index'))
        


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.get_json()
        email = data.get('email') 
        password = data.get('password')
        if email == None or password == None:
            # unauthorized
            return jsonify({'status':'error','message':'incomplete payload'}), 401
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print(user)
        uid = user['localId']
        session['user'] = uid
        session['email'] = email
        return jsonify({'status':'success','message':'logged in successfully'}), 201
    except Exception as e:
        #Firebase Error Specific Handling
        error_json = e.args[1] 
        error_data = json.loads(error_json)  # Convert the error to JSON
        error_message = error_data.get('error', {}).get('message', 'Unknown error occurred')
        print(error_message)
        return jsonify({'status':'error','message': error_message}), 500



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        data = request.get_json();
        email = data.get('email') 
        password = data.get('password')
        if email == None or password == None:
            # unauthorized
            return jsonify({'status':'error','message':'incomplete payload'}), 401
        try:
            user = auth.create_user_with_email_and_password(email, password)
            uid = user['localId']
            session['user'] = uid
            session['email'] = email

            return jsonify({'status':'success','message':'signed up successfully'}), 201
        except Exception as e:
            #Firebase Error Specific Handling
            error_json = e.args[1] 
            error_data = json.loads(error_json) 
            error_message = error_data.get('error', {}).get('message', 'Unknown error occurred')
            print(error_message)
            return jsonify({'status':'error','message': error_message}), 500

@app.route('/logout', methods=['POST'])
def logout():
    try:
        session.pop('user')
        session.pop('email')
        return jsonify({'status':'success', 'message':'logged out successfully'}), 200
    except Exception as e:
        return jsonify({'status':'error', 'message':str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)