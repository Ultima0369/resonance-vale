#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Obsidian 仓库备份脚本

import shutil
from datetime import datetime
from pathlib import Path

def backup_vault(vault_path="D:/LDD/璇玑台"):
    """备份 Obsidian 仓库"""
    
    vault = Path(vault_path)
    if not vault.exists():
        print(f"错误: 仓库不存在: {vault}")
        return False
    
    # 创建备份路径
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = vault.parent / f"{vault.name}_备份_{timestamp}"
    
    print(f"开始备份: {vault}")
    print(f"备份到: {backup_path}")
    
    if backup_path.exists():
        print("警告: 备份目录已存在，跳过备份")
        return False
    
    try:
        # 复制整个仓库
        shutil.copytree(vault, backup_path)
        print(f"备份完成: {backup_path}")
        
        # 计算备份大小
        total_size = sum(f.stat().st_size for f in backup_path.rglob('*') if f.is_file())
        print(f"备份大小: {total_size / 1024 / 1024:.2f} MB")
        
        return True
    except Exception as e:
        print(f"备份失败: {e}")
        return False

if __name__ == "__main__":
    backup_vault()