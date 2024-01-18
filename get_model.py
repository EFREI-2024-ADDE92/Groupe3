import numpy as np
import joblib
from flask import Flask, request, Response, jsonify
from prometheus_client import Counter, generate_latest, REGISTRY


app = Flask(__name__)

api_call_counter = Counter('api_calls_total', 'Total number of API calls')

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
        #Get input data from the request
        data = request.get_json()

        # inputs from user for each of these features
        sepal_length = data.get('sepal_length')
        sepal_width = data.get('sepal_width')
        petal_length = data.get('petal_length')
        petal_width = data.get('petal_width')

        #Assuming the input data is in the same format as the Iris dataset
        features = np.array([sepal_length, sepal_width, petal_length, petal_width]).reshape(1, -1)
    
        #Make predictions
        prediction = model.predict(features)
        prediction = species_mapping(prediction)
        api_call_counter.inc()

        return jsonify({'prediction': (prediction)})

    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/metrics')
def metrics():
    #Expose the metrics in Prometheus format
    return Response(generate_latest(REGISTRY), content_type='text/plain; version=0.0.4')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
