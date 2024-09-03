import requests
import json

# Replace this with your actual Google Chat webhook URL
GOOGLE_CHAT_WEBHOOK_URL = 'YOUR_GOOGLE_CHAT_WEBHOOK_URL'

def fetch_merged_data(api_url):
    """Fetch data from the API endpoint."""
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from {api_url}: {e}")
        return None

def send_message_to_google_chat(message):
    """Send a formatted message to Google Chat using the webhook URL."""
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }

    payload = {
        "text": message
    }

    try:
        response = requests.post(GOOGLE_CHAT_WEBHOOK_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        print("Message sent to Google Chat successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message to Google Chat: {e}")

def format_message(data):
    """Format the data into a message string."""
    if not data:
        return "No data available."

    message = "Latest Versions:\n"
    for app_name, info in data.items():
        version = info.get('version', 'Error fetching data')
        if version == 'Error fetching data':
            message += f"{app_name}: {version}\n"
        else:
            message += f"{app_name}: {version}\n"
    return message

def main():
    api_url = 'http://localhost:5001/api/merged'
    data = fetch_merged_data(api_url)
    message = format_message(data)
    send_message_to_google_chat(message)

if __name__ == "__main__":
    main()
