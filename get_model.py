from flask import Flask, request, jsonify
import joblib
import numpy as np


app = Flask(__name__)

# Load the trained model
model = joblib.load('./model.pkl')

def species_mapping(prediction):
    if prediction == float(0) :
        prediction = "Iris setosa"
    elif prediction == float(1) :
        prediction = "Iris versicolor"
    else :
        prediction = "Iris virginica"
    return prediction

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from the request
        data = request.get_json()

        # Assuming the input data is in the same format as the Iris dataset
        features = np.array(data['features']).reshape(1, -1)
    
        # Make predictions
        prediction = model.predict(features)
        prediction = species_mapping(prediction)

        # Return the prediction as JSON
        return jsonify({'prediction': (prediction)})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
