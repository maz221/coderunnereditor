
from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    data = request.json
    code = data.get('code')
    language = data.get('language')

    # File extensions for different languages
    extensions = {"python": "py", "cpp": "cpp"}
    ext = extensions.get(language, "txt")

    # Create a temporary file with the user's code
    file_name = f"temp.{ext}"
    with open(file_name, "w") as f:
        f.write(code)

    # Command to execute the code
    commands = {
        "python": ["python3", file_name],
        "cpp": ["g++", file_name, "-o", "temp.out", "&&", "./temp.out"]
    }

    # Execute the command and capture the output
    try:
        if language == "cpp":
            # Compile and run for C++
            compile_result = subprocess.run(["g++", file_name, "-o", "temp.out"], capture_output=True, text=True)
            if compile_result.returncode == 0:
                result = subprocess.run("./temp.out", capture_output=True, text=True)
            else:
                result = compile_result
        else:
            # Run directly for Python
            result = subprocess.run(commands[language], capture_output=True, text=True)

        output = result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        output = str(e)
    finally:
        # Clean up temporary files
        if os.path.exists(file_name):
            os.remove(file_name)
        if os.path.exists("temp.out"):
            os.remove("temp.out")

    return jsonify({"output": output})

if __name__ == '__main__':
    from waitress import serve  # Alternative: Gunicorn
    serve(app, host="0.0.0.0", port=8080)

