from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

DATA_FILE = "problems.json"

# Load data
def load_problems():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save data
def save_problems(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Home route
@app.route('/')
def home():
    return "Code Practice Tracker Running!"

# GET all problems
@app.route('/problems', methods=['GET'])
def get_problems():
    data = load_problems()
    return jsonify(data)

# ADD new problem
@app.route('/problems', methods=['POST'])
def add_problem():
    data = load_problems()
    new_problem = request.json
    data.append(new_problem)
    save_problems(data)
    return jsonify(new_problem), 201

# DELETE problem
@app.route('/problems/<int:index>', methods=['DELETE'])
def delete_problem(index):
    data = load_problems()
    if index < len(data):
        removed = data.pop(index)
        save_problems(data)
        return jsonify(removed)
    return jsonify({"error": "Invalid index"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)