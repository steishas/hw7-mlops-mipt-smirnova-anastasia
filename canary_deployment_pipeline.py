from flask import Flask, request, jsonify
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os

app = Flask(__name__)

# Версия сервиса из переменной окружения
VERSION = os.environ.get("MODEL_VERSION", "v1.0.0")

# Загружаем и обучаем модель при старте
iris = load_iris();X = iris.data ;y = iris.target
hyperparameters={"n_estimators":100, "random_state":42}
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(**hyperparameters)
model.fit(X_train, y_train)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "version": VERSION
    }), 200


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        features = np.array(data["features"]).reshape(1, -1)
        prediction = model.predict(features)
        return jsonify({
            "prediction": int(prediction[0]),
            "version": VERSION
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e),
            "version": VERSION
        }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
