from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # Enables Cross-Origin Requests for all routes

@app.route("/")
def home():
    return "Code Editor is Running!"

@app.route("/run", methods=["POST"])
def run_code():
    data = request.json
    code = data.get("code")
    
    with open("script.py", "w") as f:
        f.write(code)

    try:
        result = subprocess.run(["python3", "script.py"], capture_output=True, text=True, shell=True)
        output = result.stdout if result.stdout else result.stderr
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


