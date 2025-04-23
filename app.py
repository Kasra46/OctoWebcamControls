from flask import Flask, send_from_directory, request, jsonify
import paramiko
import json
import os
from pathlib import Path

app = Flask(__name__)

# Path to the credentials file
CREDENTIALS_FILE = 'credentials.json'

def get_ssh_connection():
    """Establish SSH connection using saved credentials"""
    if not os.path.exists(CREDENTIALS_FILE):
        return None, "Credentials file not found"

    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            credentials = json.load(f)
    except json.JSONDecodeError:
        return None, "Invalid credentials file format"

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=credentials['hostname'],
            username=credentials['username'],
            password=credentials['password'],
            port=credentials.get('port', 22)
        )
        return ssh, None
    except Exception as e:
        return None, str(e)

def execute_ssh_command(command):
    """Execute a command over SSH and return the result"""
    ssh, error = get_ssh_connection()
    if error:
        return None, error

    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        if error and "no process found" not in error.lower():
            return None, error
        
        return output, None
    except Exception as e:
        return None, str(e)
    finally:
        if ssh:
            ssh.close()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/execute', methods=['POST'])
def execute_command():
    output, error = execute_ssh_command('bash webcamfhd.sh')
    if error:
        return jsonify({'error': error}), 500
    return jsonify({'success': True, 'output': output})

@app.route('/endstream', methods=['POST'])
def end_stream():
    output, error = execute_ssh_command('pkill mjpg_streamer')
    if error:
        return jsonify({'error': error}), 500
    return jsonify({'success': True, 'output': output})

@app.route('/restartv4l2', methods=['POST'])
def restart_v4l2():
    commands = [
        'pkill mjpg_streamer',
        'modprobe -r uvcvideo',
        'modprobe uvcvideo'
    ]
    
    for command in commands:
        output, error = execute_ssh_command(command)
        if error:
            return jsonify({'error': error}), 500
    
    return jsonify({'success': True, 'output': 'v4l2 restarted successfully'})

@app.route('/fhd', methods=['POST'])
def fhd_quality():
    output, error = execute_ssh_command('./webcamfhd.sh')
    if error:
        return jsonify({'error': error}), 500
    return jsonify({'success': True, 'output': output})

@app.route('/qhd', methods=['POST'])
def qhd_quality():
    output, error = execute_ssh_command('./webcamqhd.sh')
    if error:
        return jsonify({'error': error}), 500
    return jsonify({'success': True, 'output': output})

@app.route('/quality960', methods=['POST'])
def quality_960():
    output, error = execute_ssh_command('./webcam960.sh')
    if error:
        return jsonify({'error': error}), 500
    return jsonify({'success': True, 'output': output})

@app.route('/webcamconfig', methods=['POST'])
def webcam_config():
    output, error = execute_ssh_command('./webcamconfig.sh')
    if error:
        return jsonify({'error': error}), 500
    return jsonify({'success': True, 'output': output})

if __name__ == '__main__':
    app.run(debug=True, port=5000) 