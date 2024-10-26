from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Load the saved Random Forest model
model = joblib.load('model/crop_model.pkl')

# Define a route for the homepage
@app.route('/')
def home():
    return render_template('index.html')  # Create this HTML file next

# Define a route for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Extract data from the form (from HTML form) or request JSON
    data = request.form  # Alternatively, use request.json if sending JSON data
    input_data = {
        'N': float(data['N']),  # Nutrient N
        'P': float(data['P']),  # Nutrient P
        'K': float(data['K']),  # Nutrient K
        'temperature': float(data['temperature']),
        'humidity': float(data['humidity']),
        'ph': float(data['ph']),
        'rainfall': float(data['rainfall']),
    }

    # Convert input data to DataFrame for model input
    input_df = pd.DataFrame([input_data])

    # Make prediction using loaded model
    prediction = model.predict(input_df)[0]

    # Render the prediction result page
    return render_template('result.html', recommended_crop=prediction)

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
