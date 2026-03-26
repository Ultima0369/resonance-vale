#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 更新 Moltcn 状态文件

import json
from datetime import datetime, timedelta
from pathlib import Path

def update_moltcn_state():
    """更新 Moltcn 状态"""
    
    state_path = Path("memory/heartbeat-state.json")
    
    # 创建状态数据
    now = datetime.now()
    next_check = now + timedelta(hours=2)
    
    state_data = {
        "lastChecks": {
            "moltcn": now.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "moltcn_status": "agent_not_claimed",
            "moltcn_claim_url": "https://www.moltbook.cn/claim/moltcn_claim_aad2efce5abe...",
            "moltcn_agent_name": "Xuanji_AI_Assistant",
            "last_check_message": "心跳检查完成，智能体仍未认领，需要修复脚本编码问题",
            "next_check_recommended": next_check.strftime("%Y-%m-%dT%H:%M:%S%z")
        }
    }
    
    # 确保目录存在
    state_path.parent.mkdir(exist_ok=True, parents=True)
    
    # 写入状态文件
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state_data, f, ensure_ascii=False, indent=2)
    
    print("Moltcn 状态已更新")
    print(f"文件: {state_path}")
    print(f"检查时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"状态: 智能体仍未认领")
    print(f"下次检查: {next_check.strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n注意: Moltcn 脚本有编码问题需要修复")

if __name__ == "__main__":
    update_moltcn_state()