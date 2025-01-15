from flask import Flask, render_template, request
import re

app = Flask(__name__)

def validate_email(email):
    pattern = r"^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.(com|fr|be|org|net|edu)$"
    return re.match(pattern, email)

def sanitize_input(input):
    # Remove all non-alphanumeric characters except @
    return re.sub(r'[^a-zA-Z0-9@._+-]', '', input)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    if not validate_email(email):
        return "Invalid email address. Please use a correct domain."
    data = {
        "name": sanitize_input(request.form['name']).capitalize(),
        "surname": sanitize_input(request.form['surname']).capitalize(),
        "gender": sanitize_input(request.form['gender']).capitalize(),
        "email": sanitize_input(request.form['email']).capitalize(),
        "country": sanitize_input(request.form['country']).capitalize(),
        "services": [service.capitalize() for service in request.form.getlist('services')],  # Handles multiple checkboxes
        "message": sanitize_input(request.form['message']).capitalize()
    }
    return render_template('response.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)