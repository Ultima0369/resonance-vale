import json

with open('C:/Users/lgdln/.openclaw/workspace/memory/heartbeat-state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

print("智能体信息:")
print(f"名称: {state['moltcn']['agentName']}")
print(f"状态: {state['moltcn']['status']}")
print(f"API Key: {state['moltcn']['apiKey']}")
print(f"认领链接: {state['moltcn']['claimUrl']}")
print(f"邮箱: {state['moltcn']['email']}")
print(f"邮箱验证: {state['moltcn']['emailVerified']}")
print(f"上次检查: {state['moltcn']['lastCheck']}")
print(f"下次检查: {state['moltcn']['nextCheck']}")
print(f"待办任务: {state['moltcn']['postClaimTasks']}")