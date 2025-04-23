# Linux Webcam Control

A simple web interface to control your Linux laptop over SSH and execute the webcamfhd.sh script.

## Setup

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `credentials.json` file in the same directory with your SSH credentials:
   ```json
   {
       "hostname": "your-linux-laptop-ip",
       "username": "your-username",
       "password": "your-password",
       "port": 22
   }
   ```

3. Make sure the `webcamfhd.sh` script is present on your Linux laptop in the home directory.

## Usage

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`

3. Click the "Start Webcam" button to execute the webcamfhd.sh script on your Linux laptop.

## Security Note

- The credentials are stored in plain text. For better security, consider using SSH keys instead of passwords.
- Make sure to keep the `credentials.json` file secure and never commit it to version control. 