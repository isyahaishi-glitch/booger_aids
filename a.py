import requests
import json

# Replace with your actual (new) API key
API_KEY = "AIzaSyCNEw_z4g3DMkYRh31TOuJGFEDtgJFn2Ig"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"

headers = {
    "Content-Type": "application/json"
}

data = {
    "contents": [
        {
            "parts": [
                {"text": "Explain how AI works in a few words"}
            ]
        }
    ]
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    print(response.json()['candidates'][0]['content']['parts'][0]['text'])
else:
    print(f"Error: {response.status_code}")
    print(response.text)