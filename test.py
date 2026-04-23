import requests

API_KEY = "86c2923a-9faf-4c2c-9e2e-6895f34e69d1"

res = requests.post(
    "http://localhost:8000/api/chat",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"message": "bayrak nedir"}
)

print(res.json())