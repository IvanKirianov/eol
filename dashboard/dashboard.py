from flask import Flask, render_template
import requests

app = Flask(__name__)

def fetch_public_repo_data():
    """Fetch and return the data from the public-repo-scanner API."""
    try:
        response = requests.get('http://localhost:5001/api/merged')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching public-repo-scanner data: {e}")
        return {}

@app.route('/')
def index():
    """Render the dashboard page."""
    public_repo_data = fetch_public_repo_data()
    return render_template('dashboard.html', public_repo_data=public_repo_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
