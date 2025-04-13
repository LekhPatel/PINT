import requests


def send_message(url, message):
    try:
        response = requests.post(f"{url}/receive", data={"text": message})
        print("Pi B response:", response.text)
        return f"Sent to {url} — Response: {response.text}"
    except Exception as e:
        return f" Error: {e}"

def webreq(url, website):
    try:
        response = requests.post(f"{url}/webreq", data={"text": website})
        print("Pi B response:", response.text)
        return f"Sent to {url} — Response: {response.text}"
    except Exception as e:
        return f" Error: {e}"

def filesend(url, files):
    try:
        response = requests.post(f"{url}/upload", files=files)
        print("Pi B response:", response.text)
        return f"Sent to {url} — Response: {response.text}"
    except Exception as e:
        return f" Error: {e}"