import requests
import json

API_KEY = "moltcn_451b6e21e70ac556015b7d051bbbcb13"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("Testing API connection...")

# Try different endpoints
endpoints = [
    "https://www.moltbook.cn/api/v1/agents/status",
    "https://www.moltbook.cn/api/v1/agent/info",
    "https://www.moltbook.cn/api/v1/status"
]

for endpoint in endpoints:
    print(f"\nTrying endpoint: {endpoint}")
    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            print(f"Response text: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")