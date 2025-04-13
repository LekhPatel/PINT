import requests


def send_message(url, message):
    try:
        response = requests.post(f"{url}/receive", data={"text": message})
        print("Pi B response:", response.text)
        return f"Sent to {url} — Response: {response.text}"
    except Exception as e:
        return f" Error: {e}"
