from flask import Flask, request, jsonify, render_template
import pickle
import json
import numpy as np

app = Flask(__name__)

# Load the model
model = pickle.load(open('bengaluru_home_prices.pickle', 'rb'))

# Load the column names from columns.json
with open('columns.json', 'r') as f:
    data_columns = json.load(f)['data_columns']
    locations = data_columns[3:]  # Locations start after the first 3 columns

@app.route('/')
def home():
    """
    Render the main page with the form.
    """
    return render_template('index.html', locations=locations)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle predictions by accepting JSON input and returning the predicted price.
    """
    try:
        total_sqft = float(request.form['total_sqft'])
        bath = int(request.form['bath'])
        bhk = int(request.form['bhk'])
        location = request.form['location'].lower()

        # Prepare the input vector
        x = np.zeros(len(data_columns))
        x[0] = total_sqft
        x[1] = bath
        x[2] = bhk
        if location in locations:
            loc_index = data_columns.index(location)
            x[loc_index] = 1

        # Predict price
        predicted_price = model.predict([x])[0]
        return jsonify({'price': round(predicted_price, 2)})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
