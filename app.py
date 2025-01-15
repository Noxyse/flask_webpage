from flask import Flask, render_template, request, redirect
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for secure sessions

def validate_email(email):
    pattern = r"^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)

def sanitize_input(input, field_name):
    allowed_pattern = r'^[\w\s@._+-]*$'  # Allowed characters
    if not re.match(allowed_pattern, input):
        raise ValueError(f"Invalid characters in {field_name}.")
    return input.strip()

@app.route('/')
def index():
    # Render the form with no pre-filled data and no errors
    return render_template('index.html', form_data={}, errors={})

@app.route('/submit', methods=['POST'])
def submit():
    errors = {}
    form_data = request.form.to_dict()  # Convert form data to a dictionary

    try:
        # Honeypot validation
        honeypot = request.form.get('honeypot', '')
        if honeypot:
            errors['honeypot'] = "You're a bot! Get out of here!"

        # Validate email
        email = request.form.get('email', '')
        if not validate_email(email):
            errors['email'] = "Invalid Email address."

        # Validate and sanitize all fields
        try:
            form_data['name'] = sanitize_input(request.form.get('name', ''), 'Name')
            form_data['surname'] = sanitize_input(request.form.get('surname', ''), 'Surname')
            form_data['gender'] = sanitize_input(request.form.get('gender', ''), 'Gender')
            form_data['country'] = sanitize_input(request.form.get('country', ''), 'Country')
            form_data['message'] = sanitize_input(request.form.get('message', ''), 'Message')
            form_data['services'] = request.form.getlist('services')  # Get multiple checkbox values
        except ValueError as e:
            field_name = str(e).split(' ')[-1].strip('.')
            errors[field_name.lower()] = str(e)

    except Exception as e:
        errors['general'] = "An unexpected error occurred."

    if errors:
        # Render the form with errors and pre-filled data
        return render_template('index.html', form_data=form_data, errors=errors)

    # If no errors, process the form and redirect to the response page
    return render_template('response.html', data=form_data)


if __name__ == "__main__":
    app.run(debug=True)
