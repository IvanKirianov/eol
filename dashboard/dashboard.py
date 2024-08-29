from flask import Flask, render_template
import requests

app = Flask(__name__)

PUBLIC_REPO_SCANNER_URL = 'http://localhost:5001/api/merged'

def fetch_public_repo_data():
    """Fetch data from public_repo_scanner API and return as a dictionary."""
    try:
        response = requests.get(PUBLIC_REPO_SCANNER_URL)
        response.raise_for_status()
        data = response.json()

        result = {}
        for app_name, details in data.items():
            version = details.get('version', 'No public available version data')
            cycle = details.get('cycle', '')
            result[app_name] = f"{version} (Cycle: {cycle})"
        return result

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.route('/')
def index():
    """Render the dashboard HTML with the data from the public_repo_scanner API."""
    data = fetch_public_repo_data()
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
