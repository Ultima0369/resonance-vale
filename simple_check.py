import requests
import json
from datetime import datetime

API_KEY = "moltcn_451b6e21e70ac556015b7d051bbbcb13"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print(f"Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

try:
    response = requests.get("https://www.moltbook.cn/api/v1/agents/status", headers=headers, timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Agent claimed: {json.dumps(data, ensure_ascii=False)}")
    elif response.status_code == 403:
        error_data = response.json()
        print(f"Agent not claimed: {error_data.get('error', 'Unknown error')}")
        print(f"Hint: {error_data.get('hint', 'No hint provided')}")
    else:
        print(f"Status {response.status_code}: {response.text[:100]}")
        
except Exception as e:
    print(f"Connection error: {e}")