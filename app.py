
from flask import Flask, render_template, request
import subprocess
import sys
import platform
import io
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    output = None
    user_code = ""
    selected_language = "python"  # Default language

    if request.method == "POST":
        user_code = request.form.get("code")
        selected_language = request.form.get("language")
        
        if selected_language == "python":
            output = run_python_code(user_code)
        elif selected_language == "cpp":
            output = run_cpp_code(user_code)
        elif selected_language == "vb":
            output = run_vb_code(user_code)
        else:
            output = "Unsupported language"
    
    return render_template("index.html", output=output, code=user_code, language=selected_language)

def run_python_code(code):
    try:
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        exec(code)
        output = sys.stdout.getvalue()
    except Exception as e:
        output = f"Error: {str(e)}"
    finally:
        sys.stdout = old_stdout
    return output

def run_cpp_code(code):
    try:
        with open("temp.cpp", "w") as file:
            file.write(code)
        
        compile_process = subprocess.run(
            ["g++", "temp.cpp", "-o", "temp"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        
        if compile_process.returncode != 0:
            return f"Compilation Error: {compile_process.stderr.decode()}"
        
        executable = "temp.exe" if platform.system() == "Windows" else "./temp"
        
        run_process = subprocess.run(
            [executable], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        
        if run_process.returncode != 0:
            return f"Runtime Error: {run_process.stderr.decode()}"
        
        return run_process.stdout.decode()
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        # Cleanup temp files
        if os.path.exists("temp.cpp"):
            os.remove("temp.cpp")
        if os.path.exists("temp.exe"):
            os.remove("temp.exe")

def run_vb_code(code):
    try:
        with open("temp.vb", "w") as file:
            file.write(code)
        
        compile_process = subprocess.run(
            ["vbc", "temp.vb", "/out:temp.exe"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        
        if compile_process.returncode != 0:
            return f"Compilation Error: {compile_process.stderr.decode()}"
        
        run_process = subprocess.run(
            ["temp.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        
        if run_process.returncode != 0:
            return f"Runtime Error: {run_process.stderr.decode()}"
        
        return run_process.stdout.decode()
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        # Cleanup temp files
        if os.path.exists("temp.vb"):
            os.remove("temp.vb")
        if os.path.exists("temp.exe"):
            os.remove("temp.exe")

if __name__ == "__main__":
    app.run(debug=True)

