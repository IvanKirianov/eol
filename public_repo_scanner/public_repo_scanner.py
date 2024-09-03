from flask import Flask, jsonify
import requests
from endpoints import ENDPOINTS

app = Flask(__name__)

def get_latest_record(data):
    """Extract the latest record from a list of records based on 'date' field."""
    if isinstance(data, list) and len(data) > 0:
        latest_record = max(data, key=lambda x: x.get('date', ''))
        return latest_record
    return {"error": "No records found or data format is incorrect"}

def get_latest_release(url):
    """Fetch the latest release version from a GitHub releases page or API endpoint."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        try:
            release_data = response.json()
        except ValueError as e:
            app.logger.error(f"Failed to parse JSON from {url}: {e}")
            return 'Error parsing data'

        app.logger.info(f"Response from {url}: {release_data}")

        # Extract version name from the response
        if isinstance(release_data, dict) and 'name' in release_data:
            return release_data['name']

        return 'No version found'

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Failed to fetch latest release from {url}: {e}")
        return 'Error fetching data'

@app.route('/')
def list_endpoints():
    """Generate an HTML page listing all available endpoints."""
    html_content = """
    <html>
    <body>
        <h1>Public Repo Scanner API</h1>
        <p>Use the following endpoints to get information:</p>
        <ul>
    """
    for app_name, config in ENDPOINTS.items():
        html_content += f"<li><a href='/api/{app_name}'>{app_name}</a> - {config['description']}</li>\n"
    html_content += """
        </ul>
    </body>
    </html>
    """
    return html_content

@app.route('/api/<app_name>')
def get_application_data(app_name):
    """Fetch and return the latest version or record for the specified application."""
    config = ENDPOINTS.get(app_name)
    if not config:
        return jsonify({"error": "Endpoint not found"}), 404

    url = config['url']
    try:
        if app_name in ['karpenter', 'cilium', 'keda', 'metrics-server', 'nginx-ingress', 'secrets-store-csi-driver-provider-aws']:
            version_number = get_latest_release(url)
            return jsonify({"version": version_number})

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        latest_record = get_latest_record(data)
        return jsonify(latest_record)

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching data from {url}: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/api/merged')
def get_merged_data():
    """Fetch and return the latest version or record for all applications combined into one JSON."""
    combined_data = {}
    for app_name, config in ENDPOINTS.items():
        url = config['url']
        try:
            if app_name in ['karpenter', 'cilium', 'keda', 'metrics-server', 'nginx-ingress', 'secrets-store-csi-driver-provider-aws']:
                version_number = get_latest_release(url)
                combined_data[app_name] = {"version": version_number}
            else:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                latest_record = get_latest_record(data)
                combined_data[app_name] = latest_record

        except requests.exceptions.RequestException as e:
            app.logger.error(f"Error fetching data from {url} for {app_name}: {e}")
            combined_data[app_name] = {"error": str(e)}
        except Exception as e:
            app.logger.error(f"Unexpected error for {app_name}: {e}")
            combined_data[app_name] = {"error": "Internal Server Error"}

    return jsonify(combined_data)

@app.route('/routes')
def list_routes():
    """List all available routes."""
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        output.append(f"{rule.endpoint}: {rule.rule} [{methods}]")
    return '<br>'.join(output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
