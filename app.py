from flask import Flask, render_template, request, redirect, url_for
import joblib  # Assuming model is saved as a .pkl file
import datetime
import os

app = Flask(__name__)

# Load your pre-trained model (ensure this path is correct)
model = joblib.load("C:\\Users\\naiki\\OneDrive\\Desktop\\Hexart\\models1.pkl")
print(type(model))


# Load the model list
model_list = joblib.load("C:\\Users\\naiki\\OneDrive\\Desktop\\Hexart\\models1.pkl")




# Load the model directly
model = joblib.load("C:\\Users\\naiki\\OneDrive\\Desktop\\Hexart\\models1.pkl")


# Re-save the model alone (without the list wrapper)
joblib.dump(model,"C:\\Users\\naiki\\OneDrive\\Desktop\\Hexart\\models1.pkl")
model = joblib.load("C:\\Users\\naiki\\OneDrive\\Desktop\\Hexart\\models1.pkl")


@app.route('/')
def index():
    return render_template("index.html")
@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve data from the form
    name = request.form.get('name')
    email = request.form.get('email')
    contraction_count = float(request.form.get('contraction_count'))
    length_of_contraction = float(request.form.get('length_of_contraction'))
    std = float(request.form.get('std'))
    entropy = float(request.form.get('entropy'))
    contraction_times = float(request.form.get('contraction_times'))

    # Display data for cross-verification
    data = {
        'name': name,
        'email': email,
        'contraction_count': contraction_count,
        'length_of_contraction': length_of_contraction,
        'std': std,
        'entropy': entropy,
        'contraction_times': contraction_times
    }

    # Predict using the model
    input_features = [[contraction_count, length_of_contraction, std, entropy, contraction_times]]
    prediction = model.predict([input_features])
    prediction_text = 'Preterm' if prediction[0] == 1 else 'Not Preterm'

    return render_template('result.html', data=data, prediction=prediction_text)

import os  # Add this import at the beginning of your file

@app.route('/print_report', methods=['POST'])
def print_report():
    # Gather all data
    data = request.form.to_dict()
    name = data.get('name', 'User')
    prediction = data.get('prediction')  # Ensure this is passed from the form

    # Generate the report message with all values
    report_message = (
        f"Report for {name}\n"
        f"Email: {data.get('email')}\n"
        f"Contraction Count: {data.get('contraction_count')}\n"
        f"Length of Contraction: {data.get('length_of_contraction')}\n"
        f"Standard Deviation: {data.get('std')}\n"
        f"Entropy: {data.get('entropy')}\n"
        f"Contraction Times: {data.get('contraction_times')}\n"
        f"Prediction: {prediction}\n\n"
        f"Wishing you good luck and health!"

    )
    

    # Create reports directory if it doesn't exist
    reports_dir = 'reports'
    os.makedirs(reports_dir, exist_ok=True)  # Create directory

    # Save to file
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    report_file = os.path.join(reports_dir, f"report_{name}_{timestamp}.txt")  # Use os.path.join
    with open(report_file, 'w') as file:
        file.write(report_message)

    return f"Report saved as {report_file} with message: {report_message}"

if __name__ == "__main__":
    app.run(debug=True)
