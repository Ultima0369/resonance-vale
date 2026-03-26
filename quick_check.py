import requests
import json
from datetime import datetime

API_KEY = "moltcn_451b6e21e70ac556015b7d051bbbcb13"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("快速检查智能体状态...")
print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

try:
    response = requests.get("https://www.moltbook.cn/api/v1/agents/status", headers=headers, timeout=10)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"智能体状态: {json.dumps(data, indent=2, ensure_ascii=False)}")
    else:
        print(f"响应: {response.text}")
        
except Exception as e:
    print(f"错误: {e}")