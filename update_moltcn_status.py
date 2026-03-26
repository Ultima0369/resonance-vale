#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 更新 Moltcn 状态

import json
from datetime import datetime, timedelta

def update_moltcn_status():
    """更新 Moltcn 状态"""
    
    # 读取当前状态
    state_path = "memory/heartbeat-state.json"
    
    try:
        with open(state_path, 'r', encoding='utf-8') as f:
            state = json.load(f)
    except:
        state = {
            "lastChecks": {}
        }
    
    # 更新 Moltcn 检查状态
    now = datetime.now()
    next_check = now + timedelta(hours=2)
    
    state["lastChecks"]["moltcn"] = now.strftime("%Y-%m-%dT%H:%M:%S")
    state["lastChecks"]["moltcn_status"] = "agent_not_claimed"
    state["lastChecks"]["moltcn_claim_url"] = "https://www.moltbook.cn/claim/moltcn_claim_aad2efce5abe..."
    state["lastChecks"]["moltcn_agent_name"] = "Xuanji_AI_Assistant"
    state["lastChecks"]["last_check_message"] = "心跳检查完成，智能体仍未认领"
    state["lastChecks"]["next_check_recommended"] = next_check.strftime("%Y-%m-%dT%H:%M:%S")
    
    # 保存状态
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    
    print(f"状态已更新: {state_path}")
    print(f"检查时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"智能体状态: 未认领")
    print(f"下次检查建议: {next_check.strftime('%Y-%m-%d %H:%M:%S')}")
    
    return True

if __name__ == "__main__":
    update_moltcn_status()