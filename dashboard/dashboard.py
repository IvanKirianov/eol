from flask import Flask, render_template
import requests

app = Flask(__name__)

PUBLIC_REPO_API_URL = "http://localhost:5001/api/merged"

def fetch_public_repo_data():
    try:
        response = requests.get(PUBLIC_REPO_API_URL)
        response.raise_for_status()
        data = response.json()

        formatted_data = {}
        for app_name, details in data.items():
            print(f"Raw Data for {app_name}: {details}")  # Debugging output

            # Extract version and latest values
            version = details.get("version", "").replace("v", "").strip()
            latest = details.get("latest", "").replace("v", "").strip()

            # Use 'latest' if 'version' is not available
            display_value = version if version else latest

            # Only display numeric cycle values
            cycle = details.get("cycle", "").strip()
            if not cycle.isdigit():
                cycle = ""

            # Display the version if available; otherwise, use the cycle
            if display_value:
                formatted_data[app_name] = display_value
            elif cycle:
                formatted_data[app_name] = cycle
            else:
                formatted_data[app_name] = ""

            print(f"Formatted Data for {app_name}: {formatted_data[app_name]}")  # Debugging output

        print(f"Final formatted data: {formatted_data}")  # Debugging output of all data
        return formatted_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}

@app.route('/')
def index():
    public_repo_data = fetch_public_repo_data()
    print(f"Data sent to template: {public_repo_data}")  # Debugging output
    return render_template('dashboard.html', public_repo_data=public_repo_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
