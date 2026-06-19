from flask import Flask, request, jsonify
from flask.logging import create_logger
import logging
import pandas as pd
import joblib
import os

from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)


def scale(payload):
    """Scales payload"""
    LOG.info("Scaling payload: %s", payload)
    scaler = StandardScaler().fit(payload)
    scaled_adhoc_predict = scaler.transform(payload)
    return scaled_adhoc_predict


@app.route("/")
def home():
    return "<h3>Sklearn Prediction Home - Continuous Delivery </h3>"


@app.route("/predict", methods=["POST"])
def predict():
    try:
        model_path = os.path.join(os.path.dirname(__file__), "Housing_price_model", "LinearRegression.joblib")
        clf = joblib.load(model_path)

    except Exception as e:
        LOG.exception("Model not loaded")
        return "Model not loaded", 500

    json_payload = request.json
    LOG.info("JSON payload: %s", json_payload)

    inference_payload = pd.DataFrame(json_payload)
    LOG.info("Inference payload DataFrame: %s", inference_payload)

    scaled_payload = scale(inference_payload)
    prediction = clf.predict(scaled_payload)

    return jsonify({"prediction": prediction.tolist()})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
