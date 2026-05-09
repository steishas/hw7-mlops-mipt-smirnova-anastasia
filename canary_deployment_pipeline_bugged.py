# Версия с багом для демонстрации Rollback
from flask import Flask, request, jsonify
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import os

app = Flask(__name__)

VERSION = os.environ.get("MODEL_VERSION", "v1.2.0")

iris = load_iris(); X = iris.data; y = iris.target
hyperparameters = {"n_estimators": 100, "random_state": 42}
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(**hyperparameters)
model.fit(X_train, y_train)


@app.route("/health", methods=["GET"])
def health():
    # Баг: v1.2.0 падает с ошибкой 500
    raise Exception("Critical error: model failed to load")
    return jsonify({"status": "ok", "version": VERSION}), 200


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        features = np.array(data["features"]).reshape(1, -1)
        prediction = model.predict(features)
        return jsonify({"prediction": int(prediction[0]), "version": VERSION}), 200
    except Exception as e:
        return jsonify({"error": str(e), "version": VERSION}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
