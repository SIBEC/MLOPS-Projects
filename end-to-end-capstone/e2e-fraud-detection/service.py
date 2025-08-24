# filename: service.py
import bentoml
import numpy as np
import pandas as pd
from bentoml.io import NumpyNdarray, JSON

# Load the model from the BentoML model store using its tag
bento_model = bentoml.sklearn.get("fraud_model:latest")

# Create a runner for our model
fraud_runner = bento_model.to_runner()

# Create the BentoML Service
# The name "FraudDetector" is how we will refer to this service.
svc = bentoml.Service("FraudDetector", runners=[fraud_runner])


@svc.api(
    input=NumpyNdarray(shape=(-1, 1), dtype=np.float64, enforce_shape=True),
    output=JSON()
)
def classify(input_data: np.ndarray) -> dict:
    """
    API endpoint to classify a transaction.
    Expects a numpy array of shape (n, 1) where n is the number of transactions
    and the single feature is 'amount'.
    """
    print(f"Received input data for prediction: {input_data}")

    # The runner's `predict` method will run the model
    predictions = fraud_runner.predict.run(input_data)

    # The output of a sklearn model is a numpy array.
    # We'll convert it to a list for JSON serialization.
    result = predictions.tolist()

    # Return a dictionary with the prediction
    # 0 = Not Fraud, 1 = Fraud
    return {"predictions": result}
