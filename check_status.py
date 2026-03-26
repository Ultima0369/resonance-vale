import requests
import json
from datetime import datetime

API_KEY = "moltcn_451b6e21e70ac556015b7d051bbbcb13"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

try:
    response = requests.get("https://www.moltbook.cn/api/v1/agents/status", headers=headers, timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 智能体已认领: {json.dumps(data, ensure_ascii=False)}")
    elif response.status_code == 403:
        error_data = response.json()
        print(f"❌ 智能体未认领: {error_data.get('error', 'Unknown error')}")
        print(f"💡 提示: {error_data.get('hint', 'No hint provided')}")
    else:
        print(f"⚠️ 状态码 {response.status_code}: {response.text[:100]}")
        
except Exception as e:
    print(f"🚫 连接错误: {e}")