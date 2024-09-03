import requests
import json

WEBHOOK_URL = 'https://chat.googleapis.com/v1/spaces/AAA.../messages?key=...&token=...'

def fetch_merged_data():
    """Fetches merged data from the API."""
    try:
        response = requests.get('http://localhost:5001/api/merged')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching merged data: {e}")
        return None

def format_message(data):
    """Formats the Google Chat message based on merged data."""
    message = "*Dependency Update*\n\n"

    for item in data:
        name = item.get("name", "Unknown")
        version = item.get("version", "")
        cycle = item.get("cycle", "")

        # Format the version and cycle output
        version_output = f"{version}".lstrip('v') if version else ""
        cycle_output = f"({cycle})" if cycle and cycle.isdigit() else ""

        # Combine version and cycle
        formatted_output = f"{version_output} {cycle_output}".strip()

        if formatted_output:
            message += f"*{name}*: {formatted_output}\n"
        else:
            message += f"*{name}*: No data available\n"

    return {
        "text": message
    }

def send_message_to_google_chat(message):
    """Sends a formatted message to Google Chat via webhook."""
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }
    try:
        response = requests.post(WEBHOOK_URL, headers=headers, data=json.dumps(message))
        response.raise_for_status()
        print("Message sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Google Chat: {e}")

def main():
    """Main function to fetch merged data and send the Google Chat message."""
    merged_data = fetch_merged_data()
    if merged_data:
        formatted_message = format_message(merged_data)
        send_message_to_google_chat(formatted_message)

if __name__ == "__main__":
    main()
