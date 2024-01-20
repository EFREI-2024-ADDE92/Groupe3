import numpy as np
from collections import OrderedDict
import joblib
import time
from flask import Flask, request, Response, jsonify
from prometheus_client import Counter, Gauge, generate_latest, REGISTRY
 
app = Flask(__name__)

# Counter pour le nombre total de requêtes
api_call_counter = Counter('api_calls_total', 'Total number of API calls')

# Gauge pour le nombre de requêtes continuellement dans le temps
continuous_api_calls = Counter('continuous_calls_total', 'Number of continuous API calls')

# Variable pour stocker le timestamp de la dernière requête
last_request_timestamp = None

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

@app.route('/predict', methods=["POST"])
def predict():
    global last_request_timestamp

    try:
        # Get input data from the request
        sepal_length = request.args.get('sepal_length')
        sepal_width = request.args.get('sepal_width')
        petal_length = request.args.get('petal_length')
        petal_width = request.args.get('petal_width')

        # Assuming the input data is in the same format as the Iris dataset
        features = np.array([float(sepal_length), float(sepal_width), float(petal_length), float(petal_width)]).reshape(1, -1)

        # Make predictions
        prediction = model.predict(features)
        prediction = species_mapping(prediction)

        # Increment total API calls counter
        api_call_counter.inc()
        continuous_api_calls.inc()

        # Check and update continuous API calls gauge
        current_timestamp = time.time()
        if last_request_timestamp is not None:
            time_since_last_request = current_timestamp - last_request_timestamp
            continuous_api_calls.set(1 if time_since_last_request <= 600 else 0)

        last_request_timestamp = current_timestamp

        response_dict = OrderedDict([
            ('Your Input Features', OrderedDict([
                ('Sepal Length', sepal_length),
                ('Sepal Width', sepal_width),
                ('Petal Length', petal_length),
                ('Petal Width', petal_width),
            ])),
            ('Predicted Specie', prediction)
        ])

        return jsonify(response_dict)

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/metrics')
def metrics():
    # Expose the metrics in Prometheus format
    return Response(generate_latest(REGISTRY), content_type='text/plain; version=0.0.4')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
