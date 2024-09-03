import requests
import json

def send_to_google_chat(webhook_url, api_url):
    try:
        # Fetch data from the API
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        if not isinstance(data, dict):
            raise ValueError(f"Unexpected data format from API, expected dict, got {type(data)}")

        # Build the message for Google Chat
        cards = []
        for service, service_data in data.items():
            if isinstance(service_data, dict):
                version = service_data.get('version', 'N/A')
                cycle = service_data.get('cycle', 'N/A')
                message = f"*Service*: {service}\n*Version*: {version}\n*Cycle*: {cycle}"
                cards.append({"header": {"title": f"{service} - Latest Release"}, "sections": [{"widgets": [{"textParagraph": {"text": message}}]}]})
            else:
                message = f"*Service*: {service}\n*Data*: {service_data}"
                cards.append({"header": {"title": f"{service} - Data"}, "sections": [{"widgets": [{"textParagraph": {"text": message}}]}]})

        # Send the message to Google Chat
        chat_message = {"cards": cards}
        headers = {'Content-Type': 'application/json'}
        chat_response = requests.post(webhook_url, data=json.dumps(chat_message), headers=headers)

        if chat_response.status_code != 200:
            raise Exception(f"Failed to send message to Google Chat, status code: {chat_response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

# Example usage:
webhook_url = "YOUR_WEBHOOK_URL"
api_url = "http://localhost:5001/api/merged"
send_to_google_chat(webhook_url, api_url)
