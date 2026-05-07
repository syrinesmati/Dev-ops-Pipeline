from flask import Flask, jsonify
from app.calculator import add, subtract, multiply, divide

app = Flask(__name__)

@app.route("/")
def health():
    return jsonify({"status": "ok", "service": "flask-devops-app"})

@app.route("/add/<int:a>/<int:b>")
def route_add(a, b):
    return jsonify({"result": add(a, b)})

@app.route("/divide/<int:a>/<int:b>")
def route_divide(a, b):
    try:
        return jsonify({"result": divide(a, b)})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)