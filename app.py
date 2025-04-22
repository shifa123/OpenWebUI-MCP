from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def run_tool(command):
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        result = output.decode().splitlines()
        return jsonify({'status': 'success', 'results': result})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'output': e.output.decode()}), 500

@app.route('/run-subfinder', methods=['POST'])
def run_subfinder():
    domain = request.get_json().get('domain')
    if not domain:
        return jsonify({'error': 'Domain not provided'}), 400
    return run_tool(['subfinder', '-d', domain, '-silent'])

@app.route('/run-httpx', methods=['POST'])
def run_httpx():
    domains = request.get_json().get('domains')
    if not domains:
        return jsonify({'error': 'Domains not provided'}), 400
    with open('httpx_input.txt', 'w') as f:
        f.write('\n'.join(domains))
    return run_tool(['httpx', '-silent', '-l', 'httpx_input.txt'])

@app.route('/run-gau', methods=['POST'])
def run_gau():
    domain = request.get_json().get('domain')
    if not domain:
        return jsonify({'error': 'Domain not provided'}), 400
    return run_tool(['gau', domain])

@app.route('/run-waybackurls', methods=['POST'])
def run_waybackurls():
    domain = request.get_json().get('domain')
    if not domain:
        return jsonify({'error': 'Domain not provided'}), 400
    return run_tool(['waybackurls', domain])

@app.route('/run-nuclei', methods=['POST'])
def run_nuclei():
    urls = request.get_json().get('urls')
    if not urls:
        return jsonify({'error': 'URLs not provided'}), 400
    with open('nuclei_input.txt', 'w') as f:
        f.write('\n'.join(urls))
    return run_tool(['nuclei', '-l', 'nuclei_input.txt', '-silent'])

@app.route('/.well-known/openapi.json')
def serve_openapi():
    return send_from_directory(os.path.join(app.root_path, 'static/.well-known'), 'openapi.json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
