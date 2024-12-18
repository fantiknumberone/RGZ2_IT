from flask import Blueprint, render_template, request, jsonify
import subprocess

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/run', methods=['POST'])
def run_code():
    data = request.json
    code = data.get('code')
    language = data.get('language')
    
    if not code or not language:
        return jsonify({"error": "Code and language are required"}), 400

    try:
        if language == "python":
            with open("temp.py", "w") as file:
                file.write(code)
            result = subprocess.run(["python3", "temp.py"], capture_output=True, text=True, timeout=5)
        elif language == "c":
            with open("temp.c", "w") as file:
                file.write(code)
            subprocess.run(["gcc", "temp.c", "-o", "temp.out"], check=True)
            result = subprocess.run(["./temp.out"], capture_output=True, text=True, timeout=5)
        else:
            return jsonify({"error": f"Unsupported language: {language}"}), 400

        return jsonify({"output": result.stdout, "errors": result.stderr})
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Execution timed out"}), 408
    except Exception as e:
        return jsonify({"error": str(e)}), 500
